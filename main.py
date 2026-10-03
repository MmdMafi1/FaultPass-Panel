# ============================================================
# FaultPass 15.0.0
# Railway Ready
# ============================================================

import asyncio
from untitled_ui import inject as _uui
import base64
import hashlib
import json
import logging
import os
import re
import secrets
import string
import time
import psutil

from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote, parse_qs

import aiofiles
import httpx
import uvicorn

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Depends,
)
from fastapi.responses import (
    Response,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
)
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# APP
# ============================================================

APP_NAME = "FaultPass"
SALES_ENABLED = __import__("os").environ.get("FAULTPASS_SALES_ENABLED", "0").strip().lower() in ("1", "true", "yes", "on")


def sales_enabled_now() -> bool:
    """مقدار زنده‌ی «فروشگاه فعاله یا نه» — از پنل قابل تغییره و نیازی به
    ری‌استارت سرور نداره. اگه هنوز از پنل ست نشده باشه، مقدار اولیه‌ی متغیر
    محیطی FAULTPASS_SALES_ENABLED به‌عنوان پیش‌فرض استفاده می‌شه."""
    return bool(CONFIG.get("sales_enabled", SALES_ENABLED))
APP_VERSION = "27.3.0"

SUPPORT_USERNAME = "@FaultPass"
SUPPORT_URL = "https://t.me/FaultPass"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(APP_NAME)


# ============================================================
# TIMEZONE
# ============================================================

try:
    from zoneinfo import ZoneInfo

    IRAN_TZ = ZoneInfo("Asia/Tehran")

except Exception:
    IRAN_TZ = None


# ============================================================
# RAILWAY
# ============================================================

PORT = int(
    os.environ.get(
        "PORT",
        "8000",
    )
)

DATA_DIR = Path(
    os.environ.get(
        "RAILWAY_VOLUME_MOUNT_PATH",
        os.environ.get(
            "DATA_DIR",
            "./data",
        ),
    )
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATA_FILE = DATA_DIR / "faultpass_state.json"
SECRET_FILE = DATA_DIR / "faultpass_secret.key"


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOCKS
# ============================================================

SAVE_LOCK = asyncio.Lock()
LINKS_LOCK = asyncio.Lock()
SUBS_LOCK = asyncio.Lock()
SESSIONS_LOCK = asyncio.Lock()


# ============================================================
# SECRET
# ============================================================

def load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")

    if env_secret:
        return env_secret

    try:
        if SECRET_FILE.exists():
            existing = (
                SECRET_FILE
                .read_text(
                    encoding="utf-8"
                )
                .strip()
            )

            if existing:
                return existing

        generated = secrets.token_urlsafe(48)

        SECRET_FILE.write_text(
            generated,
            encoding="utf-8",
        )

        return generated

    except Exception as exc:
        logger.warning(
            "Could not persist SECRET_KEY: %s",
            exc,
        )

        return secrets.token_urlsafe(48)


SECRET_KEY = load_or_create_secret()


# ============================================================
# CONFIG
# ============================================================

CONFIG = {
    "port": PORT,
    "secret": SECRET_KEY,
    "host": os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN",
        "localhost",
    ),
   
    "tcp_public_host": os.environ.get("TCP_PUBLIC_HOST", "").strip(),
    "tcp_public_port": os.environ.get("TCP_PUBLIC_PORT", "").strip(),
}


# ============================================================
# STATE
# ============================================================

LINKS: dict = {}
SUBS: dict = {}
# Per-subscription live usage samples. Values come from the real link used_bytes field.
SUB_USAGE_HISTORY = defaultdict(lambda: deque(maxlen=144))
USAGE_PERSIST_TASK = None
SESSIONS: dict = {}
connections: dict = {}
CATEGORIES: dict = {}
DAILY_STATS: dict = {}  # "YYYY-MM-DD" -> {"traffic_bytes":.., "new_links":.., "orders":.., "stars":..}
DAILY_STATS_LOCK = asyncio.Lock()


def _today_key() -> str:
    now = datetime.now(IRAN_TZ) if IRAN_TZ else datetime.now()
    return now.strftime("%Y-%m-%d")


def bump_daily_stat(field: str, amount=1):
    """Increment a counter in today's reporting bucket (best-effort, in-memory)."""
    try:
        key = _today_key()
        bucket = DAILY_STATS.setdefault(
            key, {"traffic_bytes": 0, "new_links": 0, "orders": 0, "stars": 0}
        )
        bucket[field] = bucket.get(field, 0) + amount
        # keep only the last 180 days to avoid unbounded growth
        if len(DAILY_STATS) > 180:
            for old_key in sorted(DAILY_STATS.keys())[: len(DAILY_STATS) - 180]:
                DAILY_STATS.pop(old_key, None)
    except Exception:
        pass

stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}

_telemetry_lock = asyncio.Lock()
_telemetry_prev = {"ts": time.time(), "rx": 0, "tx": 0}


def _pct(v):
    try:
        return round(float(v), 1)
    except Exception:
        return 0.0


def _human_uptime(seconds):
    seconds = max(0, int(seconds))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    if days:
        return f"{days}d {hours:02d}:{minutes:02d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

error_logs = deque(maxlen=100)
activity_logs = deque(maxlen=250)

hourly_traffic = defaultdict(int)
# Real server telemetry samples used by the dashboard charts.
# Samples are collected from psutil; no placeholder/synthetic values are generated.
TELEMETRY_HISTORY = deque(maxlen=90)

http_client: httpx.AsyncClient | None = None


# ============================================================
# PROTOCOL
# ============================================================

PROTOCOLS = (
    "vless-ws",
    "vless-tcp",
    "xhttp-packet-up",
    "xhttp-stream-up",
    "xhttp-stream-one",
    "vmess-ws",
    "trojan-ws",
)

# این پروتکل‌ها روی همان پورت HTTP/WebSocket برنامه (پشت TLS ری‌ورس‌پروکسی یا Railway)
# سرو می‌شن و واقعاً روی سرور پیاده‌سازی شده‌ن.
REAL_TRANSPORT_PROTOCOLS = {
    "vless-ws", "xhttp-packet-up", "xhttp-stream-up",
}
# vless-tcp هم واقعی و پیاده‌سازی‌شده‌ست ولی روی یک پورت TCP خام و جداگانه
# (به‌صورت پیش‌فرض 6543، قابل تغییر با TCP_LISTEN_PORT) — نه پورت HTTP اصلی.
REAL_RAW_TCP_PROTOCOLS = {"vless-tcp"}
# همه‌ی پروتکل‌های دمو/غیرفعال از پنل حذف شده‌اند — هر چیزی که در PROTOCOLS باشد واقعاً کار می‌کند.
NON_FUNCTIONAL_DEMO_PROTOCOLS = {"vmess-ws", "trojan-ws"}

# Protocols that this project actually serves itself. VMess/Trojan entries may
# still be generated as client-side links, but they are NOT advertised as live
# listeners because this backend has no VMess/Trojan inbound parser.
LIVE_PROTOCOLS = REAL_TRANSPORT_PROTOCOLS | REAL_RAW_TCP_PROTOCOLS

PROTOCOL_LABELS = {
    "vless-ws": "VLESS WebSocket",
    "vless-tcp": "VLESS TCP (خام)",
    "xhttp-packet-up": "XHTTP Packet Up",
    "xhttp-stream-up": "XHTTP Stream Up",
    "xhttp-stream-one": "XHTTP Stream One",
    "vmess-ws": "VMess WebSocket",
    "trojan-ws": "Trojan WebSocket",
    "manual": "پروتکل دستی (سفارشی)",
}

PROTOCOL_ALIASES = {
    "vmess": "vmess-ws", "trojan": "trojan-ws", "ss": "shadowsocks",
    "socks": "socks5", "hy2": "hysteria2", "hysteria": "hysteria2",
}

DEFAULT_PROTOCOL = "vless-ws"

# نگاشت هر پروتکل غیر-دستی (manual) به Network/Security واقعی‌ای که در لینک
# نهایی (generate_vless_link) استفاده می‌شود. این فقط برای نمایش صحیح در پنل
# است (تگ‌های "ws/tls" و ...)؛ چون قبلاً این مقادیر همیشه روی مقدار پیش‌فرض
# فیلدهای دستی (tcp/none) می‌افتادند، حتی برای پروتکل‌هایی که واقعاً ws+tls بودند.
PROTOCOL_NETWORK_SECURITY = {
    "vless-ws": ("ws", "tls"),
    "vless-tcp": ("tcp", "none"),
    "xhttp-packet-up": ("xhttp", "tls"),
    "xhttp-stream-up": ("xhttp", "tls"),
    "xhttp-stream-one": ("xhttp", "tls"),
    "vmess-ws": ("ws", "tls"),
    "trojan-ws": ("ws", "tls"),
}

FINGERPRINTS = (
    "chrome",
    "firefox",
    "safari",
    "ios",
    "android",
    "edge",
    "360",
    "qq",
    "random",
    "randomized",
)

DEFAULT_FINGERPRINT = "chrome"

DEFAULT_ALPN_BY_PROTOCOL = {
    "vless-ws": "http/1.1",
    "xhttp-packet-up": "h2,http/1.1",
    "xhttp-stream-up": "h2,http/1.1",
    "xhttp-stream-one": "h2,http/1.1",
}

DEFAULT_PORT = 443
MIN_PORT = 1
MAX_PORT = 65535

DEFAULT_SPEED_LIMIT = 0


# ============================================================
# MANUAL PROTOCOL BUILDER (پروتکل دستی — مثل پنل‌های 3x-ui/Sanaei)
# ============================================================


MANUAL_BASE_PROTOCOLS = ("vless", "vmess", "trojan", "shadowsocks")

MANUAL_BASE_PROTOCOL_LABELS = {
    "vless": "VLESS",
    "vmess": "VMess",
    "trojan": "Trojan",
    "shadowsocks": "Shadowsocks",
}

NETWORKS = ("tcp", "ws", "grpc", "xhttp")

NETWORK_LABELS = {
    "tcp": "TCP",
    "ws": "WebSocket (ws)",
    "grpc": "gRPC",
    "xhttp": "XHTTP",
}

SECURITIES = ("none", "tls", "reality")

SECURITY_LABELS = {
    "none": "بدون امنیت (None)",
    "tls": "TLS",
    "reality": "Reality",
}

XHTTP_MODES = ("auto", "packet-up", "stream-up", "stream-one")
SHADOWSOCKS_METHODS = ("chacha20-ietf-poly1305", "aes-128-gcm", "aes-256-gcm", "2022-blake3-aes-128-gcm", "2022-blake3-aes-256-gcm")

# ترکیب‌هایی که همین پنل واقعاً به‌صورت زنده سرو می‌کند (بدون نیاز به Xray-core
# جداگانه). سایر ترکیب‌ها (مثل هر چیزی با Reality) فقط لینک/کانفیگ برای استفاده
# روی یک نود Xray-core واقعی می‌سازند و به همین دلیل در پنل با یک نشان
# «فقط ساخت لینک» مشخص می‌شوند — این محدودیت صادقانه در UI نشان داده می‌شود.
#
# نکته‌ی مهم: این پنل هیچ TLS‌ای خودش ترمینیت نمی‌کنه؛ TLS همیشه توسط لایه‌ی
# جلویی (Railway / ری‌ورس‌پروکسی خودتان) انجام می‌شه. پس این‌که کدوم ترکیب
# واقعاً «Live» حساب می‌شه به scheme واقعیِ دیپلوی (get_scheme()) بستگی داره:
# - وقتی دیپلوی روی https هست (حالت پیش‌فرض/رایج، مثل Railway): فقط ترکیب‌های
#   TLS واقعاً وصل می‌شن؛ یک کلاینت با security=none تلاش می‌کنه بدون TLS به
#   پورتی وصل بشه که فقط TLS قبول می‌کنه → هندشیک شکست می‌خوره. پس (ws,none) و
#   (xhttp,none) این‌جا صادقانه link-only هستن، نه Live.
# - فقط وقتی خودِ ادمین صراحتاً یک public_base_url با scheme=http تنظیم کرده
#   باشه (یعنی هیچ TLS‌ای جلوی این برنامه نیست)، برعکسش درسته: none واقعاً کار
#   می‌کنه ولی tls نه (چون این برنامه خودش گواهی TLS سرو نمی‌کنه).
# (tcp,none) مستقل از این‌هاست — روی یک پورت TCP خامِ جداگانه (tcp_relay.py)
# سرو می‌شه، نه پورت وب اصلی، پس همیشه معتبره.
def manual_live_combos() -> set[tuple[str, str]]:
    if get_scheme() == "http":
        return {("ws", "none"), ("xhttp", "none"), ("tcp", "none")}
    return {("ws", "tls"), ("xhttp", "tls"), ("tcp", "none")}


def normalize_protocol(protocol: str | None) -> str:
    value = str(protocol or DEFAULT_PROTOCOL).strip().lower()
    value = PROTOCOL_ALIASES.get(value, value)
    if value == "manual":
        return value
    return value if value in PROTOCOLS else DEFAULT_PROTOCOL


def normalize_network(network: str | None) -> str:
    value = str(network or "tcp").strip().lower()
    return value if value in NETWORKS else "tcp"


def normalize_security(security: str | None) -> str:
    value = str(security or "none").strip().lower()
    return value if value in SECURITIES else "none"


def normalize_xhttp_mode(mode: str | None) -> str:
    value = str(mode or "auto").strip().lower()
    return value if value in XHTTP_MODES else "auto"


def normalize_base_protocol(value: str | None) -> str:
    v = str(value or "vless").strip().lower()
    return v if v in MANUAL_BASE_PROTOCOLS else "vless"


def protocol_display_label(link: dict) -> str:
    """برچسب نمایشی پروتکل برای جدول‌ها و گزارش‌ها.
    برای کانفیگ‌های دستی به‌صورت «VLESS · WebSocket · TLS» نمایش داده می‌شود."""
    protocol = link.get("protocol", DEFAULT_PROTOCOL)
    if protocol != "manual":
        return PROTOCOL_LABELS.get(protocol, protocol)
    base = MANUAL_BASE_PROTOCOL_LABELS.get(normalize_base_protocol(link.get("base_protocol")), "VLESS")
    network = NETWORK_LABELS.get(normalize_network(link.get("network")), "TCP")
    security = SECURITY_LABELS.get(normalize_security(link.get("security")), "بدون امنیت")
    if base == "Shadowsocks":
        return f"Shadowsocks · {network}"
    return f"{base} · {network} · {security}"


# ============================================================
# LOGGING
# ============================================================

def log_activity(
    kind: str,
    message: str,
    level: str = "info",
):
    activity_logs.append(
        {
            "kind": kind,
            "level": level,
            "message": message,
            "time": datetime.now().isoformat(),
        }
    )


# ============================================================
# HELPERS
# ============================================================

def escape_html(value) -> str:
    return (
        str(
            value
            if value is not None
            else ""
        )
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )


def safe_int(
    value,
    default=0,
    minimum=0,
    maximum=None,
):
    try:
        number = int(value)
    except Exception:
        number = default

    if number < minimum:
        number = minimum

    if maximum is not None and number > maximum:
        number = maximum

    return number


def safe_float(
    value,
    default=0.0,
    minimum=0.0,
):
    try:
        number = float(value)
    except Exception:
        number = default

    return max(
        minimum,
        number,
    )


def generate_uuid():
    value = secrets.token_hex(16)

    return (
        f"{value[:8]}-"
        f"{value[8:12]}-"
        f"{value[12:16]}-"
        f"{value[16:20]}-"
        f"{value[20:32]}"
    )


def random_config_name(existing=None):
    existing = existing or set()
    alphabet = string.ascii_lowercase + string.digits
    for _ in range(80):
        length = secrets.randbelow(6) + 8
        name = "".join(secrets.choice(alphabet) for _ in range(length))
        if name not in existing and name and not name[0].isdigit():
            return name
    return secrets.token_hex(6)

def sanitize_config_name(name: str) -> str:
    if not name:
        return random_config_name()
    # Allow letters (Persian/Arabic/Latin/etc.), digits, emoji, @ and common
    # punctuation/spaces. Only strip control characters and newlines, which
    # could break stored records or display.
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", str(name)).strip()
    if not cleaned:
        return random_config_name()
    return cleaned[:40]

def auto_config_name() -> str:
    return random_config_name()


def now_ir():
    if IRAN_TZ:
        return datetime.now(IRAN_TZ)

    return datetime.now()


def uptime():
    seconds = int(
        time.time()
        - stats["start_time"]
    )

    h = seconds // 3600

    m = (
        seconds
        % 3600
    ) // 60

    s = (
        seconds
        % 60
    )

    return (
        f"{h:02d}:"
        f"{m:02d}:"
        f"{s:02d}"
    )


def fmt_bytes(value: int):
    value = int(
        value or 0
    )

    if value < 1024:
        return f"{value} B"

    if value < 1024 ** 2:
        return (
            f"{value / 1024:.1f} KB"
        )

    if value < 1024 ** 3:
        return (
            f"{value / 1024 ** 2:.2f} MB"
        )

    return (
        f"{value / 1024 ** 3:.2f} GB"
    )


def parse_size_to_bytes(
    value: float,
    unit: str,
):
    if value <= 0:
        return 0

    unit = (
        unit
        or "GB"
    ).upper()

    if unit == "TB":
        return int(
            value
            * 1024 ** 4
        )

    if unit == "GB":
        return int(
            value
            * 1024 ** 3
        )

    if unit == "MB":
        return int(
            value
            * 1024 ** 2
        )

    if unit == "KB":
        return int(
            value
            * 1024
        )

    return int(value)


def parse_speed_to_bytes(
    value: float,
    unit: str,
):
    if value <= 0:
        return 0

    unit = (
        unit
        or "MBIT"
    ).upper()

    if unit == "MBIT":
        return int(
            value
            * 1024
            * 1024
            / 8
        )

    if unit == "KB":
        return int(
            value * 1024
        )

    if unit == "MB":
        return int(
            value
            * 1024
            * 1024
        )

    return int(value)


def is_link_expired(
    link: dict,
):
    expiry = link.get(
        "expires_at"
    )

    if not expiry:
        return False

    try:
        return (
            datetime.now()
            > datetime.fromisoformat(
                expiry
            )
        )

    except Exception:
        return False


def is_link_allowed(
    link: dict | None,
):
    if link is None:
        return False

    if not link.get(
        "active",
        True,
    ):
        return False

    if is_link_expired(link):
        return False

    limit = int(
        link.get(
            "limit_bytes",
            0,
        )
        or 0
    )

    used = int(
        link.get(
            "used_bytes",
            0,
        )
        or 0
    )

    if (
        limit > 0
        and used >= limit
    ):
        return False

    return True


def link_visible_for_subscription(link: dict | None) -> bool:
    """برای فید/صفحه‌ی سابسکریپشن: تا وقتی ادمین دستی کانفیگ رو خاموش نکرده،
    حتی بعد از تموم شدن حجم یا رسیدن انقضا هم قابل مشاهده می‌مونه — تا مشتری
    بتونه ببینه دقیقاً چقدر مصرف کرده و کِی تموم شده، به‌جای یک ۴۰۴ خام که
    باعث می‌شه اپلیکیشن‌های کلاینت درصد مصرف رو اصلاً نشون ندن یا فریز کنن.
    اتصال واقعیِ رله (VLESS-WS/TCP/XHTTP) کماکان توسط is_link_allowed
    (سخت‌گیرانه، شامل چک حجم و انقضا) کنترل می‌شه و این تابع هیچ اتصالی رو
    مجاز نمی‌کنه، فقط نمایش اطلاعات رو."""
    if link is None:
        return False
    return bool(link.get("active", True))


def unique_ips_for_uuid(
    uuid: str,
):
    return {
        connection.get("ip")
        for connection in connections.values()
        if connection.get("uuid") == uuid
        and connection.get("ip")
    }


def client_ip(
    request: Request,
):
    forwarded = request.headers.get(
        "x-forwarded-for"
    )

    if forwarded:
        return (
            forwarded
            .split(",")[0]
            .strip()
        )

    real = request.headers.get(
        "x-real-ip"
    )

    if real:
        return real.strip()

    if request.client:
        return request.client.host

    return "unknown"


def is_ip_allowed(
    link: dict | None,
    uuid: str,
    ip: str,
):
    if link is None:
        return False

    limit = int(
        link.get(
            "ip_limit",
            0,
        )
        or 0
    )

    if limit <= 0:
        return True

    ips = unique_ips_for_uuid(uuid)

    if ip in ips:
        return True

    return len(ips) < limit


def _split_base_url(raw: str):
    """آدرس عمومی ذخیره‌شده رو به (scheme, host) تجزیه می‌کنه. ورودی می‌تونه
    با یا بدون scheme باشه (مثلاً 'panel.example.com' یا 'https://panel.example.com')."""
    raw = (raw or "").strip()
    if not raw:
        return None, None
    scheme = "https"
    rest = raw
    if "://" in raw:
        scheme, rest = raw.split("://", 1)
        scheme = scheme.strip().lower() or "https"
    host = rest.split("/", 1)[0].split(":")[0].strip()
    return (scheme if scheme in ("http", "https") else "https"), (host or None)


def get_host(
    request: Request | None = None,
) -> str:
    # اولویت اول: آدرس عمومی صریحی که در تنظیمات پنل ثبت شده (پایدار، مستقل از
    # اینکه درخواست از کجا اومده — پروکسی، آی‌پی داخلی، هلث‌چک و ...).
    _, override_host = _split_base_url(CONFIG.get("public_base_url"))
    if override_host:
        return override_host

    if request is not None:
        forwarded = request.headers.get(
            "x-forwarded-host"
        )

        normal = request.headers.get(
            "host"
        )

        host = (
            forwarded
            or normal
        )

        if host:
            # توجه: دیگه CONFIG["host"] رو اینجا آپدیت نمی‌کنیم؛ این یک متغیر سراسری
            # مشترک بین همه‌ی درخواست‌ها بود و هر درخواست با Host نادرست (هلث‌چک،
            # اسکنر، وبهوک) می‌تونست لینک‌های بعدیِ همه رو خراب کنه.
            return host.split(":")[0].strip()

    railway_domain = os.environ.get(
        "RAILWAY_PUBLIC_DOMAIN"
    )

    if railway_domain:
        return railway_domain

    return CONFIG["host"]


def get_scheme() -> str:
    """scheme (http/https) که باید برای ساخت لینک‌های ساب استفاده بشه."""
    scheme, host = _split_base_url(CONFIG.get("public_base_url"))
    if host:
        return scheme
    return "https"


def _tcp_listen_port_snapshot() -> int:
    try:
        import tcp_relay
        return tcp_relay.TCP_LISTEN_PORT
    except Exception:
        return int(os.environ.get("TCP_LISTEN_PORT", "6543"))


def _bot_settings_snapshot() -> dict:
    """وضعیت فعلی ربات فروش رو برمی‌گردونه؛ اگه ماژول ربات هنوز ایمپورت نشده
    یا مشکلی داشته باشه، مقدار خالی/امن برمی‌گردونه (این نباید کل پنل رو خراب کنه)."""
    try:
        import telegram_bot
        return telegram_bot.current_config()
    except Exception:
        return {"bot_token": "", "admin_ids": "", "running": False}


# ============================================================
# PASSWORD
# ============================================================

def hash_password(
    password: str,
) -> str:

    payload = (
        password
        + SECRET_KEY
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


DEFAULT_ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin").strip() or "admin"
DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

AUTH = {
    "username": DEFAULT_ADMIN_USERNAME,
    "password_hash":
        hash_password(
            DEFAULT_ADMIN_PASSWORD
        )
}

# ============================================================
# MULTI-ADMIN (sub-admins beyond the owner account)
# ============================================================
# The "owner" account is always backed by AUTH["password_hash"] above
# (fully backward compatible with older single-admin deployments).
# Additional named admin accounts live here and can be managed from
# the "مدیریت ادمین‌ها" tab in the dashboard.

ADMINS: dict = {}

# ============================================================
# ADMIN REGISTRATION REQUESTS ("ثبت‌نام ادمینی" از صفحه لاگین)
# ============================================================
# کاربری که می‌خواهد ادمین شود، فقط نام و آیدی تلگرام خود را از صفحه
# لاگین ارسال می‌کند. درخواست او اینجا به‌صورت pending ذخیره می‌شود تا
# مالک پنل از بخش «مدیریت حساب‌ها» آن را ببیند، تصمیم بگیرد چه دسترسی‌ها
# و چه رمز/نام‌کاربری‌ای به او بدهد، و در صورت تایید حساب ادمین واقعی
# برایش ساخته شود.
ADMIN_REQUESTS: dict = {}
ADMIN_REQUEST_RATE: dict = {}  # ip -> last submit timestamp (ضد اسپم ساده)
ADMIN_REQUEST_COOLDOWN_SECONDS = 60
ADMIN_REQUESTS_LOCK = asyncio.Lock()

ALL_PERMISSIONS = {
    "dashboard": "مشاهده داشبورد",
    "inbounds": "مدیریت اینباند و کلاینت",
    "clients": "ساخت کلاینت (بخش جدا)",
    "subscriptions": "مدیریت سابسکریپشن",
    "categories": "مدیریت دسته‌بندی",
    "plans": "مدیریت پلن فروش",
    "reports": "گزارش‌ها",
    "messages": "مرکز پیام و خطا",
    "bot": "مدیریت ربات",
    "admins": "مدیریت ادمین‌ها",
    "settings": "تنظیمات پنل",
}

BOT_TEXTS = {
    "welcome": "🛡 <b>FaultPass Control Center</b>\n\nاز منوی زیر عملیات موردنظر را انتخاب کنید.",
    "admin_menu": "🛠 <b>مدیریت پنل</b>\n\nساخت اینباند، کلاینت، گروه ساب و مدیریت فروش از همین‌جا در دسترس است.",
    "config_created": "✅ کانفیگ با موفقیت ساخته شد.",
    "config_deleted": "🗑 کانفیگ حذف شد.",
    "config_disabled": "⛔ کانفیگ غیرفعال شد.",
    "config_enabled": "✅ کانفیگ فعال شد.",
    "store_intro": "🛒 <b>فروشگاه</b>\n\nپلن موردنظر را انتخاب کنید.",
    "payment_success": "🎉 پرداخت با موفقیت انجام شد.\n\nاشتراک شما آماده است.",
}

def get_bot_text(key: str, fallback: str = "") -> str:
    return str(BOT_TEXTS.get(key, fallback))

def permissions_for_admin(admin_id: str) -> set[str]:
    if admin_id == "owner":
        return set(ALL_PERMISSIONS)
    a = ADMINS.get(admin_id) or {}
    return set(a.get("permissions") or {"dashboard"})

async def require_permission(request: Request, permission: str):
    token = request.cookies.get(SESSION_COOKIE)
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="unauthorized")
    if permission not in permissions_for_admin(info.get("admin_id", "owner")):
        raise HTTPException(status_code=403, detail="دسترسی این قابلیت برای این ادمین فعال نیست")
    return info


def verify_admin_credentials(username: str | None, password: str):
    """Returns (ok, admin_id, role, display_name)."""
    username = (username or "").strip()
    password = password or ""

    if not username or username.lower() in {"owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower()}:
        if username and username.lower() not in {"owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower()}:
            return False, None, None, None
        if hash_password(password) == AUTH["password_hash"]:
            return True, "owner", "owner", AUTH.get("username", DEFAULT_ADMIN_USERNAME)
        return False, None, None, None

    for admin_id, admin in ADMINS.items():
        if not admin.get("active", True):
            continue
        if admin.get("username", "").lower() == username.lower():
            if hash_password(password) == admin.get("password_hash"):
                return True, admin_id, admin.get("role", "admin"), admin.get("username")
            return False, None, None, None

    return False, None, None, None


# ============================================================
# LOGIN BRUTE-FORCE PROTECTION
# ============================================================
# Maximum failed login attempts per IP inside the rolling window.
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_LOCKOUT_SECONDS = 15 * 60
LOGIN_MIN_PASSWORD_LENGTH = 6

LOGIN_FAILURES = defaultdict(deque)
LOGIN_LOCKED_UNTIL = {}


def _cleanup_login_state(ip: str, now: float | None = None):
    now = now if now is not None else time.time()

    locked_until = LOGIN_LOCKED_UNTIL.get(ip, 0)
    if locked_until and locked_until <= now:
        LOGIN_LOCKED_UNTIL.pop(ip, None)

    failures = LOGIN_FAILURES.get(ip)
    if not failures:
        return

    cutoff = now - LOGIN_WINDOW_SECONDS
    while failures and failures[0] <= cutoff:
        failures.popleft()

    if not failures:
        LOGIN_FAILURES.pop(ip, None)


def login_is_blocked(ip: str):
    now = time.time()
    _cleanup_login_state(ip, now)

    locked_until = LOGIN_LOCKED_UNTIL.get(ip, 0)
    if locked_until > now:
        return True, max(1, int(locked_until - now))

    return False, 0


def register_login_failure(ip: str):
    now = time.time()
    _cleanup_login_state(ip, now)

    failures = LOGIN_FAILURES.setdefault(ip, deque())
    failures.append(now)

    if len(failures) >= LOGIN_MAX_ATTEMPTS:
        LOGIN_LOCKED_UNTIL[ip] = now + LOGIN_LOCKOUT_SECONDS
        failures.clear()
        log_activity(
            "auth",
            f"IP به دلیل تلاش‌های متعدد ورود ناموفق به مدت {LOGIN_LOCKOUT_SECONDS // 60} دقیقه مسدود شد: {ip}",
            "err",
        )
        return True, LOGIN_LOCKOUT_SECONDS

    return False, max(0, LOGIN_MAX_ATTEMPTS - len(failures))


def clear_login_failures(ip: str):
    LOGIN_FAILURES.pop(ip, None)
    LOGIN_LOCKED_UNTIL.pop(ip, None)


# ============================================================
# SESSION
# ============================================================

SESSION_COOKIE = "faultpass_session"

SESSION_TTL = (
    60
    * 60
    * 24
    * 365
)


async def create_session(admin_id: str = "owner", role: str = "owner") -> str:

    token = secrets.token_urlsafe(48)

    async with SESSIONS_LOCK:
        SESSIONS[token] = {
            "exp": time.time() + SESSION_TTL,
            "admin_id": admin_id,
            "role": role,
            "permissions": sorted(permissions_for_admin(admin_id)),
        }

    return token


def _session_expiry(entry) -> float:
    if isinstance(entry, dict):
        return entry.get("exp", 0)
    return entry or 0


async def is_valid_session(
    token: str | None,
) -> bool:

    if not token:
        return False

    async with SESSIONS_LOCK:

        entry = SESSIONS.get(token)

        if entry is None:
            return False

        if _session_expiry(entry) < time.time():

            SESSIONS.pop(
                token,
                None,
            )

            return False

        return True


async def get_session_info(token: str | None):
    if not token:
        return None

    async with SESSIONS_LOCK:
        entry = SESSIONS.get(token)

        if entry is None:
            return None

        if _session_expiry(entry) < time.time():
            SESSIONS.pop(token, None)
            return None

        if isinstance(entry, dict):
            return dict(entry)

        return {"exp": entry, "admin_id": "owner", "role": "owner"}


async def require_owner(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    info = await get_session_info(token)

    if not info:
        raise HTTPException(status_code=401, detail="unauthorized")

    if info.get("role") != "owner":
        raise HTTPException(
            status_code=403,
            detail="فقط مالک پنل به این بخش دسترسی دارد",
        )

    return token


async def destroy_session(
    token: str | None,
):
    if not token:
        return

    async with SESSIONS_LOCK:
        SESSIONS.pop(
            token,
            None,
        )


# مقدار برگشتیِ require_auth وقتی درخواست با «توکن نود» (Bearer) احراز شده، نه نشست ادمین.
# get_session_info() برای این مقدار None می‌ده، پس endpointهای حساس (رمز، ادمین‌ها،
# نشست‌ها) که خودشون نشست واقعی می‌خوان با توکن نود هرگز کار نمی‌کنن.
NODE_API_TOKEN_MARK = "__faultpass_node_api__"


async def require_auth(
    request: Request,
):
    token = request.cookies.get(
        SESSION_COOKIE
    )

    info = await get_session_info(token)
    if not info:
        if request.headers.get("authorization"):
            try:
                from nodes import authorize_node_request
            except Exception:
                authorize_node_request = None
            if authorize_node_request and authorize_node_request(request):
                return NODE_API_TOKEN_MARK
        raise HTTPException(status_code=401, detail="unauthorized")
    if info.get("admin_id") != "owner":
        path = request.url.path
        permission = "dashboard"
        if path.startswith("/api/links") or path.startswith("/api/protocols") or path.startswith("/api/reality") or path.startswith("/api/proxies"):
            permission = "inbounds"
        elif path.startswith("/api/sub") or path.startswith("/sub"):
            permission = "subscriptions"
        elif path.startswith("/api/categories"):
            permission = "categories"
        elif path.startswith("/api/plans"):
            permission = "plans"
        elif path.startswith("/api/reports"):
            permission = "reports"
        elif path.startswith("/api/errors") or path.startswith("/api/activity"):
            permission = "messages"
        elif path.startswith("/api/settings/bot") or path.startswith("/api/bot"):
            permission = "bot"
        elif path.startswith("/api/settings"):
            permission = "settings"
        elif path.startswith("/api/telemetry") or path.startswith("/api/network"):
            permission = "dashboard"
        if permission not in permissions_for_admin(info.get("admin_id", "")):
            raise HTTPException(status_code=403, detail="دسترسی این قابلیت برای این ادمین فعال نیست")
    return token


def set_auth_cookie(
    response,
    request: Request,
    token: str,
):
    forwarded_proto = (
        request.headers
        .get(
            "x-forwarded-proto",
            "",
        )
        .lower()
    )

    is_https = (
        forwarded_proto == "https"
        or request.url.scheme == "https"
    )

    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_TTL,
        httponly=True,
        samesite="lax",
        path="/",
        secure=is_https,
    )


# ============================================================
# VLESS LINK GENERATION
# ============================================================

def generate_vless_link(
    uuid: str, host: str, remark: str = "FaultPass",
    protocol: str = DEFAULT_PROTOCOL, fingerprint: str | None = None,
    alpn: str | None = None, port: int | None = None,
):
    protocol = normalize_protocol(protocol)
    fp = (fingerprint or DEFAULT_FINGERPRINT).strip().lower()
    if fp not in FINGERPRINTS: fp = DEFAULT_FINGERPRINT
    port_value = safe_int(port, DEFAULT_PORT, MIN_PORT, MAX_PORT)
    alpn_value = (alpn or DEFAULT_ALPN_BY_PROTOCOL.get(protocol, "http/1.1")).strip()
    label = quote(str(remark or "FaultPass"), safe="")
    if protocol == "vless-ws":
        sec = "tls" if get_scheme() != "http" else "none"
        q = {"encryption":"none","security":sec,"type":"ws","host":host,"path":f"/ws/{uuid}","sni":host,"fp":fp,"alpn":alpn_value}
        return "vless://" + uuid + "@" + host + ":" + str(port_value) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol == "vless-tcp":
        # VLESS خام روی TCP — این روی پورت HTTP اصلی سرو نمی‌شه، بلکه روی یک پورت TCP
        # مجزا (tcp_relay.py) که آدرس/پورت عمومیش از تنظیمات پنل (Settings) خونده می‌شه
        # تا وقتی روی Railway (یا هر جای دیگه) با TCP Proxy جداگانه دیپلوی شد، خودت
        # می‌تونی آدرس واقعی رو دستی وارد کنی.
        tcp_host = (CONFIG.get("tcp_public_host") or "").strip() or host
        tcp_port = safe_int(CONFIG.get("tcp_public_port"), port_value, MIN_PORT, MAX_PORT)
        q = {"encryption":"none","security":"none","type":"tcp","headerType":"none"}
        return "vless://" + uuid + "@" + tcp_host + ":" + str(tcp_port) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol.startswith("xhttp-"):
        mode = protocol.replace("xhttp-", "")
        sec = "tls" if get_scheme() != "http" else "none"
        q = {"encryption":"none","security":sec,"type":"xhttp","mode":mode,"host":host,"path":f"/xhttp-siz10/{mode}/{uuid}","sni":host,"fp":fp,"alpn":alpn_value}
        return "vless://" + uuid + "@" + host + ":" + str(port_value) + "?" + "&".join(f"{k}={quote(str(v), safe=',/') }" for k,v in q.items()) + "#" + label
    if protocol == "vmess-ws":
        raw = {"v":"2","ps":remark,"add":host,"port":port_value,"id":uuid,"aid":0,"scy":"auto","net":"ws","type":"none","host":host,"path":f"/ws/{uuid}","tls":"tls","sni":host,"fp":fp}
        return "vmess://" + base64.b64encode(json.dumps(raw,separators=(",",":"),ensure_ascii=False).encode()).decode()
    if protocol == "trojan-ws":
        return f"trojan://{uuid}@{host}:{port_value}?security=tls&type=ws&host={quote(host)}&path={quote('/ws/'+uuid)}&sni={quote(host)}#{label}"
    return f"vless://{uuid}@{host}:{port_value}"

# ============================================================
# SUBSCRIPTION REMARK TEMPLATE (configurable, Settings -> Subscription Template)
# ============================================================
def build_config_remark(link: dict, uid: str) -> str:
    """می‌سازه چه متنی به‌عنوان نام کانفیگ (#remark) داخل اپ کاربر دیده بشه.
    پیش‌فرض دقیقاً مثل قبل فقط «نام» است؛ مالک پنل از تب تنظیمات می‌تونه
    نمایش حجم/آی‌دی/نام اینباند رو هم فعال کنه."""
    show_name = bool(CONFIG.get("sub_remark_show_name", True))
    show_volume = bool(CONFIG.get("sub_remark_show_volume", False))
    show_id = bool(CONFIG.get("sub_remark_show_id", False))
    show_inbound = bool(CONFIG.get("sub_remark_show_inbound", False))

    name = str(link.get("label") or "Config").strip() or "Config"
    parts: list[str] = []

    if show_name:
        parts.append(name)

    if show_volume:
        try:
            limit_bytes = int(link.get("limit_bytes") or 0)
        except Exception:
            limit_bytes = 0
        parts.append(fmt_bytes(limit_bytes) if limit_bytes > 0 else "Unlimited")

    if show_id:
        parts.append(str(uid)[:8])

    if show_inbound:
        parent_id = link.get("parent_inbound_id")
        parent = LINKS.get(parent_id) if parent_id else None
        inbound_label = str((parent or {}).get("label") or "").strip()
        if inbound_label:
            parts.append(inbound_label)

    return " | ".join(p for p in parts if p) or name


def build_manual_uri(
    link: dict,
    uid: str,
    host: str,
    port_override: int | None = None,
) -> str:
    """ساخت لینک کانفیگ برای حالت پروتکل دستی (Manual) — دقیقاً مثل پنل‌های
    3x-ui/Sanaei: پروتکل پایه + شبکه (Network) + امنیت (Security) + فیلدهای
    دستی (آدرس، پورت، مسیر، هاست هدر، SNI، Reality و ...) هر کدام جدا انتخاب
    می‌شن و لینک نهایی از روی آن‌ها ساخته می‌شود."""

    base_protocol = normalize_base_protocol(link.get("base_protocol"))
    network = normalize_network(link.get("network"))
    security = normalize_security(link.get("security"))

    remark = build_config_remark(link, uid)
    label = quote(remark, safe="")

    fp = (link.get("fingerprint") or DEFAULT_FINGERPRINT).strip().lower()
    if fp not in FINGERPRINTS:
        fp = DEFAULT_FINGERPRINT

    port_value = safe_int(
        port_override if port_override is not None else link.get("port"),
        DEFAULT_PORT, MIN_PORT, MAX_PORT,
    )

    address = (str(link.get("address") or "")).strip() or host
    default_alpn = "h2,http/1.1" if network == "xhttp" else "http/1.1"
    alpn_value = (str(link.get("alpn") or default_alpn)).strip()
    path = (str(link.get("path") or "")).strip() or f"/{network}/{uid}"
    host_header = (str(link.get("host_header") or "")).strip() or address
    sni = (str(link.get("sni") or "")).strip() or address
    flow = (str(link.get("flow") or "")).strip()
    grpc_service = (str(link.get("grpc_service_name") or "")).strip() or uid
    xhttp_mode = normalize_xhttp_mode(link.get("xhttp_mode"))

    q: dict[str, str] = {}
    if base_protocol == "vless":
        q["encryption"] = "none"

    if security == "tls":
        q["security"] = "tls"
        q["sni"] = sni
        q["fp"] = fp
        q["alpn"] = alpn_value
        if link.get("allow_insecure"):
            q["allowInsecure"] = "1"
    elif security == "reality":
        q["security"] = "reality"
        q["sni"] = sni
        q["fp"] = fp
        q["pbk"] = (str(link.get("reality_public_key") or "")).strip()
        q["sid"] = (str(link.get("reality_short_id") or "")).strip()
        q["spx"] = (str(link.get("reality_spider_x") or "")).strip() or "/"
    else:
        q["security"] = "none"

    if network == "ws":
        q["type"] = "ws"
        q["path"] = path
        q["host"] = host_header
    elif network == "grpc":
        q["type"] = "grpc"
        q["serviceName"] = grpc_service
        q["mode"] = (str(link.get("grpc_mode") or "gun")).strip() or "gun"
    elif network == "xhttp":
        q["type"] = "xhttp"
        # این پنل یک سرور XHTTP ساده (packet-up/stream-up) پیاده کرده، نه هسته‌ی
        # کامل Xray-core که بتونه مد "auto" رو واقعاً negotiate کنه. اگر mode
        # واقعاً "auto" بمونه، کلاینت‌های واقعی معمولاً نمی‌تونن با این سرور وصل
        # بشن؛ پس به‌صورت خاموش و امن روی "packet-up" (سازگارترین و پایدارترین
        # مد با این بک‌اند) قفل می‌کنیم تا کانفیگ همیشه واقعاً کار کنه.
        q["mode"] = "packet-up" if xhttp_mode == "auto" else xhttp_mode
        q["path"] = path
        q["host"] = host_header
    else:
        q["type"] = "tcp"
        header_type = (str(link.get("header_type") or "")).strip()
        if header_type:
            q["headerType"] = header_type
        if flow:
            q["flow"] = flow

    if base_protocol == "shadowsocks":
        method = str(link.get("ss_method") or "chacha20-ietf-poly1305").strip()
        password = str(link.get("ss_password") or uid).strip()
        if not method:
            method = "chacha20-ietf-poly1305"
        userinfo = f"{method}:{password}"
        token = base64.urlsafe_b64encode(userinfo.encode()).decode().rstrip("=")
        return f"ss://{token}@{address}:{port_value}#{label}"

    if base_protocol == "vmess":
        raw = {
            "v": "2", "ps": remark, "add": address, "port": port_value, "id": uid,
            "aid": 0, "scy": "auto", "net": network, "type": "none",
            "host": host_header if network in ("ws", "xhttp") else "",
            "path": grpc_service if network == "grpc" else path,
            "tls": security if security != "none" else "",
            "sni": sni, "fp": fp,
        }
        return "vmess://" + base64.b64encode(
            json.dumps(raw, separators=(",", ":"), ensure_ascii=False).encode()
        ).decode()

    scheme = "trojan" if base_protocol == "trojan" else "vless"
    qs = "&".join(f"{k}={quote(str(v), safe=',/')}" for k, v in q.items() if v not in (None, ""))
    return f"{scheme}://{uid}@{address}:{port_value}?{qs}#{label}"


def vless_link_for_link(
    link: dict,
    uid: str,
    host: str,
    port_override: int | None = None,
):
    protocol = normalize_protocol(link.get("protocol", DEFAULT_PROTOCOL))
    if protocol == "manual":
        return build_manual_uri(link, uid, host, port_override=port_override)
    return generate_vless_link(
        uid,
        host,
        remark=str(link.get("label") or "Config"),
        protocol=protocol,
        fingerprint=link.get(
            "fingerprint",
            DEFAULT_FINGERPRINT,
        ),
        alpn=link.get(
            "alpn"
        ),
        port=port_override if port_override is not None else link.get(
            "port",
            DEFAULT_PORT,
        ),
    )


def get_link_info(
    link: dict,
    uid: str,
    host: str,
):
    connected_count = len(unique_ips_for_uuid(uid))
    is_active = is_link_allowed(link)
    limit_b = int(link.get("limit_bytes", 0) or 0)
    used_b = int(link.get("used_bytes", 0) or 0)
    is_expired = is_link_expired(link) or (limit_b > 0 and used_b >= limit_b)
    if not is_active or is_expired:
        status_color = "red"
    elif connected_count > 0:
        status_color = "green"
    else:
        status_color = "gray"
    clean_ips = link.get("clean_ips") or []
    cfg_count = int(link.get("config_count") or 1)
    show_vless = len(clean_ips) <= 1 and cfg_count <= 1
    cat = CATEGORIES.get(str(link.get("category_id") or "0")) or {}
    protocol = normalize_protocol(link.get("protocol"))
    if protocol == "manual":
        display_network = normalize_network(link.get("network"))
        display_security = normalize_security(link.get("security"))
    else:
        display_network, display_security = PROTOCOL_NETWORK_SECURITY.get(
            protocol, ("tcp", "none")
        )
    manual_network = normalize_network(link.get("network"))
    manual_security = normalize_security(link.get("security"))
    manual_mode = normalize_xhttp_mode(link.get("xhttp_mode"))
    manual_live = (
        protocol == "manual"
        and normalize_base_protocol(link.get("base_protocol")) == "vless"
        and (manual_network, manual_security) in manual_live_combos()
        and not (manual_network == "xhttp" and manual_mode == "stream-one")
    )
    if protocol == "manual":
        live_status = "live" if manual_live else "link-only"
    elif protocol in LIVE_PROTOCOLS:
        live_status = "live"
    else:
        live_status = "link-only"
    return {
        "uuid": uid,
        "name": link.get("label", ""),
        "label": link.get("label", ""),
        "protocol": link.get("protocol", DEFAULT_PROTOCOL),
        "protocol_display": protocol_display_label(link),
        "base_protocol": normalize_base_protocol(link.get("base_protocol")),
        "network": display_network,
        "security": display_security,
        "manual_live": manual_live,
        "live_status": live_status,
        "live_reason": ("این پروتکل توسط هسته فعلی سرو می‌شود." if live_status == "live" else "فقط لینک ساخته می‌شود؛ برای اجرای واقعی این ترکیب به Xray-core/Inbound خارجی نیاز است."),
        "address": link.get("address", ""),
        "path": link.get("path", ""),
        "host_header": link.get("host_header", ""),
        "sni": link.get("sni", ""),
        "flow": link.get("flow", ""),
        "grpc_service_name": link.get("grpc_service_name", ""),
        "grpc_mode": link.get("grpc_mode", "gun"),
        "xhttp_mode": normalize_xhttp_mode(link.get("xhttp_mode")),
        "header_type": link.get("header_type", ""),
        "allow_insecure": bool(link.get("allow_insecure", False)),
        "reality_public_key": link.get("reality_public_key", ""),
        "reality_short_id": link.get("reality_short_id", ""),
        "reality_spider_x": link.get("reality_spider_x", "/"),
        "active": is_active,
        "used_bytes": used_b,
        "limit_bytes": limit_b,
        "expires_at": link.get("expires_at"),
        "ip_limit": int(link.get("ip_limit", 0) or 0),
        "speed_limit_bytes": int(link.get("speed_limit_bytes", 0) or 0),
        "connection_limit": int(link.get("connection_limit", 0) or 0),
        "fragment": link.get("fragment", "off"),
        "fingerprint": link.get("fingerprint", DEFAULT_FINGERPRINT),
        "alpn": link.get("alpn", ""),
        "port": link.get("port", DEFAULT_PORT),
        "note": link.get("note", ""),
        "clean_ips": clean_ips,
        "alarm_enabled": bool(link.get("alarm_enabled", False)),
        "category_id": str(link.get("category_id") or "0"),
        "category_number": int(cat.get("number", 0)),
        "category_name": str(cat.get("name", "عمومی")),
        "config_count": cfg_count,
        "client_limit": int(link.get("client_limit") or 0),
        "parent_inbound_id": link.get("parent_inbound_id"),
        "is_client": bool(link.get("parent_inbound_id")),
        "status_color": status_color,
        "connected_ips": connected_count,
        "show_vless": show_vless,
        "vless": vless_link_for_link(link, uid, host) if show_vless else "",
        "vless_full": vless_link_for_link(link, uid, host),
        # همه‌ی کانفیگ‌ها به ازای هر خروجی (برای ساب گروهی روی نودهای دیگر)
        "vless_variants": [
            vless_link_for_link({**vl, "label": f"{vt} | {vl.get('label') or 'Config'}"} if vt else vl, vu, host)
            for vl, vu, vt in expand_outbound_variants(link, uid)
        ],
        "sub": f"{get_scheme()}://{host}/sub/{uid}",
        "info": f"{get_scheme()}://{host}/info/{uid}",
        "support": SUPPORT_USERNAME,
        "outbound_proxy_id": str(link.get("outbound_proxy_id") or ""),
        "outbound": outbound_info(link.get("outbound_proxy_id")),
        "outbound_proxy_ids": link_outbound_ids(link),
        "outbounds": [outbound_info(p) or {"id": "", "name": "Direct", "flag": "🚀", "country": "مستقیم"} for p in link_outbound_ids(link)],
    }


# ============================================================
# PERSISTENCE
# ============================================================

async def load_state():

    global AUTH

    try:

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not DATA_FILE.exists():
            return

        async with aiofiles.open(
            DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            raw = await file.read()

        data = json.loads(raw)

        LINKS.update(
            data.get(
                "links",
                {},
            )
        )

        SUBS.update(
            data.get(
                "subs",
                {},
            )
        )

        CATEGORIES.update(
            data.get(
                "categories",
                {},
            )
        )

        stored_username = data.get("username")
        if isinstance(stored_username, str) and stored_username.strip():
            AUTH["username"] = stored_username.strip()

        stored_password = data.get(
            "password_hash"
        )

        if stored_password:
            AUTH[
                "password_hash"
            ] = stored_password

        ADMINS.update(
            data.get("admins", {})
        )

        ADMIN_REQUESTS.update(
            data.get("admin_requests", {})
        )

        DAILY_STATS.update(
            data.get("daily_stats", {})
        )

        # بازیابی تنظیمات پنل (آدرس عمومی + مشخصات ربات فروش)
        BOT_TEXTS.update(data.get("bot_texts") or {})
        settings_data = data.get("settings") or {}
        if settings_data.get("public_base_url"):
            CONFIG["public_base_url"] = str(settings_data.get("public_base_url") or "").strip()
        if settings_data.get("tcp_public_host"):
            CONFIG["tcp_public_host"] = str(settings_data.get("tcp_public_host") or "").strip()
        if settings_data.get("tcp_public_port"):
            CONFIG["tcp_public_port"] = str(settings_data.get("tcp_public_port") or "").strip()
        CONFIG["bot_auto_start"] = bool(settings_data.get("bot_auto_start", False))
        if "sales_enabled" in settings_data:
            CONFIG["sales_enabled"] = bool(settings_data.get("sales_enabled"))
        if "name_style_enabled" in settings_data:
            CONFIG["name_style_enabled"] = bool(settings_data.get("name_style_enabled"))
        try:
            import telegram_bot
            telegram_bot.configure(
                token=settings_data.get("bot_token"),
                admin_ids_raw=settings_data.get("bot_admin_ids"),
            )
        except Exception as exc:
            logger.warning("Could not restore bot settings: %s", exc)

        # Compatibility for older records
        for uid, link in LINKS.items():

            link.setdefault(
                "protocol",
                DEFAULT_PROTOCOL,
            )

            link.setdefault(
                "fingerprint",
                DEFAULT_FINGERPRINT,
            )

            link.setdefault(
                "alpn",
                "",
            )

            link.setdefault(
                "port",
                DEFAULT_PORT,
            )

            link.setdefault(
                "ip_limit",
                0,
            )

            link.setdefault(
                "speed_limit_bytes",
                0,
            )

            link.setdefault(
                "connection_limit",
                0,
            )

            link.setdefault(
                "fragment",
                "off",
            )

            link.setdefault(
                "used_bytes",
                0,
            )
            link.setdefault("clean_ips", [])
            link.setdefault("alarm_enabled", False)
            link.setdefault("category_id", "0")
            link.setdefault("config_count", 1)
            link.setdefault("client_limit", 0)
            link.setdefault("usage_history", [])
            link.setdefault("parent_inbound_id", None)

        logger.info(
            "State loaded: %d links / %d subscriptions",
            len(LINKS),
            len(SUBS),
        )

    except Exception as exc:

        logger.exception(
            "Could not load state: %s",
            exc,
        )


async def save_state():

    try:
        rebuild_variant_index()
    except Exception:
        pass

    async with SAVE_LOCK:

        try:

            DATA_DIR.mkdir(
                parents=True,
                exist_ok=True,
            )

            payload = {
                "links":
                    dict(LINKS),

                "subs":
                    dict(SUBS),

                "categories":
                    dict(CATEGORIES),

                "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),

                "password_hash":
                    AUTH[
                        "password_hash"
                    ],

                "admins":
                    dict(ADMINS),

                "admin_requests":
                    dict(ADMIN_REQUESTS),

                "daily_stats":
                    dict(DAILY_STATS),

                # تنظیمات پنل: آدرس عمومی + مشخصات ربات فروش (برای اینکه با ری‌استارت
                # سرویس از دست نرن و نیازی به .env دستی نباشه).
                "bot_texts": BOT_TEXTS,
                "settings": {
                    "public_base_url": CONFIG.get("public_base_url", ""),
                    "tcp_public_host": CONFIG.get("tcp_public_host", ""),
                    "tcp_public_port": CONFIG.get("tcp_public_port", ""),
                    "bot_token": _bot_settings_snapshot().get("bot_token", ""),
                    "bot_admin_ids": _bot_settings_snapshot().get("admin_ids", ""),
                    "bot_auto_start": bool(CONFIG.get("bot_auto_start", False)),
                    "sales_enabled": bool(CONFIG.get("sales_enabled", SALES_ENABLED)),
                    "name_style_enabled": bool(CONFIG.get("name_style_enabled", True)),
                },

                "saved_at":
                    datetime.now().isoformat(),
            }

            temp_file = (
                DATA_FILE.with_suffix(
                    ".tmp"
                )
            )

            async with aiofiles.open(
                temp_file,
                "w",
                encoding="utf-8",
            ) as file:

                await file.write(
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        indent=2,
                    )
                )

            temp_file.replace(
                DATA_FILE
            )

        except Exception as exc:

            logger.exception(
                "Could not save state: %s",
                exc,
            )


# ============================================================
# DEFAULT LINK
# ============================================================

_default_link_created = False



async def ensure_default_categories():
    if CATEGORIES:
        return
    CATEGORIES["0"] = {
        "id": "0", "name": "عمومی", "number": 0,
        "limit_bytes": 0, "expires_days": 0, "connection_limit": 0,
        "speed_limit_bytes": 0, "ip_limit": 0, "clean_ips": [],
        "random_name": False, "single_user": False,
        "created_at": datetime.now().isoformat(),
    }
    CATEGORIES["1"] = {
        "id": "1", "name": "VIP", "number": 1,
        "limit_bytes": 0, "expires_days": 0, "connection_limit": 1,
        "speed_limit_bytes": 0, "ip_limit": 1, "clean_ips": [],
        "random_name": False, "single_user": True,
        "created_at": datetime.now().isoformat(),
    }
    asyncio.create_task(save_state())

async def ensure_default_link():

    global _default_link_created

    if _default_link_created:
        return

    async with LINKS_LOCK:

        if not any(
            item.get("is_default")
            for item in LINKS.values()
        ):

            digest = hashlib.sha256(
                (
                    "default"
                    + SECRET_KEY
                ).encode("utf-8")
            ).hexdigest()

            uid = (
                f"{digest[:8]}-"
                f"{digest[8:12]}-"
                f"{digest[12:16]}-"
                f"{digest[16:20]}-"
                f"{digest[20:32]}"
            )

            LINKS[uid] = {
                "label":
                    "لینک پیش‌فرض",

                "limit_bytes":
                    0,

                "used_bytes":
                    0,

                "created_at":
                    datetime.now().isoformat(),

                "active":
                    True,

                "expires_at":
                    None,

                "note":
                    "",

                "is_default":
                    True,

                "sub_id":
                    None,

                "protocol":
                    DEFAULT_PROTOCOL,

                "fingerprint":
                    DEFAULT_FINGERPRINT,

                "alpn":
                    "http/1.1",

                "port":
                    DEFAULT_PORT,

                "ip_limit":
                    0,

                "speed_limit_bytes":
                    DEFAULT_SPEED_LIMIT,

                "connection_limit":
                    0,

                "fragment":
                    "off",
            }

            asyncio.create_task(
                save_state()
            )

    _default_link_created = True


# ============================================================
# LINK MANAGEMENT
# ============================================================

# ============================================================
# اسم‌های تزئینی (استایل خودکار نام کانفیگ): FaultPass → FaultPass | Aurora 🌠
# ============================================================
COOL_WORDS = [
    "Kooh", "Darya", "Mahtab", "Kahkeshan", "Tir", "Bahman", "Sepand", "Azar", "Nasim", "Rakhsh",
    "Shabdiz", "Gordafarid", "Esfandiar", "Bijan", "Zal", "Anahita", "Mehr", "Khazar", "Sahand", "Sabalan",
    "Golestan", "Persepolis", "Shiraz", "Tabriz", "Hoor", "Tahmineh",
    "Aurora", "Eclipse", "Meteor", "Galaxy", "Stellar", "Lunar", "Solar", "Horizon", "Summit", "Glacier",
    "Cobalt", "Onyx", "Obsidian", "Crimson", "Emerald", "Sapphire", "Jaguar", "Lynx", "Hawk", "Cobra",
    "Mustang", "Spectre", "Echo", "Flux", "Prism", "Radiant",
]
COOL_EMOJIS = [
    "🌠", "🌈", "🍀", "🌊", "⛰️", "🏔️", "🌅", "🌟", "🪽", "🦄", "🐆", "🦈", "🐬", "🦉", "🐎", "🗡️",
    "🏆", "🎖️", "💥", "🌸", "🌺", "🍁", "❄️", "☀️", "🌤️", "🧭", "🗺️", "📡", "🔋", "🎮", "🕹️", "🏁",
    "🚩", "🪄", "🎐", "🫧",
]
COOL_STYLES = [
    "{base} | {word} {emoji}",
    "{emoji} {word} ⌁ {base}",
    "{base} ❖ {word}{emoji}",
    "{base} ⦗{word}⦘ {emoji}",
    "{base} » {word} {emoji}{emoji2}",
    "{emoji}{base}•{word}",
    "『{base}』 {word} {emoji}",
    "{base} ⚑ {word}",
]
DEFAULT_BRAND_NAME = "FaultPass"


def name_style_on() -> bool:
    return bool(CONFIG.get("name_style_enabled", True))


def sanitize_display_name(name: str, fallback: str = DEFAULT_BRAND_NAME) -> str:
    """اسمی که کاربر برای نمایش در کلاینت می‌نویسد (فارسی/انگلیسی/اموجی/فاصله) دست‌نخورده
    می‌ماند؛ فقط کاراکترهای کنترلی/خط‌جدید حذف و طولش محدود می‌شود."""
    cleaned = "".join(ch for ch in str(name or "") if ch.isprintable()).strip()
    return cleaned[:40] if cleaned else fallback


def is_name_styled(name: str) -> bool:
    """اگر کاربر خودش اسم را تزئین کرده باشد (| یا اموجی/نماد)، دیگر دست نمی‌زنیم."""
    text = str(name or "")
    return "|" in text or any(ord(ch) >= 0x2190 for ch in text)


def style_config_name(base: str, index: int | None = None, style: int | None = None) -> str:
    base = "".join(ch for ch in str(base or "") if ch.isprintable()).strip()[:32] or DEFAULT_BRAND_NAME
    rnd = secrets.SystemRandom()
    if index is None:
        word, emoji, emoji2 = rnd.choice(COOL_WORDS), rnd.choice(COOL_EMOJIS), rnd.choice(COOL_EMOJIS)
    else:
        word = COOL_WORDS[index % len(COOL_WORDS)]
        emoji = COOL_EMOJIS[(index * 5 + 1) % len(COOL_EMOJIS)]
        emoji2 = COOL_EMOJIS[(index * 5 + 9) % len(COOL_EMOJIS)]
    tpl = COOL_STYLES[(style or 0) % len(COOL_STYLES)]
    return tpl.format(base=base, word=word, emoji=emoji, emoji2=emoji2)[:60]


def decorate_label(base: str, index: int | None = None) -> str:
    """اعمال استایل خودکار روی اسم (اگر از تنظیمات فعال باشد و اسم تزئین‌نشده باشد)."""
    if name_style_on() and not is_name_styled(base):
        return style_config_name(base, index=index)
    return base


def auto_display_name() -> str:
    """اسم خودکار خفن برای وقتی که کاربر چیزی ننوشته."""
    if name_style_on():
        return style_config_name(DEFAULT_BRAND_NAME)
    return auto_config_name()


def name_suggestions(base: str, count: int = 12) -> list:
    base = sanitize_display_name(base, DEFAULT_BRAND_NAME)
    rnd = secrets.SystemRandom()
    words = rnd.sample(COOL_WORDS, min(count, len(COOL_WORDS)))
    out = []
    for i, word in enumerate(words):
        tpl = COOL_STYLES[0] if i < 4 else COOL_STYLES[i % len(COOL_STYLES)]
        out.append(tpl.format(base=base[:32], word=word, emoji=rnd.choice(COOL_EMOJIS), emoji2=rnd.choice(COOL_EMOJIS))[:60])
    return out


def clean_outbound_proxy_id(value) -> str:
    """'' = مستقیم (خودِ سرور پنل). غیرخالی باید شناسه‌ی یک پراکسی موجود باشه."""
    pid = str(value or "").strip()
    if not pid:
        return ""
    try:
        from outbound_proxy import get_proxy
    except Exception:
        raise HTTPException(status_code=400, detail="ماژول پراکسی خروجی در دسترس نیست")
    if not get_proxy(pid):
        raise HTTPException(status_code=400, detail="پراکسی انتخاب‌شده پیدا نشد (شاید حذف شده)")
    return pid


def clean_outbound_proxy_ids(values) -> list:
    """لیست چندخروجی: هر عضو '' (مستقیم) یا شناسه‌ی پراکسی معتبر. تکراری‌ها حذف می‌شوند."""
    if values is None:
        return [""]
    if not isinstance(values, (list, tuple)):
        values = [values]
    out = []
    for v in values:
        pid = clean_outbound_proxy_id(v)
        if pid not in out:
            out.append(pid)
    return (out or [""])[:30]


def link_outbound_ids(link: dict | None) -> list:
    """همه‌ی خروجی‌های یک کانفیگ. اولی = خروجی UUID اصلی، بقیه = UUIDهای مجازی (variant)."""
    link = link or {}
    ids = link.get("outbound_proxy_ids")
    if not isinstance(ids, list) or not ids:
        ids = [str(link.get("outbound_proxy_id") or "")]
    out = []
    for v in ids:
        v = str(v or "")
        if v not in out:
            out.append(v)
    return out or [""]


def set_link_outbounds(link: dict, ids: list):
    ids = list(ids or [""])
    link["outbound_proxy_ids"] = ids
    link["outbound_proxy_id"] = ids[0]


def outbound_variant_uuid(base_uid: str, proxy_id: str) -> str:
    """UUID ثابت و قطعی برای «کانفیگ X از خروجی Y». با تغییر ترتیب/ری‌استارت عوض نمی‌شود."""
    import uuid as _uuid
    try:
        ns = _uuid.UUID(str(base_uid))
    except Exception:
        ns = _uuid.NAMESPACE_URL
    return str(_uuid.uuid5(ns, "fp-outbound:" + (proxy_id or "direct")))


_VARIANT_INDEX: dict = {}
_VARIANT_INDEX_AT = 0.0


def rebuild_variant_index():
    global _VARIANT_INDEX_AT
    idx = {}
    for uid, link in list(LINKS.items()):
        ids = link_outbound_ids(link)
        for pid in ids[1:]:
            idx[outbound_variant_uuid(uid, pid)] = (uid, pid)
    _VARIANT_INDEX.clear()
    _VARIANT_INDEX.update(idx)
    _VARIANT_INDEX_AT = time.monotonic()


def resolve_link_uuid(uid: str):
    """UUID ورودی ریله → (UUID اصلی، شناسه‌ی خروجی یا None).
    None یعنی همان خروجی پیش‌فرض کانفیگ. حجم/IP/انقضا همیشه روی UUID اصلی حساب می‌شود."""
    uid = str(uid or "")
    if uid in LINKS:
        return uid, None
    hit = _VARIANT_INDEX.get(uid)
    if hit is None and time.monotonic() - _VARIANT_INDEX_AT > 2.0:
        rebuild_variant_index()
        hit = _VARIANT_INDEX.get(uid)
    if hit is None:
        return uid, None
    base, pid = hit
    if pid not in link_outbound_ids(LINKS.get(base)):
        return uid, None
    return base, pid


def with_outbound(link: dict | None, proxy_id):
    if link is None or proxy_id is None:
        return link
    return {**link, "outbound_proxy_id": proxy_id}


def outbound_tag(proxy_id: str) -> str:
    info = outbound_info(proxy_id)
    if not info:
        return "🚀 Direct"
    flag = info.get("flag") or ""
    name = info.get("country") or info.get("name") or "Proxy"
    return f"{flag} {name}".strip()


def expand_outbound_variants(link: dict, uid: str) -> list:
    """هر کانفیگ → یک آیتم به ازای هر خروجی: (link_dict, uuid_برای_لینک, برچسب_لوکیشن).
    با یک خروجی، رفتار قبلی دقیقاً حفظ می‌شود (برچسب خالی)."""
    ids = link_outbound_ids(link)
    if len(ids) <= 1:
        return [(link, uid, "")]
    out = []
    for i, pid in enumerate(ids):
        vuid = uid if i == 0 else outbound_variant_uuid(uid, pid)
        out.append(({**link, "outbound_proxy_id": pid}, vuid, outbound_tag(pid)))
    return out


def outbound_info(value):
    """خلاصه‌ی نام/کشور/پرچم پراکسی خروجی برای نمایش در پنل (None = مستقیم)."""
    pid = str(value or "").strip()
    if not pid:
        return None
    try:
        from outbound_proxy import proxy_summary
        return proxy_summary(pid)
    except Exception:
        return None


def public_remote_links(entries: list) -> list:
    """نسخه‌ی امن یک لیست عضو ریموت برای پنل (بدون خودِ رشته‌ی vless)."""
    try:
        from nodes import get_node
    except Exception:
        get_node = lambda _id: None
    out = []
    for e in entries:
        node = get_node(e.get("node_id") or "")
        out.append({
            "id": f"{e.get('node_id')}:{e.get('uuid')}",
            "node_id": e.get("node_id"),
            "node_name": (node or {}).get("name") or "نود حذف‌شده",
            "node_online": bool(node),
            "node_missing": bool(e.get("node_missing")),
            "uuid": e.get("uuid"),
            "label": e.get("label", ""),
            "protocol_display": e.get("protocol_display", ""),
            "active": bool(e.get("active", True)),
            "last_error": e.get("last_error", ""),
            "last_synced_at": e.get("last_synced_at"),
            "added_at": e.get("added_at"),
        })
    return out


async def make_link(
    label: str = "لینک جدید",
    limit_bytes: int = 0,
    expires_at: str | None = None,
    note: str = "",
    sub_id: str | None = None,
    protocol: str = DEFAULT_PROTOCOL,
    fingerprint: str = DEFAULT_FINGERPRINT,
    alpn: str = "",
    port: int = DEFAULT_PORT,
    ip_limit: int = 0,
    speed_limit_bytes: int = 0,
    connection_limit: int = 0,
    fragment: str = "off",
    clean_ips=None,
    alarm_enabled: bool = False,
    category_id: str = "0",
    config_count: int = 1,
    manual_fields: dict | None = None,
    outbound_proxy_id: str = "",
    outbound_proxy_ids: list | None = None,
):

    protocol = normalize_protocol(protocol)
    manual_fields = manual_fields or {}

    fingerprint = (
        fingerprint
        or DEFAULT_FINGERPRINT
    ).strip().lower()

    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT

    if not (
        MIN_PORT
        <= port
        <= MAX_PORT
    ):
        port = DEFAULT_PORT

    uid = generate_uuid()

    record = {
        "label":
            sanitize_config_name((label or "").strip() or random_config_name()),

        "limit_bytes":
            max(
                0,
                int(limit_bytes),
            ),

        "used_bytes":
            0,

        "created_at":
            datetime.now().isoformat(),

        "active":
            True,

        "expires_at":
            expires_at,

        "note":
            (
                note
                or ""
            ).strip()[:500],

        "is_default":
            False,

        "sub_id":
            sub_id,

        # A child client is a real live credential: it owns its own UUID and is
        # therefore accepted by the VLESS/XHTTP relay exactly like the parent.
        "parent_inbound_id": None,

        "protocol":
            protocol,

        "fingerprint":
            fingerprint,

        "alpn":
            (
                alpn
                or ""
            ).strip()[:100],

        "port":
            port,

        "ip_limit":
            max(
                0,
                int(ip_limit),
            ),

        "speed_limit_bytes":
            max(
                0,
                int(speed_limit_bytes),
            ),

        "connection_limit":
            max(
                0,
                int(connection_limit),
            ),

        "fragment":
            (
                fragment
                or "off"
            ).strip().lower(),

        "security_profile": "balanced",
        "multi_login": False,
        "clean_ips": list(clean_ips or []),
        "alarm_enabled": bool(alarm_enabled),
        "category_id": str(category_id or "0"),
        "config_count": max(1, min(40, int(config_count or 1))),
        "client_limit": 0,
        "usage_history": [],
        # مسیر خروجی: خالی = مستقیم از روی خود سرور. غیرخالی = شناسه‌ی یک پراکسی
        # (SOCKS5/SOCKS4/HTTP) از outbound_proxy.py که ارتباط با مقصد از طریق اون رد می‌شه.
        "outbound_proxy_id": str(outbound_proxy_id or "").strip(),
        # چندخروجی: هر خروجی در ساب یک کانفیگ جدا (مثلاً فرانسه/آلمان/هلند) می‌سازد
        "outbound_proxy_ids": list(outbound_proxy_ids) if outbound_proxy_ids else [str(outbound_proxy_id or "").strip()],
    }

    if protocol == "manual":
        record.update({
            "base_protocol": normalize_base_protocol(manual_fields.get("base_protocol")),
            "network": normalize_network(manual_fields.get("network")),
            "security": normalize_security(manual_fields.get("security")),
            "address": str(manual_fields.get("address") or "").strip()[:255],
            "path": str(manual_fields.get("path") or "").strip()[:255],
            "host_header": str(manual_fields.get("host_header") or "").strip()[:255],
            "sni": str(manual_fields.get("sni") or "").strip()[:255],
            "flow": str(manual_fields.get("flow") or "").strip()[:64],
            "grpc_service_name": str(manual_fields.get("grpc_service_name") or "").strip()[:128],
            "grpc_mode": str(manual_fields.get("grpc_mode") or "gun").strip()[:32] or "gun",
            "xhttp_mode": normalize_xhttp_mode(manual_fields.get("xhttp_mode")),
            "header_type": str(manual_fields.get("header_type") or "").strip()[:32],
            "allow_insecure": bool(manual_fields.get("allow_insecure", False)),
            "reality_public_key": str(manual_fields.get("reality_public_key") or "").strip()[:128],
            "reality_short_id": str(manual_fields.get("reality_short_id") or "").strip()[:32],
            "reality_spider_x": str(manual_fields.get("reality_spider_x") or "/").strip()[:128] or "/",
            "ss_method": str(manual_fields.get("ss_method") or "chacha20-ietf-poly1305").strip()[:80],
            "ss_password": str(manual_fields.get("ss_password") or uid).strip()[:255],
        })

    record["protocol_label"] = protocol_display_label(record)

    async with LINKS_LOCK:
        LINKS[uid] = record

    bump_daily_stat("new_links")

    if sub_id:

        async with SUBS_LOCK:

            if sub_id in SUBS:

                ids = SUBS[
                    sub_id
                ].setdefault(
                    "link_ids",
                    [],
                )

                if uid not in ids:
                    ids.append(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{record['label']}» "
            f"ساخته شد"
        ),
        "ok",
    )

    return uid, record


async def remove_link(
    uid: str,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return None

        label = LINKS[
            uid
        ].get(
            "label",
            uid,
        )

        sub_id = LINKS[
            uid
        ].get(
            "sub_id"
        )

        del LINKS[uid]

    if sub_id:

        async with SUBS_LOCK:

            if sub_id in SUBS:

                ids = SUBS[
                    sub_id
                ].get(
                    "link_ids",
                    [],
                )

                if uid in ids:
                    ids.remove(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"حذف شد"
        ),
        "warn",
    )

    return label


async def set_link_active(
    uid: str,
    active: bool,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return None

        LINKS[
            uid
        ][
            "active"
        ] = bool(active)

        record = LINKS[uid]

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{record['label']}» "
            f"{'فعال' if active else 'غیرفعال'} شد"
        ),
        "ok"
        if active
        else "warn",
    )

    return record


# ============================================================
# SUB GROUPS
# ============================================================

async def create_sub_group(
    name: str = "گروه جدید",
    desc: str = "",
    password: str = "",
):

    name = (
        name
        or "گروه جدید"
    ).strip()[:60]

    desc = (
        desc
        or ""
    ).strip()[:200]

    password = (
        password
        or ""
    ).strip()

    sub_id = generate_uuid()

    uuid_key = secrets.token_urlsafe(16)

    record = {
        "name":
            name,

        "desc":
            desc,

        "password_hash":
            (
                hash_password(password)
                if password
                else None
            ),

        "uuid_key":
            uuid_key,

        "created_at":
            datetime.now().isoformat(),

        "link_ids":
            [],

        "remote_links":
            [],
    }

    async with SUBS_LOCK:
        SUBS[sub_id] = record

    await save_state()

    log_activity(
        "sub",
        (
            f"گروه "
            f"«{name}» "
            f"ساخته شد"
        ),
        "ok",
    )

    return (
        sub_id,
        record,
    )


async def set_link_sub(
    uid: str,
    sub_id: str | None,
):

    async with LINKS_LOCK:

        if uid not in LINKS:
            return False

        old_sub = LINKS[
            uid
        ].get(
            "sub_id"
        )

        label = LINKS[
            uid
        ].get(
            "label",
            uid,
        )

    if sub_id is not None:

        async with SUBS_LOCK:

            if sub_id not in SUBS:
                return False

    async with SUBS_LOCK:

        if (
            old_sub
            and old_sub in SUBS
        ):

            ids = SUBS[
                old_sub
            ].get(
                "link_ids",
                [],
            )

            if uid in ids:
                ids.remove(uid)

        if (
            sub_id
            and sub_id in SUBS
        ):

            ids = SUBS[
                sub_id
            ].setdefault(
                "link_ids",
                [],
            )

            if uid not in ids:
                ids.append(uid)

    async with LINKS_LOCK:

        if uid in LINKS:

            LINKS[
                uid
            ][
                "sub_id"
            ] = sub_id

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"{'به گروه اضافه شد' if sub_id else 'از گروه خارج شد'}"
        ),
        "info",
    )

    return True


async def remove_sub_group(
    sub_id: str,
):

    async with SUBS_LOCK:

        if sub_id not in SUBS:
            return None

        name = SUBS[
            sub_id
        ].get(
            "name",
            sub_id,
        )

        del SUBS[sub_id]

    async with LINKS_LOCK:

        for link in LINKS.values():

            if (
                link.get("sub_id")
                == sub_id
            ):
                link["sub_id"] = None

    await save_state()

    log_activity(
        "sub",
        (
            f"گروه "
            f"«{name}» "
            f"حذف شد"
        ),
        "warn",
    )

    return name


async def usage_history_loop():
    """Persist live usage history periodically so the customer graph survives restarts.
    همچنین: کانفیگ‌هایی که ۷ روز از رسیدنشون به ۱۰۰٪ مصرف گذشته و هنوز خاموش
    نشدن رو خودکار غیرفعال می‌کنه."""
    while True:
        try:
            await asyncio.sleep(60)
            now = now_ir()
            ts = now.replace(second=0, microsecond=0).isoformat()
            changed = False
            auto_disabled = []
            async with LINKS_LOCK:
                for uid, link in LINKS.items():
                    history = link.setdefault("usage_history", [])
                    used = int(link.get("used_bytes", 0) or 0)
                    limit = int(link.get("limit_bytes", 0) or 0)
                    if history and str(history[-1].get("ts", ""))[:16] == ts[:16]:
                        if history[-1].get("used") != used or history[-1].get("limit") != limit:
                            history[-1]["used"] = used
                            history[-1]["limit"] = limit
                            changed = True
                    else:
                        history.append({"ts": ts, "used": used, "limit": limit})
                        if len(history) > 144:
                            del history[:-144]
                        changed = True

                    exhausted_at = link.get("quota_exhausted_at")
                    if exhausted_at:
                        if limit <= 0 or used < limit:
                            # حجم افزایش پیدا کرده یا ریست شده؛ دیگه تمام‌شده حساب نمیشه
                            link.pop("quota_exhausted_at", None)
                            changed = True
                        elif link.get("active", True):
                            try:
                                exhausted_dt = datetime.fromisoformat(str(exhausted_at))
                            except Exception:
                                exhausted_dt = datetime.now()
                            if datetime.now() - exhausted_dt >= timedelta(days=7):
                                link["active"] = False
                                auto_disabled.append(str(link.get("label") or uid[:8]))
                                changed = True
            if changed:
                await save_state()
            for name in auto_disabled:
                log_activity("link", f"کانفیگ «{name}» چون ۷ روز از تمام‌شدن حجمش گذشته بود، خودکار غیرفعال شد", "warn")
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning("Usage history loop error: %s", exc)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup():

    global http_client, USAGE_PERSIST_TASK

    limits = httpx.Limits(
        max_connections=500,
        max_keepalive_connections=100,
    )

    timeout = httpx.Timeout(
        30.0,
        connect=10.0,
    )

    http_client = httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        follow_redirects=True,
    )

    await load_state()

    USAGE_PERSIST_TASK = asyncio.create_task(usage_history_loop())

    await ensure_default_categories()
    await ensure_default_link()

    log_activity(
        "system",
        (
            f"{APP_NAME} "
            f"v{APP_VERSION} "
            f"راه‌اندازی شد"
        ),
        "ok",
    )

    logger.info(
        "%s v%s started on 0.0.0.0:%s",
        APP_NAME,
        APP_VERSION,
        PORT,
    )

    logger.info(
        "Data directory: %s",
        DATA_DIR,
    )

    try:
        import tcp_relay
        await tcp_relay.start_tcp_relay(app_logger=logger)
    except Exception as exc:
        logger.warning("VLESS-TCP relay startup skipped: %s", exc)


@app.on_event("shutdown")
async def shutdown():

    global USAGE_PERSIST_TASK
    if USAGE_PERSIST_TASK:
        USAGE_PERSIST_TASK.cancel()
        try:
            await USAGE_PERSIST_TASK
        except asyncio.CancelledError:
            pass
        USAGE_PERSIST_TASK = None

    await save_state()

    if http_client:
        await http_client.aclose()

    try:
        import tcp_relay
        await tcp_relay.stop_tcp_relay()
    except Exception:
        pass


# ============================================================
# LANDING
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # The old public landing/interstitial page has been removed.
    # Visitors go straight to the real login page; authenticated users go to the dashboard.
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse("/dashboard")
    return RedirectResponse("/login")



# ============================================================
# FAULTPASS STORE / SUBSCRIPTION PLANS
# ============================================================
# Plan data now lives in sales.py (persisted to faultpass_plans.json)
# and is fully editable from the "مدیریت پلن‌ها" tab in the dashboard.
# This page is rendered fresh on every request so edits show up instantly.

def _store_plan_cards(plans):
    cards = []
    for plan in plans:
        cards.append(f"""
        <article class="plan-card {'featured' if plan.get('featured') else ''}">
          <div class="plan-badge">{escape_html(plan.get('badge') or '')}</div>
          <div class="plan-name">{escape_html(plan.get('name',''))}</div>
          <div class="plan-price"><strong>{plan.get('stars',0)}</strong><span> Stars</span></div>
          <ul>
            <li>اعتبار {plan.get('days',0)} روزه</li>
            <li>{plan.get('volume_gb',0)}GB ترافیک</li>
            <li>تا {plan.get('speed_mbps',0)}Mbps</li>
            <li>{plan.get('ip_limit',0)} کاربر هم‌زمان</li>
            <li>لینک سابسکریپشن اختصاصی</li>
          </ul>
          <a class="buy-btn" href="https://t.me/{escape_html(os.environ.get('TELEGRAM_BOT_USERNAME','FaultPassBot'))}?start=buy_{escape_html(plan.get('id',''))}">خرید از ربات فروش</a>
        </article>
        """)
    return "\n".join(cards)

def _store_html(plans):
    return """<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FaultPass — فروش اشتراک</title>
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;font-family:Vazirmatn,Tahoma,Arial,sans-serif;color:#eef2ff;background:#070a12;
background-image:radial-gradient(circle at 15% 15%,rgba(37,99,235,.18),transparent 30%),radial-gradient(circle at 85% 20%,rgba(14,165,233,.15),transparent 30%),linear-gradient(145deg,#070a12,#0b1020 55%,#060810)}
.wrap{width:min(1120px,92%);margin:auto;padding:54px 0 70px}.hero{text-align:center;margin-bottom:38px}.logo{display:inline-flex;width:64px;height:64px;border-radius:20px;align-items:center;justify-content:center;overflow:hidden;background:#0b1020;box-shadow:0 20px 60px rgba(30,58,138,.35)}
h1{font-size:clamp(34px,6vw,64px);margin:18px 0 8px;letter-spacing:-2px}.sub{color:#9ca8c7;max-width:700px;margin:auto;line-height:1.9}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:34px}.plan-card{position:relative;padding:28px;border:1px solid rgba(255,255,255,.09);border-radius:28px;background:rgba(15,23,42,.86);backdrop-filter:blur(10px);box-shadow:0 25px 80px rgba(0,0,0,.25);transition:.25s;contain:layout style paint}.plan-card:hover{transform:translateY(-5px);border-color:rgba(129,140,248,.4)}.featured{border-color:rgba(37,99,235,.55);box-shadow:0 25px 90px rgba(79,70,229,.16)}.plan-badge{display:inline-block;font-size:12px;padding:7px 10px;border-radius:999px;background:rgba(37,99,235,.13);color:#b7c2ff}.plan-name{font-size:24px;font-weight:900;margin:18px 0 8px}.plan-price strong{font-size:42px}.plan-price span{color:#94a3b8}ul{padding:0;list-style:none;line-height:2.2;color:#cbd5e1;min-height:150px}.buy-btn{display:block;text-align:center;text-decoration:none;color:white;font-weight:800;padding:13px 16px;border-radius:15px;background:linear-gradient(135deg,#2563eb,#06b6d4)}.note{margin-top:26px;padding:16px;border-radius:18px;background:rgba(255,255,255,.035);color:#8fa0bf;text-align:center;font-size:13px}@media(max-width:800px){.grid{grid-template-columns:1fr}.wrap{padding-top:32px}}@media(max-width:800px),(pointer:coarse){.plan-card{backdrop-filter:none!important;-webkit-backdrop-filter:none!important;background:rgba(15,23,42,.96)}}
</style></head><body><main class="wrap"><section class="hero"><div class="logo"><img src="data:image/png;base64,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" alt="FaultPass" style="width:100%;height:100%;object-fit:contain;border-radius:inherit"></div><h1>FaultPass Store</h1><p class="sub">خرید سریع، تحویل خودکار و سابسکریپشن اختصاصی. پرداخت از طریق ربات فروش انجام می‌شود و بعد از پرداخت، لینک شما به‌صورت خودکار ساخته خواهد شد.</p></section><section class="grid">""" + _store_plan_cards(plans) + """</section><div class="note">پرداخت و تحویل توسط ربات رسمی FaultPass انجام می‌شود. برای فعال‌سازی ربات، TELEGRAM_BOT_TOKEN و درگاه/Stars را تنظیم کنید.</div></main></body></html>"""

@app.get("/plans", response_class=HTMLResponse)
async def public_plans():
    if not sales_enabled_now():
        return HTMLResponse("""<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FaultPass · Future Release</title><style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#070b13;color:#f5f7fb;font-family:Tahoma,Arial,sans-serif}.box{width:min(560px,calc(100% - 36px));padding:42px 28px;text-align:center;border:1px solid rgba(255,255,255,.1);border-radius:28px;background:linear-gradient(145deg,#0d1320,#111a2a);box-shadow:0 30px 90px rgba(0,0,0,.35)}.ico{width:72px;height:72px;margin:0 auto 18px;display:grid;place-items:center;border-radius:22px;background:rgba(59,130,246,.15);font-size:30px}.muted{color:#9aa7bc;line-height:2;font-size:13px}.tag{display:inline-block;margin-top:18px;padding:8px 13px;border-radius:999px;background:rgba(53,214,255,.08);border:1px solid rgba(53,214,255,.2);color:#64dcff;font-size:11px}</style></head><body><main class="box"><div class="ico">🔒</div><h1>فروش اشتراک موقتاً غیرفعال است</h1><p class="muted">ماژول فروش و پلن‌ها در نسخه فعلی FaultPass فعال نیست. این قابلیت پس از تکمیل و تست نهایی در نسخه‌های بعدی منتشر خواهد شد.</p><span class="tag">FaultPass · Future Release</span></main></body></html>""".replace("</head>", __import__("untitled_ui").css("public") + "</head>"))
    import sales
    return HTMLResponse(_uui(_store_html(sales.list_plans()), "public"))

# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": APP_NAME,
        "version": APP_VERSION,
        "connections": len(connections),
        "uptime": uptime(),
    }


# ============================================================
# LIVE TELEMETRY
# ============================================================

@app.get("/api/telemetry")
async def api_telemetry(_=Depends(require_auth)):
    """Lightweight live server metrics for the dashboard."""
    global _telemetry_prev
    now = time.time()
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage(str(DATA_DIR))
    cpu = psutil.cpu_percent(interval=None)
    load = None
    try:
        load = [round(x, 2) for x in os.getloadavg()]
    except Exception:
        load = []
    net = psutil.net_io_counters()
    async with _telemetry_lock:
        prev = _telemetry_prev
        dt = max(0.25, now - float(prev.get("ts", now)))
        rx_rate = max(0, net.bytes_recv - int(prev.get("rx", net.bytes_recv))) / dt
        tx_rate = max(0, net.bytes_sent - int(prev.get("tx", net.bytes_sent))) / dt
        _telemetry_prev = {"ts": now, "rx": net.bytes_recv, "tx": net.bytes_sent}
    process = psutil.Process(os.getpid())
    sample = {
        "ts": datetime.now().isoformat(),
        "cpu": _pct(cpu),
        "ram": _pct(vm.percent),
        "swap": _pct(swap.percent),
        "storage": _pct(disk.percent),
        "rx_bps": int(rx_rate),
        "tx_bps": int(tx_rate),
        "connections": len(connections),
    }
    TELEMETRY_HISTORY.append(sample)
    return {
        "ok": True,
        "cpu": _pct(cpu),
        "cpu_cores": psutil.cpu_count(logical=True) or 1,
        "ram": {"percent": _pct(vm.percent), "used": vm.used, "total": vm.total},
        "swap": {"percent": _pct(swap.percent), "used": swap.used, "total": swap.total},
        "storage": {"percent": _pct(disk.percent), "used": disk.used, "total": disk.total},
        "network": {"rx_bps": int(rx_rate), "tx_bps": int(tx_rate), "bytes_recv": int(net.bytes_recv), "bytes_sent": int(net.bytes_sent)},
        "connections": len(connections),
        "traffic_bytes": int(stats.get("total_bytes", 0)),
        "requests": int(stats.get("total_requests", 0)),
        "errors": int(stats.get("total_errors", 0)),
        "uptime": _human_uptime(now - stats.get("start_time", now)),
        "load": load,
        "process": {"rss": process.memory_info().rss, "cpu": _pct(process.cpu_percent(interval=None))},
        "bot_running": bool(_bot_settings_snapshot().get("running")),
        "history": list(TELEMETRY_HISTORY),
    }


# ============================================================
# LOGIN
# ============================================================

from pages import LOGIN_HTML


def login_error_html(
    message: str,
):
    safe_message = escape_html(
        message
    )

    return LOGIN_HTML.replace(
        "</form>",
        (
            f"""
            <div class="error">
                {safe_message}
            </div>
            </form>
            """
        ),
    )


@app.get(
    "/login",
    response_class=HTMLResponse,
)
async def login_page(
    request: Request,
):

    if await is_valid_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    ):
        return RedirectResponse(
            "/dashboard"
        )

    return HTMLResponse(
        LOGIN_HTML
    )


@app.post("/login")
async def login_form(
    request: Request,
):

    try:

        content_type = (
            request.headers
            .get(
                "content-type",
                "",
            )
            .lower()
        )

        if "application/json" in content_type:

            body = await request.json()

            password = str(
                body.get(
                    "password",
                    "",
                )
            ).strip()

            login_username = str(
                body.get(
                    "username",
                    "",
                )
            ).strip()

        else:

            raw = await request.body()

            parsed = parse_qs(
                raw.decode(
                    "utf-8",
                    errors="ignore",
                )
            )

            password = (
                parsed.get(
                    "password",
                    [""],
                )[0]
                .strip()
            )

            login_username = (
                parsed.get(
                    "username",
                    [""],
                )[0]
                .strip()
            )

    except Exception as exc:

        logger.exception(
            "Login parser error: %s",
            exc,
        )

        return HTMLResponse(
            login_error_html(
                "خطا در پردازش اطلاعات ورود."
            ),
            status_code=400,
        )

    ip = client_ip(request)

    blocked, retry_after = login_is_blocked(ip)
    if blocked:
        minutes = max(1, (retry_after + 59) // 60)
        return HTMLResponse(
            login_error_html(
                f"به دلیل تلاش‌های ناموفق متعدد، ورود موقتاً مسدود شده است. حدود {minutes} دقیقه دیگر دوباره تلاش کنید."
            ),
            status_code=429,
            headers={"Retry-After": str(retry_after)},
        )

    if not password:
        register_login_failure(ip)
        return HTMLResponse(
            login_error_html(
                "رمز عبور را وارد کنید."
            ),
            status_code=400,
        )

    ok, admin_id, role, display_name = verify_admin_credentials(login_username, password)

    if not ok:

        locked, value = register_login_failure(ip)
        if locked:
            return HTMLResponse(
                login_error_html(
                    "تعداد تلاش‌های ناموفق بیش از حد مجاز بود. این IP برای ۱۵ دقیقه مسدود شد."
                ),
                status_code=429,
                headers={"Retry-After": str(LOGIN_LOCKOUT_SECONDS)},
            )

        remaining = value
        log_activity(
            "auth",
            (
                f"تلاش ورود ناموفق از {ip}؛ "
                f"{remaining} تلاش باقی مانده"
            ),
            "err",
        )

        return HTMLResponse(
            login_error_html(
                f"رمز عبور اشتباه است. {remaining} تلاش دیگر باقی مانده است."
            ),
            status_code=401,
        )

    clear_login_failures(ip)

    if admin_id != "owner" and admin_id in ADMINS:
        ADMINS[admin_id]["last_login_at"] = datetime.now().isoformat()
        ADMINS[admin_id]["last_login_ip"] = ip
        asyncio.create_task(save_state())

    token = await create_session(admin_id, role)

    response = RedirectResponse(
        "/dashboard?login=1",
        status_code=303,
    )

    set_auth_cookie(
        response,
        request,
        token,
    )

    log_activity(
        "auth",
        (
            f"ورود موفق «{display_name or admin_id}» به پنل "
            f"از {client_ip(request)}"
        ),
        "ok",
    )

    return response


@app.post("/api/login")
async def api_login(
    request: Request,
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    password = str(
        body.get(
            "password",
            "",
        )
    ).strip()

    login_username = str(
        body.get(
            "username",
            "",
        )
    ).strip()

    ip = client_ip(request)

    blocked, retry_after = login_is_blocked(ip)
    if blocked:
        raise HTTPException(
            status_code=429,
            detail=f"ورود موقتاً مسدود است. حدود {max(1, (retry_after + 59) // 60)} دقیقه دیگر تلاش کنید.",
            headers={"Retry-After": str(retry_after)},
        )

    if not password:
        register_login_failure(ip)
        raise HTTPException(
            status_code=400,
            detail="رمز عبور را وارد کنید",
        )

    ok, admin_id, role, display_name = verify_admin_credentials(login_username, password)

    if not ok:

        locked, value = register_login_failure(ip)
        if locked:
            raise HTTPException(
                status_code=429,
                detail="تعداد تلاش‌های ناموفق بیش از حد مجاز بود. این IP برای ۱۵ دقیقه مسدود شد.",
                headers={"Retry-After": str(LOGIN_LOCKOUT_SECONDS)},
            )

        log_activity(
            "auth",
            (
                f"تلاش ورود ناموفق از {ip}؛ "
                f"{value} تلاش باقی مانده"
            ),
            "err",
        )

        raise HTTPException(
            status_code=401,
            detail=f"رمز عبور اشتباه است؛ {value} تلاش دیگر باقی مانده است",
        )

    clear_login_failures(ip)

    if admin_id != "owner" and admin_id in ADMINS:
        ADMINS[admin_id]["last_login_at"] = datetime.now().isoformat()
        ADMINS[admin_id]["last_login_ip"] = ip
        asyncio.create_task(save_state())

    log_activity(
        "auth",
        f"ورود موفق «{display_name or admin_id}» به پنل از {ip}",
        "ok",
    )

    token = await create_session(admin_id, role)

    response = JSONResponse(
        {
            "ok": True,
            "authenticated": True,
            "admin": {"id": admin_id, "username": display_name or admin_id, "role": role},
        }
    )

    set_auth_cookie(
        response,
        request,
        token,
    )

    return response


# ============================================================
# LOGOUT
# ============================================================

@app.get("/logout")
async def logout_page(
    request: Request,
):

    await destroy_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    )

    response = RedirectResponse(
        "/login"
    )

    response.delete_cookie(
        SESSION_COOKIE,
        path="/",
    )

    return response


@app.post("/api/logout")
async def api_logout(
    request: Request,
):

    await destroy_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    )

    response = JSONResponse(
        {
            "ok": True
        }
    )

    response.delete_cookie(
        SESSION_COOKIE,
        path="/",
    )

    return response


@app.get("/api/me")
async def api_me(
    request: Request,
):

    info = await get_session_info(
        request.cookies.get(SESSION_COOKIE)
    )

    if not info:
        return {"authenticated": False}

    admin_id = info.get("admin_id", "owner")
    role = info.get("role", "owner")

    if admin_id == "owner":
        username = AUTH.get("username", DEFAULT_ADMIN_USERNAME)
    else:
        admin = ADMINS.get(admin_id, {})
        username = admin.get("username", admin_id)

    return {
        "authenticated": True,
        "admin": {"id": admin_id, "username": username, "role": role},
    }


# ============================================================
# CHANGE PASSWORD
# ============================================================

@app.get("/api/system/diagnostics")
async def api_system_diagnostics(request: Request, token=Depends(require_auth)):
    """Authenticated live diagnostics used by the Pro dashboard."""
    try:
        import psutil
        proc = psutil.Process(os.getpid())
        vm = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=None)
        mem = proc.memory_info().rss
        net = psutil.net_io_counters()
        disk = psutil.disk_usage("/")
        bot = _bot_settings_snapshot()
        async with LINKS_LOCK:
            links_snapshot = dict(LINKS)
        async with SUBS_LOCK:
            subs_snapshot = dict(SUBS)
        active = sum(1 for x in links_snapshot.values() if is_link_allowed(x))
        clients = sum(1 for x in links_snapshot.values() if x.get("parent_inbound_id"))
        inbounds = len(links_snapshot) - clients
        return {
            "ok": True,
            "time": datetime.now().isoformat(),
            "uptime": _human_uptime(time.time() - stats.get("start_time", time.time())),
            "service": {"status": "healthy", "version": "FaultPass Pro"},
            "resources": {
                "cpu_percent": round(float(cpu), 1),
                "memory_rss": int(mem),
                "memory_percent": round(float(proc.memory_percent()), 1),
                "system_memory_percent": round(float(vm.percent), 1),
                "disk_percent": round(float(disk.percent), 1),
                "rx_bytes": int(net.bytes_recv),
                "tx_bytes": int(net.bytes_sent),
            },
            "objects": {
                "inbounds": max(0, inbounds),
                "clients": clients,
                "active_links": active,
                "subscriptions": len(subs_snapshot),
                "admins": len(ADMINS) + 1,
                "errors": len(error_logs),
            },
            "bot": {"running": bool(bot.get("running")), "admin_count": len(bot.get("admin_ids", "").split(",")) if bot.get("admin_ids") else 0},
            "security": {"session_count": len(SESSIONS), "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME)},
        }
    except Exception as exc:
        logger.exception("Diagnostics error: %s", exc)
        raise HTTPException(status_code=500, detail="Diagnostics unavailable")


@app.post("/api/security/revoke-other-sessions")
async def api_revoke_other_sessions(request: Request, token=Depends(require_auth)):
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است")
    admin_id = info.get("admin_id", "owner")
    removed = 0
    async with SESSIONS_LOCK:
        stale = [tok for tok, sess in SESSIONS.items() if tok != token and isinstance(sess, dict) and sess.get("admin_id", "owner") == admin_id]
        for tok in stale:
            SESSIONS.pop(tok, None)
            removed += 1
    log_activity("auth", f"نشست‌های قبلی حساب «{AUTH.get('username') if admin_id == 'owner' else ADMINS.get(admin_id, {}).get('username', admin_id)}» لغو شد", "warn")
    return {"ok": True, "revoked": removed}


@app.post("/api/change-password")
async def api_change_password(
    request: Request,
    token=Depends(require_auth),
):
    # نکته مهم (رفع باگ): این endpoint قبلاً همیشه رمز عبور مالک (owner) را
    # چک/جایگزین می‌کرد، حتی وقتی یک ادمین فرعی (sub-admin) وارد شده بود.
    # نتیجه: تغییر رمز برای ادمین‌های فرعی یا با خطای «رمز فعلی اشتباه است»
    # مواجه می‌شد (چون با هش رمز owner مقایسه می‌شد)، یا در بدترین حالت رمز
    # owner را به‌جای رمز خودِ ادمین overwrite می‌کرد. همچنین همه‌ی session های
    # تمام ادمین‌ها پاک می‌شد. اینجا اول مشخص می‌کنیم کدام حساب (owner یا کدام
    # sub-admin) درخواست را زده، سپس دقیقاً همان حساب را چک/آپدیت می‌کنیم و
    # فقط نشست‌های همان حساب باطل می‌شوند، نه بقیه‌ی ادمین‌ها.

    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است، دوباره وارد شوید")

    admin_id = info.get("admin_id", "owner")
    is_owner = admin_id == "owner"
    admin_record = None if is_owner else ADMINS.get(admin_id)

    if not is_owner and not admin_record:
        raise HTTPException(status_code=401, detail="حساب کاربری یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    current_password = str(body.get("current_password", ""))
    current_hash = AUTH["password_hash"] if is_owner else admin_record.get("password_hash", "")

    if hash_password(current_password) != current_hash:
        raise HTTPException(
            status_code=400,
            detail="رمز فعلی اشتباه است",
        )

    new_password = str(body.get("new_password", ""))
    repeat_password = str(body.get("repeat_password", ""))

    if len(new_password) < 8:
        raise HTTPException(
            status_code=400,
            detail="رمز جدید باید حداقل ۸ کاراکتر باشد",
        )

    if new_password == current_password:
        raise HTTPException(
            status_code=400,
            detail="رمز جدید باید با رمز فعلی متفاوت باشد",
        )

    if new_password != repeat_password:
        raise HTTPException(
            status_code=400,
            detail="تکرار رمز عبور یکسان نیست",
        )

    new_hash = hash_password(new_password)

    if is_owner:
        AUTH["password_hash"] = new_hash
    else:
        admin_record["password_hash"] = new_hash

    async with SESSIONS_LOCK:
        # فقط نشست‌های همین حساب باطل می‌شوند (نه همه‌ی ادمین‌ها)، اما نشست
        # فعلی زنده می‌ماند تا کاربر بلافاصله logout نشود.
        stale = [
            tok for tok, sess in SESSIONS.items()
            if sess.get("admin_id", "owner") == admin_id and tok != token
        ]
        for tok in stale:
            SESSIONS.pop(tok, None)

        SESSIONS[token] = {
            "exp": time.time() + SESSION_TTL,
            "admin_id": admin_id,
            "role": info.get("role", "owner" if is_owner else "admin"),
            "permissions": sorted(permissions_for_admin(admin_id)),
        }

    await save_state()

    log_activity(
        "auth",
        "رمز عبور پنل تغییر کرد" if is_owner else f"رمز عبور ادمین «{admin_record.get('username', admin_id)}» تغییر کرد",
        "ok",
    )

    return {
        "ok": True
    }


# ============================================================
# CHANGE USERNAME
# ============================================================

@app.post("/api/change-username")
async def api_change_username(
    request: Request,
    token=Depends(require_auth),
):
    info = await get_session_info(token)
    if not info:
        raise HTTPException(status_code=401, detail="نشست نامعتبر است، دوباره وارد شوید")

    admin_id = info.get("admin_id", "owner")
    is_owner = admin_id == "owner"
    admin_record = None if is_owner else ADMINS.get(admin_id)
    if not is_owner and not admin_record:
        raise HTTPException(status_code=401, detail="حساب کاربری یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    if not username:
        raise HTTPException(status_code=400, detail="نام کاربری نمی‌تواند خالی باشد")
    if len(username) < 3 or len(username) > 40:
        raise HTTPException(status_code=400, detail="نام کاربری باید بین ۳ تا ۴۰ کاراکتر باشد")
    if any(ch.isspace() for ch in username):
        raise HTTPException(status_code=400, detail="نام کاربری نباید فاصله داشته باشد")
    if username.lower() == "owner":
        raise HTTPException(status_code=400, detail="این نام کاربری رزرو شده است")

    current = AUTH.get("username", DEFAULT_ADMIN_USERNAME) if is_owner else admin_record.get("username", admin_id)
    for aid, admin in ADMINS.items():
        if aid != admin_id and str(admin.get("username", "")).lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    if is_owner and username.lower() in {str(a.get("username", "")).lower() for a in ADMINS.values()}:
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    if is_owner:
        AUTH["username"] = username
    else:
        admin_record["username"] = username

    async with SESSIONS_LOCK:
        sess = SESSIONS.get(token)
        if sess:
            sess["exp"] = time.time() + SESSION_TTL

    await save_state()
    log_activity("auth", f"نام کاربری «{current}» به «{username}» تغییر کرد", "ok")
    return {"ok": True, "username": username}


# ============================================================
# CREATE LINK
# ============================================================


@app.get("/api/network/railway")
async def railway_network_info(_=Depends(require_auth)):
    """Return Railway networking hints without exposing secrets."""
    return {
        "is_railway": bool(os.environ.get("RAILWAY_PROJECT_ID") or os.environ.get("RAILWAY_ENVIRONMENT_ID")),
        "public_domain": os.environ.get("RAILWAY_PUBLIC_DOMAIN", ""),
        "tcp_proxy_domain": os.environ.get("RAILWAY_TCP_PROXY_DOMAIN", ""),
        "tcp_proxy_port": safe_int(os.environ.get("RAILWAY_TCP_PROXY_PORT", "0"), minimum=0, maximum=65535),
        "tcp_application_port": safe_int(os.environ.get("RAILWAY_TCP_APPLICATION_PORT", "0"), minimum=0, maximum=65535),
        "app_port": safe_int(os.environ.get("PORT", "0"), minimum=0, maximum=65535),
    }


@app.post("/api/network/tcp-ping")
async def tcp_ping(request: Request, _=Depends(require_auth)):
    """Server-side TCP connectivity test for an address/port entered in the builder."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات تست اتصال معتبر نیست.")
    host = str(body.get("host") or body.get("address") or "").strip()
    port = safe_int(body.get("port", 0), minimum=1, maximum=65535)
    timeout = min(max(float(body.get("timeout", 4.0) or 4.0), 0.5), 8.0)
    if not host:
        raise HTTPException(status_code=400, detail="آدرس سرور را وارد کنید.")
    if not port:
        raise HTTPException(status_code=400, detail="پورت باید بین 1 تا 65535 باشد.")
    started = time.perf_counter()
    try:
        infos = await asyncio.get_running_loop().run_in_executor(None, lambda: __import__('socket').getaddrinfo(host, port, type=__import__('socket').SOCK_STREAM))
        resolved = []
        for info in infos:
            addr = info[4][0]
            if addr not in resolved:
                resolved.append(addr)
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return {"ok": True, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "resolved": resolved[:6], "message": "اتصال TCP برقرار شد."}
    except asyncio.TimeoutError:
        return {"ok": False, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "message": "Timeout: سرور در زمان تعیین‌شده پاسخ نداد."}
    except Exception as exc:
        return {"ok": False, "host": host, "port": port, "latency_ms": round((time.perf_counter()-started)*1000, 1), "message": f"اتصال ناموفق: {type(exc).__name__}: {str(exc)[:180]}"}


@app.get("/api/name-suggestions")
async def api_name_suggestions(request: Request, _=Depends(require_auth)):
    base = request.query_params.get("base", "")
    count = safe_int(request.query_params.get("n"), default=12, minimum=4, maximum=24)
    return {
        "ok": True,
        "enabled": name_style_on(),
        "suggestions": name_suggestions(base, count),
    }


@app.post("/api/links")
async def create_link_api(
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()

        if not isinstance(body, dict):
            raise ValueError(
                "body is not object"
            )

    except Exception as exc:

        logger.exception(
            "Create link JSON error: %s",
            exc,
        )

        raise HTTPException(
            status_code=400,
            detail="اطلاعات ارسال‌شده معتبر نیست.",
        )

    limit_value = safe_float(
        body.get(
            "limit_value",
            0,
        )
    )

    limit_unit = str(
        body.get(
            "limit_unit",
            "GB",
        )
        or "GB"
    ).upper()

    limit_bytes = (
        0
        if limit_value <= 0
        else parse_size_to_bytes(
            limit_value,
            limit_unit,
        )
    )

    expires_days = safe_int(
        body.get(
            "expires_days",
            0,
        ),
        minimum=0,
    )

    expires_at = (
        (
            datetime.now()
            + timedelta(
                days=expires_days
            )
        ).isoformat()
        if expires_days > 0
        else None
    )

    port = safe_int(
        body.get(
            "port",
            DEFAULT_PORT,
        ),
        default=DEFAULT_PORT,
        minimum=MIN_PORT,
        maximum=MAX_PORT,
    )

    ip_limit = safe_int(
        body.get(
            "ip_limit",
            0,
        ),
        minimum=0,
    )

    speed_value = safe_float(
        body.get(
            "speed_limit_value",
            0,
        )
    )

    speed_unit = str(
        body.get(
            "speed_limit_unit",
            "MBIT",
        )
        or "MBIT"
    ).upper()

    speed_bytes = (
        0
        if speed_value <= 0
        else parse_speed_to_bytes(
            speed_value,
            speed_unit,
        )
    )

    connection_limit = safe_int(
        body.get(
            "connection_limit",
            0,
        ),
        minimum=0,
    )

    protocol = str(
        body.get(
            "protocol",
            DEFAULT_PROTOCOL,
        )
        or DEFAULT_PROTOCOL
    ).strip().lower()

    if protocol != "manual" and protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL

    manual_fields = body.get("manual") or {}
    if not isinstance(manual_fields, dict):
        manual_fields = {}

    fingerprint = str(
        body.get(
            "fingerprint",
            DEFAULT_FINGERPRINT,
        )
        or DEFAULT_FINGERPRINT
    ).strip().lower()

    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT

    fragment = str(
        body.get(
            "fragment",
            "off",
        )
        or "off"
    ).strip().lower()

    allowed_fragments = {
        "off",
        "safe",
        "balanced",
        "aggressive",
    }

    if fragment not in allowed_fragments:
        fragment = "off"

    raw_clean = body.get("clean_ips") or body.get("clean_ip") or ""
    if isinstance(raw_clean, list):
        clean_ips = [str(x).strip() for x in raw_clean if str(x).strip()]
    else:
        clean_ips = [x.strip() for x in str(raw_clean).replace(",", "\n").splitlines() if x.strip()]
    alarm_enabled = bool(body.get("alarm_enabled", False))
    category_id = str(body.get("category_id") or "0")
    if category_id not in CATEGORIES:
        category_id = "0"
    config_count = safe_int(body.get("config_count", 1), minimum=1, maximum=40)
    client_limit = safe_int(body.get("client_limit", 0), minimum=0, maximum=1000)
    requested_expires_at = str(body.get("expires_at") or "").strip()
    if requested_expires_at:
        try:
            dt = datetime.fromisoformat(requested_expires_at.replace("Z", "+00:00"))
            expires_at = dt.replace(tzinfo=None).isoformat()
        except Exception:
            raise HTTPException(status_code=400, detail="زمان انقضا معتبر نیست")
    cat = CATEGORIES.get(category_id) or {}
    if cat.get("limit_bytes") and limit_bytes <= 0:
        limit_bytes = int(cat["limit_bytes"])
    if cat.get("expires_days") and expires_days <= 0:
        expires_days = int(cat["expires_days"])
        expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days > 0 else None
    if cat.get("connection_limit") and connection_limit <= 0:
        connection_limit = int(cat["connection_limit"])
    if cat.get("speed_limit_bytes") and speed_bytes <= 0:
        speed_bytes = int(cat["speed_limit_bytes"])
    if cat.get("ip_limit") and ip_limit <= 0:
        ip_limit = int(cat["ip_limit"])
    if cat.get("clean_ips") and not clean_ips:
        clean_ips = list(cat["clean_ips"])
    if cat.get("single_user"):
        if ip_limit == 0: ip_limit = 1
        if connection_limit == 0: connection_limit = 1
    label_val = body.get("label", "")
    if cat.get("random_name") or not str(label_val).strip():
        label_val = auto_display_name()
    else:
        label_val = decorate_label(sanitize_display_name(str(label_val)))

    _obs = clean_outbound_proxy_ids(body.get("outbound_proxy_ids")) if isinstance(body.get("outbound_proxy_ids"), list) else [clean_outbound_proxy_id(body.get("outbound_proxy_id"))]
    uid, link = await make_link(
        label=label_val,
        limit_bytes=limit_bytes,
        expires_at=expires_at,
        note=body.get(
            "note",
            "",
        ),
        sub_id=body.get(
            "sub_id"
        ),
        protocol=protocol,
        fingerprint=fingerprint,
        alpn=body.get(
            "alpn",
            DEFAULT_ALPN_BY_PROTOCOL.get(
                protocol,
                "http/1.1",
            ),
        ),
        port=port,
        ip_limit=ip_limit,
        speed_limit_bytes=speed_bytes,
        connection_limit=connection_limit,
        fragment=fragment,
        clean_ips=clean_ips,
        alarm_enabled=alarm_enabled,
        category_id=category_id,
        config_count=config_count,
        manual_fields=manual_fields,
        outbound_proxy_id=_obs[0],
        outbound_proxy_ids=_obs,
    )

    async with LINKS_LOCK:
        LINKS[uid]["client_limit"] = client_limit
    await save_state()

    host = get_host(request)

    result = {
        **get_link_info(
            link,
            uid,
            host,
        ),
        "ok": True,
    }

    return result


# ============================================================
# AUTO CREATE
# ============================================================

@app.post("/api/links/auto")
async def create_auto_link(
    request: Request,
    _=Depends(require_auth),
):
    try:
        body = await request.json()
    except Exception:
        body = {}
    if not isinstance(body, dict): body = {}
    host = get_host(request)
    protocol = normalize_protocol(body.get("protocol", DEFAULT_PROTOCOL))
    profile = str(body.get("profile", "balanced")).strip().lower()
    profiles = {
        "normal": {"ip":0,"conn":0,"speed":0,"fp":"chrome","fragment":"off"},
        "balanced": {"ip":2,"conn":4,"speed":0,"fp":"chrome","fragment":"safe"},
        "gaming": {"ip":1,"conn":2,"speed":0,"fp":"chrome","fragment":"safe"},
        "maximum": {"ip":0,"conn":0,"speed":0,"fp":"randomized","fragment":"safe"},
    }
    cfg = profiles.get(profile, profiles["balanced"])
    _obs = clean_outbound_proxy_ids(body.get("outbound_proxy_ids")) if isinstance(body.get("outbound_proxy_ids"), list) else [clean_outbound_proxy_id(body.get("outbound_proxy_id"))]
    uid, link = await make_link(
        label=auto_display_name(), limit_bytes=0, expires_at=None,
        ip_limit=cfg["ip"], speed_limit_bytes=cfg["speed"], connection_limit=cfg["conn"],
        note=f"Auto generated by FaultPass | profile={profile}",
        protocol=protocol, fingerprint=cfg["fp"],
        alpn=DEFAULT_ALPN_BY_PROTOCOL.get(protocol, ""), port=443, fragment=cfg["fragment"],
        outbound_proxy_id=_obs[0],
        outbound_proxy_ids=_obs,
    )
    link["security_profile"] = profile
    result = {**get_link_info(link, uid, host), "ok": True, "profile": profile}
    log_activity("link", f"کانفیگ خودکار «{link['label']}» با {PROTOCOL_LABELS.get(protocol, protocol)} ساخته شد", "ok")
    return result


MAX_BULK_LINKS = 500


@app.post("/api/links/outbound")
async def set_links_outbound(
    request: Request,
    _=Depends(require_auth),
):
    """اعمال (یا تغییر) خروجی روی هر تعداد اینباند. کلاینت‌های هر اینباند هم
    پیش‌فرض همراهش عوض می‌شوند، چون ریلی خروجی را از UUID خودِ کلاینت می‌خواند.
    body: {uuids: [...], outbound_proxy_id: "" | "<id>", include_clients: true}"""
    try:
        body = await request.json()
    except Exception:
        body = None
    if not isinstance(body, dict) or not isinstance(body.get("uuids"), list) or not body["uuids"]:
        raise HTTPException(status_code=400, detail="حداقل یک اینباند انتخاب کنید.")
    if len(body["uuids"]) > MAX_BULK_LINKS:
        raise HTTPException(status_code=400, detail=f"حداکثر {MAX_BULK_LINKS} مورد در هر بار")
    if isinstance(body.get("outbound_proxy_ids"), list):
        ids = clean_outbound_proxy_ids(body.get("outbound_proxy_ids"))
    else:
        ids = [clean_outbound_proxy_id(body.get("outbound_proxy_id"))]
    pid = ids[0]
    include_clients = bool(body.get("include_clients", True))
    targets = [str(u) for u in dict.fromkeys(body["uuids"])]

    updated, clients, missing = 0, 0, []
    async with LINKS_LOCK:
        for uid in targets:
            link = LINKS.get(uid)
            if link is None:
                missing.append(uid)
                continue
            set_link_outbounds(link, ids)
            updated += 1
            if include_clients:
                for child in LINKS.values():
                    if child.get("parent_inbound_id") == uid:
                        set_link_outbounds(child, ids)
                        clients += 1
    await save_state()
    info = outbound_info(pid)
    names = "، ".join(outbound_tag(p) for p in ids)
    log_activity("link", f"خروجی {updated} اینباند و {clients} کلاینت روی «{names}» تنظیم شد", "ok")
    return {"ok": True, "updated": updated, "clients": clients, "missing": missing, "outbound": info, "outbound_proxy_ids": ids}


# ============================================================
# INBOUND CLIENT MANAGER
# ============================================================

async def add_client_to_inbound(uid: str, label: str = None, limit_bytes: int = None, expires_days: int = 0,
                                  ip_limit: int = None, speed_limit_bytes: int = None, connection_limit: int = None,
                                  note: str = None):
    """Core logic to create a real client (child link) under an inbound. Shared by the
    HTTP API and the Telegram bot so both stay in sync."""
    async with LINKS_LOCK:
        parent = LINKS.get(uid)
        if not parent:
            raise ValueError("اینباند پیدا نشد")
        source = dict(parent)
        existing_clients = sum(1 for x in LINKS.values() if x.get("parent_inbound_id") == uid)
        client_limit = int(source.get("client_limit") or 0)
        if client_limit and existing_clients >= client_limit:
            raise ValueError(f"ظرفیت اینباند تکمیل است ({client_limit} کاربر)")
    final_label = str(label or f"Client · {existing_clients+1}").strip()[:120]
    final_limit_bytes = safe_int(limit_bytes if limit_bytes is not None else source.get("limit_bytes", 0), minimum=0)
    expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() if expires_days else source.get("expires_at")
    child_uid, child = await make_link(
        label=final_label,
        limit_bytes=final_limit_bytes,
        expires_at=expires_at,
        note=str(note or source.get("note") or "")[:500],
        sub_id=source.get("sub_id"),
        protocol=source.get("protocol", DEFAULT_PROTOCOL),
        fingerprint=source.get("fingerprint", DEFAULT_FINGERPRINT),
        alpn=source.get("alpn", ""),
        port=int(source.get("port", DEFAULT_PORT) or DEFAULT_PORT),
        ip_limit=safe_int(ip_limit if ip_limit is not None else source.get("ip_limit", 0), minimum=0),
        speed_limit_bytes=safe_int(speed_limit_bytes if speed_limit_bytes is not None else source.get("speed_limit_bytes", 0), minimum=0),
        connection_limit=safe_int(connection_limit if connection_limit is not None else source.get("connection_limit", 0), minimum=0),
        fragment=source.get("fragment", "off"),
        clean_ips=source.get("clean_ips", []),
        alarm_enabled=bool(source.get("alarm_enabled", False)),
        category_id=str(source.get("category_id") or "0"),
        config_count=1,
        manual_fields={k: source.get(k) for k in ("base_protocol","network","security","address","path","host_header","sni","flow","grpc_service_name","grpc_mode","xhttp_mode","header_type","allow_insecure","reality_public_key","reality_short_id","reality_spider_x","ss_method","ss_password")},
    )
    async with LINKS_LOCK:
        LINKS[child_uid]["parent_inbound_id"] = uid
        LINKS[child_uid]["is_default"] = False
        # ریلی خروجی را از UUID خودِ کلاینت می‌خواند؛ پس باید همان خروجی اینباند را داشته باشد
        set_link_outbounds(LINKS[child_uid], link_outbound_ids(source))
        LINKS[child_uid]["protocol_label"] = protocol_display_label(LINKS[child_uid])
    await save_state()
    log_activity("client", f"کلاینت جدید برای «{source.get('label','اینباند')}» ساخته شد", "ok")
    return child_uid, LINKS[child_uid]


async def remove_inbound_client(uid: str, client_id: str):
    async with LINKS_LOCK:
        child = LINKS.get(client_id)
        if not child or child.get("parent_inbound_id") != uid:
            raise ValueError("کلاینت پیدا نشد")
        LINKS.pop(client_id, None)
    await save_state()
    log_activity("client", f"کلاینت {client_id[:8]}… حذف شد", "warn")


@app.get("/api/links/{uid}/clients")
async def list_inbound_clients(uid: str, request: Request, _=Depends(require_auth)):
    async with LINKS_LOCK:
        parent = LINKS.get(uid)
        if not parent:
            raise HTTPException(status_code=404, detail="اینباند پیدا نشد")
        children = [(cid, dict(link)) for cid, link in LINKS.items() if link.get("parent_inbound_id") == uid]
    host = get_host(request)
    return {"ok": True, "inbound": get_link_info(parent, uid, host), "clients": [get_link_info(x, cid, host) for cid, x in children]}

@app.post("/api/links/{uid}/clients")
async def create_inbound_client(uid: str, request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    try:
        child_uid, _child = await add_client_to_inbound(
            uid,
            label=body.get("label"),
            limit_bytes=body.get("limit_bytes"),
            expires_days=safe_int(body.get("expires_days", 0), minimum=0),
            ip_limit=body.get("ip_limit"),
            speed_limit_bytes=body.get("speed_limit_bytes"),
            connection_limit=body.get("connection_limit"),
            note=body.get("note"),
        )
    except ValueError as exc:
        code = 409 if "ظرفیت" in str(exc) else 404
        raise HTTPException(status_code=code, detail=str(exc))
    host = get_host(request)
    return {"ok": True, "client": get_link_info(LINKS[child_uid], child_uid, host)}

@app.delete("/api/links/{uid}/clients/{client_id}")
async def delete_inbound_client(uid: str, client_id: str, _=Depends(require_auth)):
    try:
        await remove_inbound_client(uid, client_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {"ok": True, "deleted": client_id}

# ============================================================
# LIST LINKS
# ============================================================

@app.get("/api/protocols")
async def api_protocols(request: Request, _=Depends(require_auth)):
    return {
        "protocols": [
            {
                "id": p,
                "label": PROTOCOL_LABELS.get(p, p),
                "functional": p in LIVE_PROTOCOLS,
                "live_status": "live" if p in LIVE_PROTOCOLS else "link-only",
            }
            for p in PROTOCOLS
        ],
        "default": DEFAULT_PROTOCOL,
        "manual": {
            "base_protocols": [
                {"id": p, "label": MANUAL_BASE_PROTOCOL_LABELS.get(p, p)}
                for p in MANUAL_BASE_PROTOCOLS
            ],
            "networks": [
                {"id": n, "label": NETWORK_LABELS.get(n, n)}
                for n in NETWORKS
            ],
            "securities": [
                {"id": s, "label": SECURITY_LABELS.get(s, s)}
                for s in SECURITIES
            ],
            "xhttp_modes": list(XHTTP_MODES),
            "shadowsocks_methods": list(SHADOWSOCKS_METHODS),
            "fingerprints": list(FINGERPRINTS),
            "live_combos": [["vless", n, s] for n, s in manual_live_combos()],
        },
    }


@app.get("/api/reality-keypair")
async def api_reality_keypair(_=Depends(require_auth)):
    """تولید یک جفت‌کلید X25519 و Short ID تصادفی برای Reality — دقیقاً با همان
    فرمتی که Xray-core و کلاینت‌ها (v2rayN، NekoBox، Streisand، ...) انتظار دارند
    (base64url بدون padding، ۳۲ بایت خام)."""
    try:
        from cryptography.hazmat.primitives.asymmetric import x25519
        from cryptography.hazmat.primitives import serialization

        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()

        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        b64 = lambda b: base64.urlsafe_b64encode(b).decode().rstrip("=")

        return {
            "ok": True,
            "private_key": b64(priv_bytes),
            "public_key": b64(pub_bytes),
            "short_id": secrets.token_hex(4),
        }
    except Exception as exc:
        logger.exception("Reality keypair generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="تولید کلید Reality ممکن نشد. کتابخانه‌ی cryptography نصب است؟")


@app.get("/api/links")
async def list_links(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    result = []

    for uid, link in snapshot.items():

        info = get_link_info(
            link,
            uid,
            host,
        )

        info["client_count"] = sum(1 for x in snapshot.values() if x.get("parent_inbound_id") == uid)
        result.append(
            {
                **info,

                "created_at":
                    link.get(
                        "created_at"
                    ),

                "expired":
                    is_link_expired(
                        link
                    ),

                "sub_url":
                    f"{get_scheme()}://{host}/sub/{uid}",

                "info_url":
                    f"{get_scheme()}://{host}/info/{uid}",

                "connected_ips":
                    len(
                        unique_ips_for_uuid(
                            uid
                        )
                    ),
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "created_at",
                "",
            ),
        reverse=True,
    )

    return {
        "links": result
    }


# ============================================================
# LINK INFO API
# ============================================================

@app.get("/api/links/{uid}/info")
async def link_info_api(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    async with LINKS_LOCK:

        link = LINKS.get(uid)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        snapshot = dict(link)

    host = get_host(request)

    return {
        "ok": True,
        **get_link_info(
            snapshot,
            uid,
            host,
        ),
    }


# ============================================================
# UPDATE LINK
# ============================================================

@app.patch("/api/links/{uid}")
async def update_link(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=400,
            detail="اطلاعات نامعتبر است",
        )

    async with LINKS_LOCK:

        if uid not in LINKS:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        link = LINKS[uid]

        old_sub = link.get(
            "sub_id"
        )

        label = link.get(
            "label",
            uid,
        )

        if "active" in body:
            link["active"] = bool(
                body["active"]
            )

        if "label" in body:

            value = str(
                body["label"]
            ).strip()

            if value:
                link["label"] = value[:60]

        if "note" in body:

            link["note"] = str(
                body.get(
                    "note",
                    "",
                )
            )[:500]

        if "reset_usage" in body:

            if body.get(
                "reset_usage"
            ):
                link[
                    "used_bytes"
                ] = 0
                link.pop("quota_exhausted_at", None)

        if "limit_value" in body:

            value = safe_float(
                body.get(
                    "limit_value",
                    0,
                )
            )

            unit = str(
                body.get(
                    "limit_unit",
                    "GB",
                )
                or "GB"
            )

            link[
                "limit_bytes"
            ] = (
                0
                if value <= 0
                else parse_size_to_bytes(
                    value,
                    unit,
                )
            )

        if "expires_at" in body and str(body.get("expires_at") or "").strip():
            try:
                dt = datetime.fromisoformat(str(body.get("expires_at")).replace("Z", "+00:00"))
                link["expires_at"] = dt.replace(tzinfo=None).isoformat()
            except Exception:
                raise HTTPException(status_code=400, detail="زمان انقضا معتبر نیست")
        elif "expires_at" in body and not str(body.get("expires_at") or "").strip() and "expires_days" not in body:
            link["expires_at"] = None

        if "expires_days" in body:

            days = safe_int(
                body.get(
                    "expires_days",
                    0,
                ),
                minimum=0,
            )

            link[
                "expires_at"
            ] = (
                (
                    datetime.now()
                    + timedelta(
                        days=days
                    )
                ).isoformat()
                if days > 0
                else None
            )

        if "fingerprint" in body:

            fingerprint = str(
                body.get(
                    "fingerprint",
                    DEFAULT_FINGERPRINT,
                )
            ).strip().lower()

            link[
                "fingerprint"
            ] = (
                fingerprint
                if fingerprint in FINGERPRINTS
                else DEFAULT_FINGERPRINT
            )

        if "alpn" in body:

            link["alpn"] = str(
                body.get(
                    "alpn",
                    "",
                )
            )[:100]

        if "port" in body:

            p = safe_int(
                body.get(
                    "port",
                    DEFAULT_PORT,
                ),
                default=DEFAULT_PORT,
                minimum=MIN_PORT,
                maximum=MAX_PORT,
            )

            link["port"] = p

        if "ip_limit" in body:

            link["ip_limit"] = safe_int(
                body.get(
                    "ip_limit",
                    0,
                ),
                minimum=0,
            )

        if "connection_limit" in body:

            link[
                "connection_limit"
            ] = safe_int(
                body.get(
                    "connection_limit",
                    0,
                ),
                minimum=0,
            )

        if "client_limit" in body:
            link["client_limit"] = safe_int(body.get("client_limit", 0), minimum=0, maximum=1000)

        if "config_count" in body:
            link["config_count"] = safe_int(body.get("config_count", 1), minimum=1, maximum=40)

        if "clean_ips" in body:
            raw_clean = body.get("clean_ips") or body.get("clean_ip") or ""
            if isinstance(raw_clean, list):
                link["clean_ips"] = [str(x).strip() for x in raw_clean if str(x).strip()]
            else:
                link["clean_ips"] = [x.strip() for x in str(raw_clean).replace(",", "\n").splitlines() if x.strip()]

        if "speed_limit_value" in body:

            speed_value = safe_float(
                body.get(
                    "speed_limit_value",
                    0,
                )
            )

            speed_unit = str(
                body.get(
                    "speed_limit_unit",
                    "MBIT",
                )
                or "MBIT"
            )

            link[
                "speed_limit_bytes"
            ] = (
                0
                if speed_value <= 0
                else parse_speed_to_bytes(
                    speed_value,
                    speed_unit,
                )
            )

        if "protocol" in body:

            protocol = str(
                body.get(
                    "protocol",
                    DEFAULT_PROTOCOL,
                )
            ).strip().lower()

            link["protocol"] = (
                protocol
                if protocol == "manual" or protocol in PROTOCOLS
                else DEFAULT_PROTOCOL
            )
            if link["protocol"] != "manual":
                link["protocol_label"] = protocol_display_label(link)

        if link.get("protocol") == "manual" and isinstance(body.get("manual"), dict):
            manual_fields = body["manual"]
            link["base_protocol"] = normalize_base_protocol(manual_fields.get("base_protocol", link.get("base_protocol")))
            link["network"] = normalize_network(manual_fields.get("network", link.get("network")))
            link["security"] = normalize_security(manual_fields.get("security", link.get("security")))
            if "address" in manual_fields:
                link["address"] = str(manual_fields.get("address") or "").strip()[:255]
            if "path" in manual_fields:
                link["path"] = str(manual_fields.get("path") or "").strip()[:255]
            if "host_header" in manual_fields:
                link["host_header"] = str(manual_fields.get("host_header") or "").strip()[:255]
            if "sni" in manual_fields:
                link["sni"] = str(manual_fields.get("sni") or "").strip()[:255]
            if "flow" in manual_fields:
                link["flow"] = str(manual_fields.get("flow") or "").strip()[:64]
            if "grpc_service_name" in manual_fields:
                link["grpc_service_name"] = str(manual_fields.get("grpc_service_name") or "").strip()[:128]
            if "grpc_mode" in manual_fields:
                link["grpc_mode"] = str(manual_fields.get("grpc_mode") or "gun").strip()[:32] or "gun"
            if "xhttp_mode" in manual_fields:
                link["xhttp_mode"] = normalize_xhttp_mode(manual_fields.get("xhttp_mode"))
            if "header_type" in manual_fields:
                link["header_type"] = str(manual_fields.get("header_type") or "").strip()[:32]
            if "allow_insecure" in manual_fields:
                link["allow_insecure"] = bool(manual_fields.get("allow_insecure"))
            if "reality_public_key" in manual_fields:
                link["reality_public_key"] = str(manual_fields.get("reality_public_key") or "").strip()[:128]
            if "reality_short_id" in manual_fields:
                link["reality_short_id"] = str(manual_fields.get("reality_short_id") or "").strip()[:32]
            if "reality_spider_x" in manual_fields:
                link["reality_spider_x"] = str(manual_fields.get("reality_spider_x") or "/").strip()[:128] or "/"
            if "ss_method" in manual_fields:
                link["ss_method"] = str(manual_fields.get("ss_method") or "chacha20-ietf-poly1305").strip()[:80]
            if "ss_password" in manual_fields:
                link["ss_password"] = str(manual_fields.get("ss_password") or "").strip()[:255]
            link["protocol_label"] = protocol_display_label(link)

        if "outbound_proxy_ids" in body or "outbound_proxy_id" in body:
            if isinstance(body.get("outbound_proxy_ids"), list):
                _ids = clean_outbound_proxy_ids(body.get("outbound_proxy_ids"))
            else:
                _ids = [clean_outbound_proxy_id(body.get("outbound_proxy_id"))]
            set_link_outbounds(link, _ids)
            # کلاینت‌های این اینباند باید همان خروجی‌ها را داشته باشند (ریلی از UUID کلاینت می‌خواند)
            for _child in LINKS.values():
                if _child.get("parent_inbound_id") == uid:
                    set_link_outbounds(_child, _ids)

        if "fragment" in body:

            fragment = str(
                body.get(
                    "fragment",
                    "off",
                )
                or "off"
            ).strip().lower()

            if fragment not in {
                "off",
                "safe",
                "balanced",
                "aggressive",
            }:
                fragment = "off"

            link["fragment"] = fragment

        if "sub_id" in body:

            link[
                "sub_id"
            ] = (
                body.get(
                    "sub_id"
                )
                or None
            )

        new_sub = body.get(
            "sub_id",
            "UNCHANGED",
        )

    if new_sub != "UNCHANGED":

        async with SUBS_LOCK:

            if (
                old_sub
                and old_sub in SUBS
            ):

                ids = SUBS[
                    old_sub
                ].get(
                    "link_ids",
                    [],
                )

                if uid in ids:
                    ids.remove(uid)

            if (
                new_sub
                and new_sub in SUBS
            ):

                ids = SUBS[
                    new_sub
                ].setdefault(
                    "link_ids",
                    [],
                )

                if uid not in ids:
                    ids.append(uid)

    await save_state()

    log_activity(
        "link",
        (
            f"کانفیگ "
            f"«{label}» "
            f"ویرایش شد"
        ),
        "info",
    )

    return {
        "ok": True
    }


# ============================================================
# RESET USAGE
# ============================================================

@app.post(
    "/api/links/{uid}/reset-usage"
)
async def reset_link_usage(
    uid: str,
    _=Depends(require_auth),
):

    async with LINKS_LOCK:

        link = LINKS.get(uid)

        if not link:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        link["used_bytes"] = 0

        label = link.get(
            "label",
            uid,
        )
        link.pop("quota_exhausted_at", None)

    await save_state()

    log_activity(
        "link",
        (
            f"مصرف کانفیگ "
            f"«{label}» ریست شد"
        ),
        "info",
    )

    return {
        "ok": True,
        "uuid": uid,
        "used_bytes": 0,
    }


# ============================================================
# REGENERATE / SWAP LINK (تعویض لینک — UUID جدید، همان تنظیمات)
# ============================================================
# لینک قدیمی بلافاصله از کار می‌افتد (چون UUID عوض شده) و یک UUID جدید با
# همان تنظیمات (حجم، انقضا، دسته، پروتکل، محدودیت‌ها و ...) جایگزینش می‌شود.
# برای کلاینت‌های فرزند یک اینباند هم پشتیبانی می‌شود.

@app.post("/api/links/{uid}/regenerate")
async def regenerate_link(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):
    async with LINKS_LOCK:
        old_link = LINKS.get(uid)
        if not old_link:
            raise HTTPException(status_code=404, detail="link not found")

        new_uid = generate_uuid()
        while new_uid in LINKS:
            new_uid = generate_uuid()

        new_link = dict(old_link)
        # مصرف قبلی حفظ می‌شود (این فقط تعویض کلید/لینک است، نه ریست حجم)
        LINKS[new_uid] = new_link
        del LINKS[uid]

        parent_id = old_link.get("parent_inbound_id")
        sub_id = old_link.get("sub_id")
        label = old_link.get("label", uid)

        # اگر این اینباند بود، فرزندانش را به UUID جدید مادر وصل کن
        updated_children = 0
        for child in LINKS.values():
            if child.get("parent_inbound_id") == uid:
                child["parent_inbound_id"] = new_uid
                updated_children += 1

    if sub_id:
        async with SUBS_LOCK:
            sub = SUBS.get(sub_id)
            if sub:
                ids = sub.get("link_ids", [])
                if uid in ids:
                    ids[ids.index(uid)] = new_uid

    await save_state()

    log_activity(
        "link",
        f"لینک «{label}» تعویض شد (UUID جدید صادر شد)",
        "warn",
    )

    host = get_host(request)
    async with LINKS_LOCK:
        refreshed = LINKS.get(new_uid)

    return {
        **(get_link_info(refreshed, new_uid, host) if refreshed else {}),
        "ok": True,
        "old_uuid": uid,
        "uuid": new_uid,
        "updated_children": updated_children,
    }


# ============================================================
# LINK ACTION
# ============================================================

@app.post(
    "/api/links/{uid}/action"
)
async def link_action(
    uid: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    action = str(
        body.get(
            "action",
            "",
        )
    ).strip().lower()

    if action == "reset":

        await reset_link_usage(
            uid,
            _
        )

        return {
            "ok": True,
            "action": "reset",
        }

    if action == "enable":

        result = await set_link_active(
            uid,
            True,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        return {
            "ok": True,
            "action": "enable",
        }

    if action == "disable":

        result = await set_link_active(
            uid,
            False,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="link not found",
            )

        return {
            "ok": True,
            "action": "disable",
        }

    raise HTTPException(
        status_code=400,
        detail="unknown action",
    )


# ============================================================
# DELETE LINK
# ============================================================

@app.delete("/api/links/{uid}")
async def delete_link(
    uid: str,
    _=Depends(require_auth),
):

    label = await remove_link(uid)

    if label is None:
        raise HTTPException(
            status_code=404,
            detail="link not found",
        )

    return {
        "ok": True,
        "deleted": uid,
    }




def subscription_metadata_headers(used_bytes: int, limit_bytes: int, expires_at, host: str, info_url: str, title: str):
    """Standard subscription headers understood by v2rayNG/v2rayN/Hiddify and similar clients."""
    used_bytes = max(0, int(used_bytes or 0))
    limit_bytes = max(0, int(limit_bytes or 0))

    expire_unix = 0
    if expires_at:
        try:
            dt = datetime.fromisoformat(str(expires_at))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=IRAN_TZ) if IRAN_TZ else dt
            expire_unix = max(0, int(dt.timestamp()))
        except Exception:
            expire_unix = 0

    userinfo = f"upload=0; download={used_bytes}; total={limit_bytes}; expire={expire_unix}"

    return {
        "profile-title": quote(title, safe=""),
        "profile-web-page-url": info_url,
        "support-url": SUPPORT_URL,
        "profile-update-interval": "12",
        "subscription-userinfo": userinfo,
        "content-disposition": 'inline; filename="subscription.txt"',
    }

# ============================================================
# ONE SUBSCRIPTION LINK FOR BOTH APPS AND BROWSERS
# ============================================================
# VPN clients (v2rayNG, v2rayN, Hiddify, Clash, sing-box, ...) send a
# non-browser User-Agent and never ask for text/html, so they keep getting
# the raw base64 config feed below exactly as before. A normal visit from a
# desktop/mobile browser is redirected to the rich HTML portal instead — the
# customer only ever needs to hand out a single /sub/{uuid} link, whether
# it's pasted into an app or opened by hand to check usage.
_SUB_CLIENT_UA_HINTS = (
    "v2ray", "v2rayng", "v2rayn", "hiddify", "clash", "sing-box", "sing_box",
    "shadowrocket", "streisand", "nekobox", "nekoray", "karing", "matsuri",
    "kitsunebi", "quantumult", "surge", "loon", "stash", "husi", "foxray",
    "v2box", "happ", "flclash", "mihomo", "openclash", "passwall",
    "npvtunnel", "netch", "qv2ray", "leaf", "outline", "throne", "exclave",
    "okhttp", "curl", "wget", "python", "go-http", "libcurl",
)
_SUB_BROWSER_UA_HINTS = ("mozilla", "chrome", "safari", "firefox", "edg/", "opr/", "webkit", "gecko")

def _subscription_wants_browser_view(request: Request) -> bool:
    ua = (request.headers.get("user-agent") or "").lower()
    accept = (request.headers.get("accept") or "").lower()
    if not ua or any(h in ua for h in _SUB_CLIENT_UA_HINTS):
        return False
    return "text/html" in accept and any(h in ua for h in _SUB_BROWSER_UA_HINTS)

# ============================================================
# SINGLE SUB
# ============================================================

@app.get("/sub/{uuid}")
async def subscription_single(
    uuid: str,
    request: Request,
):

    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not link_visible_for_subscription(link):
        raise HTTPException(
            status_code=404,
            detail="not found or inactive",
        )

    if _subscription_wants_browser_view(request):
        return RedirectResponse(url=f"/subscription/{uuid}", status_code=307)

    host = get_host(request)
    clean_ips = link.get("clean_ips") or []
    used = int(link.get("used_bytes", 0) or 0)
    limit = int(link.get("limit_bytes", 0) or 0)
    remaining = max(0, limit - used) if limit > 0 else 0
    volume_text = f"{fmt_bytes(used)}/{fmt_bytes(limit)} (باقی {fmt_bytes(remaining)})" if limit > 0 else f"{fmt_bytes(used)}/∞"
    expires_at = link.get("expires_at")
    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(str(expires_at))
            now_dt = datetime.now(exp_dt.tzinfo) if getattr(exp_dt, "tzinfo", None) else datetime.now()
            secs = int((exp_dt - now_dt).total_seconds())
            if secs <= 0:
                time_text = "منقضی"
            else:
                days, rem = divmod(secs, 86400)
                hours, rem = divmod(rem, 3600)
                mins = rem // 60
                time_text = f"{days}د {hours}س" if days else (f"{hours}س {mins}د" if hours else f"{mins}د")
        except Exception:
            time_text = str(expires_at)[:16]
    else:
        time_text = "∞"
    label = str(link.get("label") or "Config")
    stats_remark = f"{label} | {volume_text} | {time_text}"
    stats_line = vless_link_for_link({**link, "label": stats_remark}, uuid, "0.0.0.0")
    lines = [stats_line]
    used_names = set()
    cfg_count = max(1, min(40, int(link.get("config_count") or 1)))
    if clean_ips:
        hosts = list(clean_ips)
        while len(hosts) < cfg_count:
            hosts.extend(clean_ips)
        hosts = hosts[:cfg_count]
    else:
        hosts = [host] * cfg_count
    # چندخروجی: به ازای هر لوکیشن (فرانسه/آلمان/هلند/...) یک دسته کانفیگ جدا
    for vlink, vuid, vtag in expand_outbound_variants(link, uuid):
        for cip in hosts:
            name = random_config_name(used_names)
            used_names.add(name)
            if vtag:
                name = f"{vtag} | {name}"
            lines.append(vless_link_for_link({**vlink, "label": name}, vuid, cip))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    profile_title = f"0.0.0.0 | {stats_remark}"
    headers = subscription_metadata_headers(
        used,
        limit,
        link.get("expires_at"),
        host,
        f"{get_scheme()}://{host}/info/{uuid}",
        profile_title,
    )

    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers=headers,
    )

# ============================================================
# LIVE SUBSCRIPTION TELEMETRY
# ============================================================

@app.get("/api/subscription/{uuid}")
async def subscription_telemetry(uuid: str):
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if not link_visible_for_subscription(link):
            raise HTTPException(status_code=404, detail="subscription not found or inactive")
        limit = int(link.get("limit_bytes", 0) or 0)
        used = int(link.get("used_bytes", 0) or 0)
        history = list(link.get("usage_history") or [])[-144:]
        # همیشه مقدار لحظه‌ای رو به‌عنوان آخرین نقطه بفرست تا نمودار زنده باشه
        now_ts = now_ir().replace(second=0, microsecond=0).isoformat()
        if history and str(history[-1].get("ts", ""))[:16] == now_ts[:16]:
            history[-1] = {**history[-1], "used": used, "limit": limit}
        else:
            history.append({"ts": now_ts, "used": used, "limit": limit})
        active_ips = sorted({str(x.get("ip") or "").strip() for x in connections.values() if x.get("uuid") == uuid and str(x.get("ip") or "").strip()})
        active_sessions = sum(1 for x in connections.values() if x.get("uuid") == uuid)
        return {
            "ok": True, "uuid": uuid, "active": bool(link.get("active", True)),
            "traffic_used": used, "traffic_limit": limit,
            "traffic_remaining": max(0, limit - used) if limit else None,
            "traffic_percent": min(100, round((used / limit) * 100, 1)) if limit else 0,
            "active_connections": len(active_ips), "active_sessions": active_sessions,
            "active_ips": active_ips,
            "connection_limit": int(link.get("connection_limit", 0) or 0),
            "ip_limit": int(link.get("ip_limit", 0) or 0),
            "updated_at": now_ir().isoformat(), "usage_history": history,
        }

# ============================================================
# SMART SUBSCRIPTION PORTAL
# ============================================================

@app.get("/subscription/{uuid}", response_class=HTMLResponse)
async def subscription_portal(uuid: str, request: Request):
    '''Premium customer subscription portal. All figures come from live backend state.'''
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
        if link:
            link = dict(link)
    if not link_visible_for_subscription(link):
        raise HTTPException(status_code=404, detail="subscription not found or inactive")

    host = get_host(request)
    raw_url = f"{get_scheme()}://{host}/sub/{uuid}"
    info_url = f"{get_scheme()}://{host}/info/{uuid}"
    label = str(link.get("label") or "FaultPass Subscription")
    protocol = protocol_display_label(link)
    used = int(link.get("used_bytes", 0) or 0)
    limit = int(link.get("limit_bytes", 0) or 0)
    pct = min(100, round((used / limit) * 100, 1)) if limit else 0
    remaining = max(0, limit - used) if limit else None
    expires = str(link.get("expires_at") or "نامحدود")
    conn_limit = int(link.get("connection_limit", 0) or 0)
    ip_limit = int(link.get("ip_limit", 0) or 0)
    active = bool(link.get("active", True))
    active_ips = {str(x.get("ip") or "").strip() for x in connections.values()
                  if x.get("uuid") == uuid and str(x.get("ip") or "").strip()}
    active_people = len(active_ips)
    active_sessions = sum(1 for x in connections.values() if x.get("uuid") == uuid)
    qr = quote(raw_url, safe="")
    initial = (label.strip()[:1] or "V").upper()

    html = r'''<!doctype html><html lang="fa" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FFFFFF"><title>__LABEL__ · FaultPass</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Vazirmatn:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
/* ============================================================
   Untitled UI design tokens (v2.0) — light + dark
   ============================================================ */
:root{
  --gray-25:#FCFCFD;--gray-50:#F9FAFB;--gray-100:#F2F4F7;--gray-200:#EAECF0;--gray-300:#D0D5DD;--gray-400:#98A2B3;--gray-500:#667085;--gray-600:#475467;--gray-700:#344054;--gray-800:#182230;--gray-900:#101828;--gray-950:#0C111D;
  --brand-25:#FCFAFF;--brand-50:#F9F5FF;--brand-100:#F4EBFF;--brand-200:#E9D7FE;--brand-300:#D6BBFB;--brand-400:#B692F6;--brand-500:#9E77ED;--brand-600:#7F56D9;--brand-700:#6941C6;--brand-800:#53389E;--brand-900:#42307D;
  --success-50:#ECFDF3;--success-200:#ABEFC6;--success-500:#17B26A;--success-600:#079455;--success-700:#067647;
  --error-50:#FEF3F2;--error-200:#FECDCA;--error-500:#F04438;--error-600:#D92D20;--error-700:#B42318;
  --warning-50:#FFFAEB;--warning-200:#FEDF89;--warning-500:#F79009;--warning-600:#DC6803;--warning-700:#B54708;
  --blue-50:#EFF8FF;--blue-200:#B2DDFF;--blue-700:#175CD3;

  /* semantic (light) */
  --bg-primary:#FFFFFF;--bg-secondary:var(--gray-50);--bg-tertiary:var(--gray-100);--bg-brand-section:var(--brand-50);
  --border-primary:var(--gray-300);--border-secondary:var(--gray-200);
  --text-primary:var(--gray-900);--text-secondary:var(--gray-700);--text-tertiary:var(--gray-600);--text-quaternary:var(--gray-500);--text-placeholder:var(--gray-400);
  --text-brand:var(--brand-700);--fg-brand:var(--brand-600);
  --featured-bg:var(--brand-100);--featured-ring:var(--brand-50);--featured-fg:var(--brand-600);
  --b-success-bg:var(--success-50);--b-success-bd:var(--success-200);--b-success-tx:var(--success-700);
  --b-error-bg:var(--error-50);--b-error-bd:var(--error-200);--b-error-tx:var(--error-700);
  --b-warning-bg:var(--warning-50);--b-warning-bd:var(--warning-200);--b-warning-tx:var(--warning-700);
  --b-gray-bg:var(--gray-50);--b-gray-bd:var(--gray-200);--b-gray-tx:var(--gray-700);
  --b-brand-bg:var(--brand-50);--b-brand-bd:var(--brand-200);--b-brand-tx:var(--brand-700);
  --shadow-xs:0 1px 2px rgba(16,24,40,.05);
  --shadow-sm:0 1px 3px rgba(16,24,40,.10),0 1px 2px rgba(16,24,40,.06);
  --shadow-md:0 4px 8px -2px rgba(16,24,40,.10),0 2px 4px -2px rgba(16,24,40,.06);
  --shadow-lg:0 12px 16px -4px rgba(16,24,40,.08),0 4px 6px -2px rgba(16,24,40,.03);
  --ring-brand:0 0 0 4px rgba(158,119,237,.24);
  --ring-gray:0 0 0 4px rgba(152,162,179,.14);
  --radius-sm:6px;--radius-md:8px;--radius-lg:10px;--radius-xl:12px;--radius-2xl:16px;--radius-full:9999px;
  --chart-grid:var(--gray-100);
}
body[data-theme="dark"]{
  --bg-primary:#0C111D;--bg-secondary:#161B26;--bg-tertiary:#1F242F;--bg-brand-section:#1F242F;
  --border-primary:#333741;--border-secondary:#1F242F;
  --text-primary:#F5F5F6;--text-secondary:#CECFD2;--text-tertiary:#94969C;--text-quaternary:#94969C;--text-placeholder:#85888E;
  --text-brand:#CECFD2;--fg-brand:var(--brand-500);
  --featured-bg:#1F242F;--featured-ring:#161B26;--featured-fg:var(--brand-400);
  --b-success-bg:#053321;--b-success-bd:#085D3A;--b-success-tx:#75E0A7;
  --b-error-bg:#55160C;--b-error-bd:#912018;--b-error-tx:#FDA29B;
  --b-warning-bg:#4E1D09;--b-warning-bd:#93370D;--b-warning-tx:#FEC84B;
  --b-gray-bg:#161B26;--b-gray-bd:#333741;--b-gray-tx:#CECFD2;
  --b-brand-bg:#2C1C5F;--b-brand-bd:#53389E;--b-brand-tx:#D6BBFB;
  --shadow-xs:0 1px 2px rgba(0,0,0,.4);--shadow-sm:0 1px 3px rgba(0,0,0,.4),0 1px 2px rgba(0,0,0,.3);
  --shadow-md:0 4px 8px -2px rgba(0,0,0,.45);--shadow-lg:0 12px 16px -4px rgba(0,0,0,.5);
  --chart-grid:#1F242F;
}

/* ============================================================ base */
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;min-height:100vh;background:var(--bg-secondary);color:var(--text-primary);
  font-family:Inter,Vazirmatn,Tahoma,sans-serif;font-size:14px;line-height:20px;-webkit-font-smoothing:antialiased;transition:background .2s,color .2s}
a{text-decoration:none;color:inherit}
button{font-family:inherit;cursor:pointer}
.ltr{direction:ltr;unicode-bidi:isolate}
.wrap{width:min(1024px,calc(100% - 32px));margin:auto;padding:0 0 112px}

/* ============================================================ header nav */
.topbar{background:var(--bg-primary);border-bottom:1px solid var(--border-secondary);position:sticky;top:0;z-index:20}
.topbar-in{width:min(1024px,calc(100% - 32px));margin:auto;height:72px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{display:flex;gap:10px;align-items:center;min-width:0}
.logo{width:36px;height:36px;flex:none;border-radius:var(--radius-md);overflow:hidden;border:1px solid var(--border-secondary);box-shadow:var(--shadow-xs);background:var(--bg-primary)}
.brand b{display:block;font-size:16px;line-height:24px;font-weight:600;color:var(--text-primary)}
.brand small{display:block;color:var(--text-tertiary);font-size:12px;line-height:18px}
.top-actions{display:flex;align-items:center;gap:12px}

/* ============================================================ badges (pill, with dot) */
.badge{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border-radius:var(--radius-full);border:1px solid var(--b-gray-bd);background:var(--b-gray-bg);color:var(--b-gray-tx);font-size:12px;line-height:18px;font-weight:500;white-space:nowrap}
.badge.lg{padding:4px 12px;font-size:14px;line-height:20px}
.badge .dot{width:8px;height:8px;border-radius:50%;background:currentColor;flex:none}
.badge.success,.badge.status-on{border-color:var(--b-success-bd);background:var(--b-success-bg);color:var(--b-success-tx)}
.badge.success .dot,.badge.status-on .dot{background:var(--success-500)}
.badge.error,.badge.off,.badge.status-off{border-color:var(--b-error-bd);background:var(--b-error-bg);color:var(--b-error-tx)}
.badge.off .dot,.badge.status-off .dot{background:var(--error-500)}
.badge.warning{border-color:var(--b-warning-bd);background:var(--b-warning-bg);color:var(--b-warning-tx)}
.badge.brand{border-color:var(--b-brand-bd);background:var(--b-brand-bg);color:var(--b-brand-tx)}
.badge b{font-weight:600}
.live .dot{animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(23,178,106,.45)}70%{box-shadow:0 0 0 6px rgba(23,178,106,0)}100%{box-shadow:0 0 0 0 rgba(23,178,106,0)}}
.live.off .dot{animation:none}

/* ============================================================ buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:10px 14px;border-radius:var(--radius-md);border:1px solid var(--border-primary);background:var(--bg-primary);color:var(--text-secondary);font-size:14px;line-height:20px;font-weight:600;box-shadow:var(--shadow-xs);transition:background .15s,border-color .15s,box-shadow .15s;white-space:nowrap}
.btn i{font-size:20px}
.btn:hover{background:var(--bg-secondary);color:var(--text-primary)}
.btn:focus-visible{outline:0;box-shadow:var(--shadow-xs),var(--ring-gray)}
.btn.primary{background:var(--brand-600);border-color:var(--brand-600);color:#fff}
.btn.primary:hover{background:var(--brand-700);border-color:var(--brand-700)}
.btn.primary:focus-visible{box-shadow:var(--shadow-xs),var(--ring-brand)}
.btn.sm{padding:8px 12px}
.btn.sm i{font-size:18px}
.btn.icon{padding:10px}
.btn.link{border:0;background:none;box-shadow:none;padding:0;color:var(--text-brand)}
.btn.link:hover{color:var(--brand-800);background:none}
.btn.block{width:100%}

/* ============================================================ page header */
.page-head{padding:32px 0 24px;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap}
.who{display:flex;gap:16px;align-items:center;min-width:0}
.avatar{width:64px;height:64px;flex:none;border-radius:50%;display:grid;place-items:center;font:600 24px/1 Inter,sans-serif;color:var(--brand-700);background:var(--brand-50);border:4px solid var(--bg-primary);box-shadow:var(--shadow-lg);outline:1px solid var(--border-secondary)}
body[data-theme="dark"] .avatar{color:var(--brand-300);background:#2C1C5F}
.who h1{margin:0;font-size:24px;line-height:32px;font-weight:600;color:var(--text-primary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:58vw}
.who p{margin:4px 0 8px;color:var(--text-tertiary);font-size:14px;line-height:20px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.head-actions{display:flex;gap:12px}

/* ============================================================ cards */
.card{background:var(--bg-primary);border:1px solid var(--border-secondary);border-radius:var(--radius-xl);box-shadow:var(--shadow-xs);overflow:hidden}
.card-head{padding:20px 24px;border-bottom:1px solid var(--border-secondary);display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
.card-head h2{margin:0;font-size:18px;line-height:28px;font-weight:600;color:var(--text-primary)}
.card-head p{margin:4px 0 0;font-size:14px;line-height:20px;color:var(--text-tertiary)}
.card-body{padding:24px}
.stack{display:grid;gap:24px;margin-top:24px}
.grid-2{display:grid;grid-template-columns:1.25fr .75fr;gap:24px}

/* metric cards */
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.metric{background:var(--bg-primary);border:1px solid var(--border-secondary);border-radius:var(--radius-xl);box-shadow:var(--shadow-xs);padding:20px 24px;display:flex;flex-direction:column;gap:16px}
.metric-top{display:flex;align-items:center;gap:12px}
.metric-top span{font-size:14px;line-height:20px;font-weight:500;color:var(--text-tertiary)}
.metric b{font-size:30px;line-height:38px;font-weight:600;letter-spacing:-.02em;color:var(--text-primary);direction:ltr;text-align:right;unicode-bidi:isolate}

/* featured icon (light circle, modern) */
.fi{width:40px;height:40px;flex:none;border-radius:50%;display:grid;place-items:center;background:var(--featured-bg);box-shadow:0 0 0 6px var(--featured-ring);color:var(--featured-fg);font-size:20px}
.fi.sq{border-radius:var(--radius-md);box-shadow:var(--shadow-xs);background:var(--bg-primary);border:1px solid var(--border-primary);color:var(--text-secondary)}
.fi.success{background:var(--b-success-bg);box-shadow:0 0 0 6px color-mix(in srgb,var(--b-success-bg) 55%,transparent);color:var(--success-600)}
.fi.warning{background:var(--b-warning-bg);box-shadow:0 0 0 6px color-mix(in srgb,var(--b-warning-bg) 55%,transparent);color:var(--warning-600)}
.fi.lg{width:48px;height:48px;font-size:24px;box-shadow:0 0 0 8px var(--featured-ring)}

/* usage */
.usage{display:grid;grid-template-columns:180px 1fr;gap:32px;align-items:center}
.ring{width:180px;height:180px;border-radius:50%;background:conic-gradient(var(--fg-brand) calc(var(--pct)*1%),var(--bg-tertiary) 0);display:grid;place-items:center;position:relative;transition:background .4s}
.ring:before{content:"";position:absolute;inset:16px;border-radius:50%;background:var(--bg-primary)}
.ring-c{position:relative;text-align:center}
.ring-c small{display:block;font-size:12px;line-height:18px;font-weight:500;color:var(--text-tertiary)}
.ring-c b{display:block;font-size:30px;line-height:38px;font-weight:600;color:var(--text-primary);letter-spacing:-.02em;direction:ltr}
.kv{display:grid;gap:0}
.kv-row{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border-secondary);font-size:14px}
.kv-row:first-child{padding-top:0}
.kv-row span{color:var(--text-tertiary)}
.kv-row b{font-weight:600;color:var(--text-primary);direction:ltr;unicode-bidi:isolate}
.progress{display:flex;align-items:center;gap:12px;margin-top:16px}
.bar{flex:1;height:8px;border-radius:var(--radius-full);background:var(--bg-tertiary);overflow:hidden}
.bar i{display:block;height:100%;width:0;border-radius:inherit;background:var(--fg-brand);transition:width .5s ease}
.progress span{font-size:14px;font-weight:500;color:var(--text-secondary);direction:ltr;min-width:44px;text-align:left}

/* live connections */
.live-num{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:20px;border-bottom:1px solid var(--border-secondary);margin-bottom:8px}
.live-num b{display:block;font-size:36px;line-height:44px;font-weight:600;letter-spacing:-.02em;color:var(--text-primary)}
.live-num small{display:block;font-size:14px;color:var(--text-tertiary)}
.muted{color:var(--text-tertiary)}

/* alert / note */
.alert{display:flex;gap:12px;padding:16px;border:1px solid var(--border-primary);border-radius:var(--radius-xl);background:var(--bg-secondary);font-size:14px;line-height:20px;color:var(--text-tertiary);margin-top:20px}
.alert i{font-size:20px;color:var(--text-quaternary);flex:none;margin-top:1px}
.actions{display:flex;gap:12px;margin-top:20px;flex-wrap:wrap}
.actions .btn{flex:1;min-width:140px}

/* expiry row */
.expire{display:flex;align-items:center;gap:20px;padding:20px 24px}
.expire div.t{flex:1;min-width:0}
.expire span{display:block;font-size:14px;color:var(--text-tertiary)}
.expire strong{display:block;font-size:18px;line-height:28px;font-weight:600;color:var(--text-primary);direction:ltr;text-align:right;unicode-bidi:isolate}

/* chart */
.chart{height:220px;position:relative}
.chart svg{width:100%;height:100%;overflow:visible}
.chart .line{fill:none;stroke:var(--fg-brand);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}
.chart .area{fill:url(#area)}
.chart .gridline{stroke:var(--chart-grid);stroke-width:1;vector-effect:non-scaling-stroke}
.chart .point{fill:transparent;stroke:none}
.chart .point.last{fill:var(--bg-primary);stroke:var(--fg-brand);stroke-width:2.5}
.chart text{fill:var(--text-quaternary);font-size:11px;font-family:Inter,sans-serif}

/* input w/ trailing button (Untitled "input with copy") */
.field-label{display:block;font-size:14px;line-height:20px;font-weight:500;color:var(--text-secondary);margin-bottom:6px}
.input-group{display:flex;direction:ltr;border:1px solid var(--border-primary);border-radius:var(--radius-md);box-shadow:var(--shadow-xs);background:var(--bg-primary);overflow:hidden}
.input-group:focus-within{border-color:var(--brand-300);box-shadow:var(--shadow-xs),var(--ring-brand)}
.input-group .url{flex:1;min-width:0;padding:10px 14px;font:14px/24px Inter,ui-monospace,monospace;color:var(--text-primary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:left}
.input-group button{border:0;border-left:1px solid var(--border-primary);background:var(--bg-primary);color:var(--text-secondary);padding:10px 14px;display:flex;align-items:center;gap:8px;font-weight:600;font-size:14px}
.input-group button:hover{background:var(--bg-secondary)}
.hint{font-size:14px;line-height:20px;color:var(--text-tertiary);margin-top:6px}
.qr-wrap{display:none;place-items:center;margin-bottom:20px}
.qr-wrap.show{display:grid}
.qr-wrap img{width:180px;height:180px;padding:12px;background:#fff;border:1px solid var(--gray-200);border-radius:var(--radius-xl);box-shadow:var(--shadow-sm)}

/* apps list (table-ish rows) */
.apps{display:grid}
.app-row{display:flex;align-items:center;gap:12px;padding:16px 24px;border-bottom:1px solid var(--border-secondary)}
.app-row:last-child{border-bottom:0}
.app-row:hover{background:var(--bg-secondary)}
.app-icon{width:40px;height:40px;flex:none;border-radius:var(--radius-md);display:grid;place-items:center;border:1px solid var(--border-secondary);background:var(--bg-primary);box-shadow:var(--shadow-xs);font-size:22px;color:var(--text-secondary)}
.app-meta{flex:1;min-width:0}
.app-name{font-size:14px;line-height:20px;font-weight:600;color:var(--text-primary)}
.app-sub{font-size:14px;line-height:20px;color:var(--text-tertiary)}
.app-row .badge{margin-inline-end:8px}

.footer{text-align:center;color:var(--text-quaternary);font-size:14px;margin-top:32px}

/* toast (Untitled notification) */
.toast{position:fixed;top:16px;left:50%;z-index:100;transform:translate(-50%,-140%);display:flex;align-items:center;gap:12px;padding:12px 16px;border-radius:var(--radius-xl);background:var(--bg-primary);border:1px solid var(--border-primary);box-shadow:var(--shadow-lg);color:var(--text-primary);font-size:14px;font-weight:600;transition:transform .3s cubic-bezier(.2,.8,.2,1)}
.toast:before{content:"";width:10px;height:10px;border-radius:50%;background:var(--success-500);box-shadow:0 0 0 4px var(--b-success-bg)}
.toast.show{transform:translate(-50%,0)}

/* mobile bottom bar */
.bottom-nav{display:none}
@media(max-width:760px){
  .bottom-nav{display:grid;position:fixed;z-index:30;left:0;right:0;bottom:0;grid-template-columns:repeat(2,1fr);
    padding:8px 12px calc(8px + env(safe-area-inset-bottom));background:var(--bg-primary);border-top:1px solid var(--border-secondary);box-shadow:0 -4px 12px rgba(16,24,40,.06)}
  .bottom-nav button{border:0;background:transparent;color:var(--text-quaternary);border-radius:var(--radius-md);padding:6px 0;display:grid;place-items:center;gap:2px;font-size:22px}
  .bottom-nav button small{font-size:12px;font-weight:600}
  .bottom-nav button.active{color:var(--fg-brand);background:var(--bg-brand-section)}
}

@media(max-width:900px){.metrics{grid-template-columns:repeat(2,1fr);gap:16px}.grid-2{grid-template-columns:1fr}}
@media(max-width:640px){
  .wrap,.topbar-in{width:calc(100% - 32px)}
  .topbar-in{height:64px}
  .brand small,#themeLabel{display:none}
  .page-head{padding:24px 0 20px;align-items:flex-start}
  .head-actions{width:100%}.head-actions .btn{flex:1}
  .who h1{font-size:20px;line-height:30px;max-width:64vw}
  .avatar{width:56px;height:56px;font-size:20px}
  .usage{grid-template-columns:1fr;gap:24px}.ring{margin:auto}
  .metric{padding:16px}.metric b{font-size:24px;line-height:32px}
  .card-head,.card-body{padding-left:16px;padding-right:16px}
  .app-row{padding:16px}.expire{padding:16px}
  .stack{gap:16px;margin-top:16px}.grid-2{gap:16px}
  .app-row .badge{display:none}
}
</style></head><body>

<header class="topbar"><div class="topbar-in">
  <div class="brand"><div class="logo"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAIAAABMXPacAAA060lEQVR42r29aaxs2Xkdtta3Tw13emOT3WyyOcicKYYmBQGSYIdIHEQx/CM/AkSBASc2ICBIguRXAgRBECEIjAxGICOC4yGWkSBxHMOOASOSEFCOLcexBkuRZUkkRXEW2ezpDd3vvXur6py9v5Uf+5xT+wxV93ZLyEWDvK9u1alz9vAN61vf2kTxQxKAJJKS+heHvwNQ/xELq2qxXizOq8W5hSWtolXGJc1AA0AGshIBACJEgGKgGWEAXQCcIGkABaH/vu5DoEEEXO5gcVcCBRgEUA4QDAIlEQ6ANIfkifL8XN1FAThIQXA3SHAQchcEEEjc302SJ0iAuxp546n2eBXjlcerlLblEJaD0w9p+TN8OHA09OUnR2/dX51cLC9W67vV4pZVJ2YLkvmvkuc3IE+UBJA05a9Gfjpr398PNQXRwDxP02/th1sSOHjK/DUABFn7tN3cEN1ogkoSkKclf6S9jiB0X9vdDoj26Sk5wXx9Mn9zMFL5eT162sbmSazfjPVTtffF/tbynY8WcT8THM1P/77+Y/3d5suZLU7O3rU6ez5UJ3AkT3IHHO1zdh8gALYPSYO6kW2nLy/28pXBTWM8AdT+zyIoSJKE8vYH/+zGoVhD+5Hv1gW6P/rgjYN7kPYrKd+JyuEDQQTjAmaets3mjd32dfeGBGB5OY4Wdzm2kjh6de5/AcgsnJy/9+T0edgipSglQpLYL+fxvmP7tGQ/r/nryMHEjyZ7uk+7e80rGt2+0YG3abjENLvx9/+Ut1th5g39K2x39tCWuFK/AwnSFmYLeF1vH2yvXpVivqlDdqV9cMz9dO9r/391ev/s4gMW1inW7olEHvduu9js6APt0xdLwPoJ6Lfa7A20K7x4QzGL80M5dWB59CeGdHj91lXwwGXVGrRiW7S30e778YfIUIW1e7N59q1m95jMy05TW5R/Qjlwo4UJiAy37n749OL9yT01W7Ed3/7Nk+VvpJGGfu113pWtT54xetPlP7thp8MNCJ2zbR02203X25zxBzuzli1P/xVzVx4YpXIp9K+hf0oRMAKgu9egrdbvsrCK9VPA84dGo5+vE/rfhquSgEJ1cvv+J6vl7Rg3hEjLvonFT2dq1F3ERnY0W/xitjD1RbMTM7sxilhApAHqL9OvsuxUphfoPJm6vw4W9fAbZ7ZO+7xUHwhwsGbZeh3k/Z3cY7W4WKxupfhMHkcrqf/nnBMmIS2Wt27d/7hcMe3MDLJyaPoVh/b71N2MTTxpu/anppCku09XwGxcIEGK3VdIcjLkRz0e541GmfCReZnbYZq6k25mPG9RgpK1ho4aOPHOcxNuYUXw8snXUvMsL52RqQxTuw9oubp1697H3eUeiRywY7gN+091DoBt4D/8MU5enF9Zxe8jYwhAcsDJALCzOftYtAwqZjZT91/n07hfruMNN3C8XTjdry3lcLm3EaQw4wk6k0SCTCkBXK2fS/GZe03a6CbDdPSrxfmt+59oR58s987UkhQjONgK3c9g7U9j4SOXnRqf7g0uHXvzdALaFV36tnkfPrKRHH6vBAc4Cn8PRQTqYj4pAVyu7qXmiXszevAwvF1aWNy5/ykX3GN3Exgtz+HCQvFK/87s+jmbB46W/HTU+mhnZJQk726bRxJLje4PLmWTBWYfMHH1B3wv+lU1iE2pscFUm2mOdqTlZEiSHGbL5Z1m97iMDkiGgauEbt/7mIV18l2/b4crmqMUujT0RVTKzmrP2PR+8kcLf+oDppZh5j1DU5MdIY/uiTknoaH9AYDSP4HS3uFP9h9Barqte49CQh7JdbVYN/XjcuEOTNDJ+XvXpy808crMhjtxGrxz6maxj4vGczbrGEem/0BAgj6fnDeAMyuiXInHwqqjRm/4Hqo0R8c/uHezlrPtLmJVUy0vBE/xss/R9k64CuuLux+JaTMYF9goxxkFoL2b1dgFocMnBkusG832DcV1JLnkXXw5SEdmn7mFk1qET7Or+HosjON7H5q+jGP5ga05/cmP0Ibd8DbVKP7sy+WtWD+R4t4J53ef3f6QVevsJdjBHBM7zonxaZEczsWOwwkY/LV4g/JaOGwZ5vFBtkCNDg1HaQTK1dDvjBGyO/zebuMeADNmHXAHH/TA1dijCG4MFpZN/Wb+iirHwtXifHlyL8ZtAZPlpALDIGGKnubEJEytSgnFuLer2MzcvRiywch3v1lhkOZQ8cE+m/fzhTP3qUc5kiqALghuJEDvsq75NEUFwgfIGFq0jsroldxHziKlxqrzEE5Tuso7gADOb38ghBNPDebcrJl1T8XpMkPndcv3l5NURj5Tuz+XB5S568iBg9A163A43IV38Ws/hYxNd7tlAu2NnTklKsPZbeDfmtYcBc7sylx4YLAqNk8AGqAQVov1nRR3s1WB2Zk/bpSOvL9MQ/pwc/L+3lscsg+a/ml0nVkEbRbLG2B87BNjlRM2iwPub7XYqeX3Hgg9II9hcc6wQgYYlus7gDlcxFxojOOJz6FRPmDWB4/t7uXbyumZiXqVcGAVDweo9+fjiZmZabqQhNT+Mr1hd3iaDHrOzNs3m2AgXPBEqU08DqKwkEfQFotbyNDNYnnbUxqPMMuQFm/35zjafGhKZvOyDmbUoR0mqVzI5XAfXgR5kgaf6n/cvdt/6iow6pb2/G0c383DSwGku1eLWwAqWqiqU5/eJV0gWrypLw+Mgs1BKYPDLQPJD9c4h/HM8Z3urZk9fKky5J98BafAPehF3DJGpNGWmdsHbAtqhLuyx8tVSmrG58/cA/exQw5ASBNiVZ0YF9ViccpqoabWaKU7W9h8/x2a2qIOQQJHVYwRrDUtIQ6G3gcF4EHYqiOupQ/DjrjKPNY9HCcfFxonAb5yqbiLZUSyBSC6qhyFI8VzdW65KEpNEMNc4q1WVi1OSRN06Ak1KK/zGFpWwGbXBRs3MktlGHrIak2HsnwlW5R+nnqzM1v/Yp8dTOwJwVlI4xD+eihS2E+zIMnCumI46YP0wQpqNxjnIuzuOqImwBDLavsU3+qrzZNUi9wn7rNP2BuKPT5chKrjOaDnmx+5hLmL7++xtxYjQPAI/DcA6WQARC9Tr7ZkweGdQAEKYVmFsC5Lw0UQzkkFRhN0AR1lA5xAEXmevS2J5ugYQk9GUBHC6iYuuoTJynrANNbu7k+HyE6jpJddqjgqPpNtOT7vCqOJaqkR7HdGhqnzWvDxWLDPLMYogCTasgph0eXko9neW9UOm+NkFxT5/WD50yjKvavkZPJBZ/usM/osneRxwG6uXI7DEU7nWqEj+HY7ixo4+TELrdgf6hKUfY45zsT3F2q/rvcnYzMiQGaLigy5zKM2tUPra/I+ku3LEZodFC8KTF0pnPBcD+j30SCM8Vm0Z64AMIvzaJokt2Fbi/bP0yamV56NnQZXG9YaQZ/x3prPw4+HRi3FBqzaRZmxN+0XdV8LKKzwNX74eD3rneVuhyLXuVfaASuQjJkUbL+BWm7boDpWsLVmpvnmQcTBkLQvdbbBuszM9lFVt2KpDJyxtGglo+3AKKeOz1eGoeq5C9MAf2RJ+sk+sPA1xHY0N8R7rGhu7fe2SMyIzTBUERx07L2o3kEgN8zvho8gWV+RQyJZdQt/CHO2TpjoUOmi1ngky2URlYtzrKYjz9P/7p2xnUcevQO6hDmGHbxnc2pKnBJzNjKo1nU5KmegqpvXcKYh0zBSaO3MsFxnlcBDAEvHxOWhqvpslDakj2mWhjX7nAX1YzDrc5cdOJWC8NOGfIfXqWasNvd+9R3lKzOGNOPHE5YRh9wAAla10bw0pmloJrecJAI8XnWazk35Tx9h5dwzkmciWxQEv5GRoYrkdn5k2MJg022VDmyX68d6bli8sxPeJ2TWQgD0vUu3zjB4NcLd1eIfPAw+38jzHKLfHgYmr/XVKu3gwIDMcXUHTm9gmgfXwfWp/cEH349yX3nXtD7d5hET5l0Ld1dtjcPbGrEgo+V/lhWVm1Sx+yyjr+mPcP+pbZ1kFQeHYP9xqI2bBVCkTwPBkk8HJZJ7WJAaxewDAjrZA4nTmsewUjQuc/Yl7sz5A9y9pavkjIRdVNmXvgVVRV03/92kDGAd5BNeizwf8g19MXLyhiPWY/8VrclihkfboRxBEUWY0MVIx5GfYWya79BdI0pWti0SmcPcotpc4BltIEv2L/qACT/wfG01sZoYRgo+DRoPuYFDac4UF5tlD5Zp7U1DaWHi3Mo39J/1WSs3goaGm1Kzb+iR4A5FK4MLDUGA/adGTiK75ckosep4VKMy5ACGK8kjU2il2302n+/MY7Y6bvR7dmsuB/RRcRHqd6jSpKmkxQllrXPeQ4vSvp9iwFnQhIEx52wAJZ9vRCjiOiljy1MvOFrB+e9VTwktnMl4PqaUI8x03sA9x3M2N6C4dsmX98dhUWFfKzXCKBdSUpPUDWN50XaXsItNiz40SBmV8m5gW2ey7yfgHpwiGazDHDuz1820Dcd0Px9qZ7ilU6jtXJPm0/4uCmJRtp+jsc/GM6MNZUZ3lk54dj9eO/p76oiK0TcToMtL7na2CnZ2poszN6IzykWwWqYKLUJJWJv1et851dEayD1tDB0kbua72q82OYC1fC0Orbn2r+wBc+xzipxpdyUdDfN09LwgoFzyslEgdd3AaVId08iGlyWdQ7HNTCGFewSSIfiTJxZs/YOf5r/4R/TZz8QX3xfPb8lMDgpI9CS6QWICIuBgBBMQxQhLRFRooAg0qCItiRFoaBGMUiKT2JBRlkSFO3r4zf/lx66ePLJQJegICta7inHgy4IiyByvDQsSUHWc5z30mewKizycx7Lw8hMW8bB8eKPEMpiaxLeenPzoH+V/8OO7H/rh7UkVd9AOaIA81glIQNP9LsDBGmyACKvBGoiwBla3bws1Qg1EMIINULezxQRLMPeqsubZl3dP3wi2niUU7TNbHV5S0xR8gN+z9QFTgt8Banhbmh/6H8M1LYbjsvhsUKjeHPewoMQQfLOpzk5P/9x/efmnfuyZoDeFtyIkJIMb3ZHESOXRb8AIRiICO7VDXIO1VCvUYMM84u3/NkR0RqoGI4KTCZTofnE7PPy1P19vLldn6662NoUGZbnxzTWq/8xGjM6xj+9M0D64Iw9sgmlkOYtDHA6xD2ZtBQIxoD/k0V+9cN/++l948IOfia8mek5ejKISkKREJFMtNkADNEKSGqAha6kmd1AN1mQNbcWUTRDRyBsguiVDBKIQIReT6Fqtl8vX//GDb/xftjz3FFsKhLSnTI7KWxyGpnMxy6Rkl3unVQ2LrhOWc5kBteNuo9Gf64O9aQEgt4kVgV33STNt6+Vzd6q/89cefuyjennHsBACoyNS2fJEIRJRaNjNAZFnIgqNoQa2QO2owRpWUw3YQI1QQ5EWpeSIZglMoiMI5rx7hgdf+guxuVpW5/J9S15J7DjS1nD94isMVNU1/12P8JTtBh0u5hMAoIDIDtzZlG/bLqKSi+XOoPBXf/Lhxz+q13eqFohAcmSHGfMEEI2y5UEN7ZCdKmqxIRqhBmpwR+6ARmrIHdQIEWrERh4ZksxlLksMYlA6XSxWT/7pq1/7GavO3RPpZCUzAqZc80UAxZlmmtHzmqagINTaohxmsJotUs+wKCYSBlPK/JFi1hSoGa4gR0lLCqZHj6qf+A/f+vwP+fdq5tGPRB76prX1aI0J82hqB9TUTqyBRtYADVSDu35KgCZvFDGS0RlhkUwKgCUsgIVw/5Sv/fZ/1zRPw+I5KZGLrjhRCCpkX4j5ns6i8n6keND+Uo2HqWUuDOzMtdDCO6hLZib4nkLS2lnQ6JdX1R/+/ubf+fH4WgKCGjBJKS95sJYaKJIxD7FYCw25ExpgS9TOmmiIKG7FWopgQ+Z5imAkG1gio0JC5TJpIS6gM1uebL78nW/877RzKdFC1ocw9XUrlpSLI/6PZAKswHbGm4Fk64THdEMCnlPI0s5MQaEb1ura5cIexFRbe2pRqx5dSQBhFZsd/t0f367XfCuCAQmKQlKeANXMoaSiMxp3VA3sxJqoaTW0NWQ/3IA7qJbV7bijAaOY3CIsMSRY8iBU4FJWKb37Fr/31Z+q66dW3QUI2Z5+aaa2aEsMyXEDC9OnAurRm4M7QIUJ6vdLb3B4yIwc6as+5HPUgbddBUoj/LL9SjO/2tgnP7r70R/1NxxuSGLqbE5y5aWd48uGiEANNOAuz4FQw2qyBmtnDaulBtwRjSMRkZZoLou0hCohOBaONbmkny4Wy/rrX/vG/0qugcQWKCtSGCOLiiyPJaUdzedAQGLGDooQBxx/usS+L/5Q7Ph2ykYQe2AyDSVkxp5HIWi7tT/xL8fTEzxuwIDEzuWiG27lCehinmx5wBrYgXVe+Mqjn+NR5klyt2SWYE5LrFyLxMqxBk9gleJ7z+13v/xf7eq3bHFXEmhG9gyz1gnPsggnXjfnwDzmBVq4qzoQNep48eu4pe+joCJhPE5Y78oRLp6u9fnP6ynQEK523Js+7AFjjvQzxkDkjHcH1uAOtlMecdawHAs1sJqMNKclmCM4gis4ls4VbE0svH7h7CQ9/cKXv/4/MpzLHZ2gV786RwnQtXVKHhjykgABqepFXTpqqhU9+ddHkOO/toSOLOsxYykPpMGWV5q2u/Dh74sf+iQei43loc/D3ea6EciYQc5726iG1hA1rBZ33r5SZ68LJjEhJDNXcJkrOBduQVgKK6jy+MLZybl96Wd/8c9ENwshswJaoF6D9qkSZzyG4mhmJfds2/yLA6Aq9qIr4s1X/SHKhjJwCwevpyiNcA5Y4G7HT38qrk/1RqQbaqEBWq/b+l4mIYnRUed4hqhlDW0n7IBaVsNqqIFFWWxBnpAYkgchOEyo5AtnJTsN1YtnFXZ//2d/+c+8efmKhQuHyECEnHUNRbkOwj7HS7Z9J0Eeo/53ENUegtj/oSdYX5/sDZf//spvdxbzp51YfO6zfgXshCjUUMM2eI9Q42wAVVyAJwgnYIPQwBqELbhAWIE7cAurYBHWIEQwIvvbRYI5KkclrIS1cEqE9OVvf+cv/r9f+YsxyezM4URFBiC0AOdMSf3YcHctGDxUD+lZzegz4YKoLCERWZxmVLHLea6PN0q2Od6RhHWQ1VwUBjQKtHISlqLj1q34yc/iCbijGsv2RA2QqMZpVbiD4DE8+Kq9/GU+fBmXz8y9SmLtObxh40pglDng8uTmyG1btSsIUTDHjni8e/L06W+/9ujXd/VTYM1QOUBWefn3Gkf7dXmzjqtCZKAr53c5ZsbYBVirPkgDKxXUX5YkfWLEPO+xmrKYPqpNz5bgi1dEek8E72n4AETDrq4+8VE+94f0QNyaamGXkUtHNLtTVZtXqn/wvzW/+DP1N3/XLy8ddS/eBKSO6OhHOiPmflYWbklJWWETodfmmUNybxCDcMCNnGyFgbChiAp9nXT/YUmJZgWq3dWZfNgf0GfjPEZIHpmaORNEWPBUh099JmlZPY1qjHUGMh1crG6D//iv7P72T9avvyqcY7XGySlZgVmP0ts5UAM5BckhZ1sEVl+bJJi5/J2MG11R6GrjnQDhXo5BnDIBZ81yX/fM7MNZUki7uIcfqgTvG1Z6FA0sW2XyfvBWJ2pf5CmZCpa7MeYGVz0fnTzcOgvSuPj4Z/0JbCNlvKF2C4tl9cD/8r9/9Y9+HuEOzl8iKrFqF5MgRsCpJN9lwVUhihlNKVghPXuu3bqe6WlEQBvqh1bVDnuNtXZAcUxcZ9DQcZjTNmpKVIfGVR294LBD72o5e1q3xvynwgnfFB0a6nSakle37tlL328PEHbwLbBLDMtl+N7uJ//k9nd+i2fvgy1lZwgrhCVZtR0pqKGIuJVv6Q3UIOWI1eUJcmNHUaH34cheA7QVJAldbsuRIEDH0zouaTtmdE/IXhpVvPtHb03QUVWRXqRgvtmqy581ZytT64RakTW12zq1NqBdELRUN+vve+/y4gO7VxVqYy33xWr5aPtTf3L7ld/hxQelFVfPcXXfFheoVqxWgMu38h2aJ2ieWNoo7ZA2SI15FKJ5giKRJFGOtn9DLW+B+Z+5XSdL0fEQ23VU/5hFhacslVlG895hmntOxOAihaH7PixblSV0O/av+r1XwrM9Tx2QWBLZfL9RsmpC3vRomvWHP4VmGS4bbwIanFw02//539t+5Uu8eAl2i2cv2vn7dPv70p0P4NYtBGKzw9M38fRVPH0F8XX4Y9SPUNfwnZSgRp5r8BFKgBOp5b73bEbCQavOssObH/2OUdTjQvOyRcZRP2Gp9zTCj7vOMpA9FCHckAB6EOufF9rsUmqy5/BgWPdtb8aw/PAPpLcQNuI2LS4W6ef+s2e/+vd464Oyc55/CO/+VHr/5/ADH/ngD9z96HtXVcKrD5rtg83uwaPtg9eazZP09IEuH/n2UnVUs0MTGZO7exPZuNwRxSQ4UXvmUhjJtN28/v+4Xx3pPVHRZlzuieEQe4nBlIM5UN4aD68qyFrFH3VyjF1ufC36obIZdRiCoq+j9rLLLU9JvWXNgr+QFFN1++7yuU9tHsCuFJZL+2d/69HP/zTPP4hwzrP38v6H/WP//Mf+9U/+6T+2+IEL3gbegL6u5XfT+uXdvdeefPjxMzx7jPox4lOkp0hX8EvoEtoCNbABdrCco23BHRDdmrTw6ry6/Oabn683T2jrY0qi7Pp+Crr7fog7jnsrXTXXPDLGksEgEqhaOexe9bwn2uNY6nFI334mC5u0AQEDgiDNfNesn3+J4f14HE2r6tGXXv+Zn9D6BS5u+ekLdu8j/r4f/NS/9tE/9SdWz0uvbsM34E+dD52v1unBFZ481rNHunqDu4dq3kR6Kn8mXMKvGm6b0AjbyAahFmv3XWIDkyvGFe5t4t/dXH61qu4ckdqawz5LgQOfkbEpRb+MmO1vzKwIo6Ve47Do+4VwpOxeJtwHwh7PnZae6ZuuGR5Ky68PSs3ypU+nTYVts7anD37mP6o3sovntLpvF+/zux+98yMf/+APn/3uMz1e2EWlSngmPIUuM9LjHqPFBnGnuHVt4HVC46x3qGvVwi6xdjTOOrKhRYQYLYWL9e7bj/6alKQkjZPY2Y6SMjjMjs9bpqKNBNhZhHg9+DDpcGlpKZ0k/ND37Me3w3emzfmjRpxRlJkj6pJUgRH6k8EW48VLn4uPZL549o9+4tn3vshbH1Q458m7dfFieN+H1p94/juPmQyhYpN0axXOKn73KtVCdO0i4g5xg7hV2jq3CZuITfTNznZJO7dtY7uEJlkUo1cJIcVTPufbv//08ldoF1Ikg3vaZwDDvoyZPu8u7yG7HqMBWWSff9DZ8VamgrS02eyJHcvd3eGti562MM51wbmGZ1UcECDat1Cqaez8bHX+ycWG9Zf+zsPf/Bt29n6EU6zu4PQ5XbxoL7xwtbPHT/CkCW+63n0WPvFkc/83vvtD1K3zUDdsamt2ORMQt8k3tW922tTcRWwjtjXrhrut1bU1sWqaRROrhPOgVx7/tHvqOgrm9KE0aHk8DMlxGqq2YfagkDwzaBVlYNleA2btoY5qmuucbW10rmFvDn3d5xtjM9X2jrNFggilen3vw9E/4K9++81f+2+weo6LUy7uYPUcTu7x/I5b1Tyrm93yWfTb5+HsF7/zn/ynf/M73/rKj3z2+/+Vn/rTX1lepJ1Um7YRm+S7xDpx22DX2C5iF23X5AplFb1KXCSv3M+q+6n+5YeX/zfDWdcmZi0lfmCmJwtfewnvwTuHdacOw2CXuk5pbS2j3LQ//2Kgs3ZIo7VzrTNMvX1mME9EFPYNaOrEhKhUn734g6FZPPyVP1tvnnJxT+FMi9taXKg6x/LEXKhdDRD4oV390//tF77+5d+APf2Fn/8Hv/mX/o+Xblm9c1xGbhI2kZvadk3YxbBpwqaudruqUdX4MmmRfJHSSliKt8lX3vorUCykjdF3ZR2HnYcyg8NUmPOqvocje1a98Zpt4ELXLNzPYNlGXNC1fU9qUV9jL5d/W6KRSzLQScnz6kq33vNHm2/94pPv/cNw+l7ZknbmdopwQltBQS46mHhSGZ/Urz+5CnfuoHliZ3r4Rv3uLdIGfCY8jbyMdrXjJlrtqhPrFCKqJlXRK9fCbeGo0Jzb7dp/9fWrXyBP85kw6Biu5MFKy3DlqZeq7/WD3ItPURMYuGAyFAQ2K4Ufu3NRqF41PJ8cNGjfHyWJ3p6B1ClDleKu+8XSzwQBpr4Y4B6rW++Svfjqr/5lLp8DT2GnCmcMa9oatqDDXEtyEXjSxB+5f/qxP/y5tH4+nNzy8K5P/PBnHl8ivAVeKVzJto1tEreR2121a6ral7Uv67SMvkpYulbytdvdxfprb/15gcaqPQ2kPXciTBfsWF+IynaJR0XxZjGFLioFW0Eu7rU4+kvNqCCVScShSvScvsCRAl4nRGJKm/X9Tz/73jcuH3+Vi/sIa9gpwinDCaolw9JWyypUAfaeO/q37vHzC/7n//Zn7734wq6xf/Xf/OPpj/1z3/uGn17Rnni4aqqrGBoLO1W7uIhaJSzrtI5YJy6S1o6F4vOL9728+R8ebH4l2GkXfHOkinqMYtM/JmcEN2eFuEbHPIyi1apwIAPwpzuaoVNNljiehEJrgYMu1OEvYyLQIMhTWp1/5Om3f8mqJW0BO2E4Z1gjrGlrhgVtWS2r93/A/o2P8I+cYQu8+44tgml79cHPvecrl4v4SoMnHp421WVjW/dtwzpaRGiCpWblWLgqd0u+lD2//MBr6W/+1qM/ZzxxCgjs7M+1MMxMvtnKqNtEtnLQstGj+D1rpUeODah6YBrT0yLmAE728IPmyUJj1VrqoAdD4vIk4f7mrX/C6oy2hK1kS9iCYSVbWVhX5+d/6Ptv/Uufqz584s8ini2r//OfPnr86oOFb7705W/z/ufwIOlBE57tfNvYrk67rTUp1ERdV02sIqqklda3w62zsPvG5r/+rbf+e3Kh9iwIHugFwrVo6KjRZdotMxpJmu05hkWDbdVGJp1M0M34boKuJ+EW3zR/QVcd1i/sNrU3lwzn4AK2NFsirBVOrDo5vXv/pc+869OfWr9n5U3E44A18Gu//nvpyStWX169+eT0DaTXantS42m92K1XuIuwqyoPQVbVS6bKsExXS735uP7Cbzz5nx5sv0ietuEOAxlwuJ/iEB9nOA1U2dNwiDO455OPT6CreqhyThe6I0JqhLLZ6BSCGQvDvrn5AIWURGq4fjHuroxEWMNWtCXDUrauVhfn73nxPZ968aUPLO+cCMKzBBov32z+yS//tl89TJfby++9fvHI/VGNp9tz3db2q89e+bnds2+j2TGmtl9Q2139yrPmG5v4AKDxXMwsz370jSQZrl124+WfvajNK4ke5E0NJoWiqrZAbweUHjijQVUi/jclQ4+aIDvpRq7ek+qnVp3QlrIFbMWwWpzeuXjvi8995IX77z29fU5LfrlFSNwo7L771sX5yYc/9+nLN149v3eKZ5d6cnXK25ff/evf/Gf/Rb17NVclR0QFcGE87xgKAQg0dsQ39DnQHKbGWdtyxEQf8hmzNTUWRflJM7GGRMNxQ+SRqMvL2kyLaXCg39T2Ddpa4d2ID2ErIdBWVp0uzu+dvfv528/fu313fXEaKiFu/TIwLchnkdXtf+HHf+y7r8bLp4mX8XtfvDrTre3LP/uVX/uPYZVVz+UuvRxrc28rve0dZiDaCvDoaLNDVbDpEm6LUXsS1MEy/RERh46GYpVAwqlBB98MxQ69Ion3WMNIOnbfO1hK4xRNuKX6rzxi+S6Fe9QrsAVtyepkdX7/5P4L5/fvnt9dr09Dxagdmo1tEhuDGj59E7/3pe3la3Vzpd3jWle68Fe++Bt/lrYC4d50TShjgwiY0aZnfEzFx8tRnsrzlGH6qNo1Xe+HJrWrFQJtozZ0gE56yKSIBfp67NzVfvmNLaDJr8LqJSQQznDGxeni/N763r2TO7dPbq0XKzNF1Au/8saVQgoMaYM3v7vdfO+ZLqM/TXjWXPDuy7/z09vL74bqzFUPv3lyQE1/1ErJe8BMs9vxkxZnpcYP2duRhv/ws8zMOAFBLJVL9xIL6E8QGwl3tDXuyQ3Rb9K1kTWEuX5JqQaXXJwszu4sz+4sTk6WJ1W1CIFSk5pNXStpYxaI2Oye6OnvbeoHm+Yq+jO3tFT9je9862+zWrsiup5ZhjmGSNsI12ugHsy8jpOfcVi3BHPNo4eA4fZQGanaqyVP+eKSsk71AbmIubE+JMQ6UtV3hLXW78Pm0lZ3qtVZtT5fnp4t1yfBjO6+i7FqGoq74FVFoNn47tHu8rVd/fAqbhpscVHdeuVbfyvWD21xng/Zyxa5kxmeaIChPIALOCAAVuh68jgH/YjTnnUGsxer6OwVvfpzYzoOIgw+NZGjUx2GJ2qxL/ROiFlF5uYRyztc3sXuO7ZcL9Zn1Xptq6UtKpCpaVQvVIU6eTKL3DEpbbR9sN28fhmfNqEhawv22itv/BysUns62v7ouD2rb38b1kHke355WQKbVDtUvvlQCnakWeMGFCkCrLxQE26Pl245wQ5CDHLnUOD0QHTV5yNyH8VLHFfbFHnyfuMiVAzLs7BaV8tVqCoCniKwUJPi5c5CiEDjiRG48s0bl7u3NtgmNbyldz968oXN9ttWnfSEyeHJD5wGjtMTxEd6QbPj2L8ylOIbc+XevqKqA71aypyMWHGgjnC9biow1AnGQB2qhLiNSrr9EQuyahGWKwuB+YwGd8m9jo12ycxISMGJWs2bm93DS3+WtBOj28Jfe/yFUpVpL/rFcXQ/y+MrW/WLrezT2cIB6empoZ/IKF3/U0mpPza9aJfo0i9PmqB9M5sRaZaX2GsDDuOj5LYKFx9gfWmLU5AMFVnJ3WPDhhFUSiGrJzvYuLYpvrWJT3bpKlkMaz+P228+vPp12Ko9VYGUQkE8PiajMO0zHM7B+DjiKc54KOc6dGrz0QkoymFDGf1e01s4MAcDdu1E36yrxWtIw6V7g9N3hfV7uH0ZoaIFM0ieJ0ASosvoEJxIzq2nTeOXDTYNa6nxVXju8dUveHpg4a7QduNOT76c7sVDFa65VzDR5Lsmscexs34GdK5CEkuZljKHKxROaZp99EM8MjK8Jl6iYFRj5x8KCDQxhEzqIxxpJwQCyWOrQJIc0bWTLhttErbOaFUyU/Pq1c8Di/zFBgKBtK6piBJGOmY35/3tjwKfObKOs9N5RGN3Vup2jxGQ1Z63fl3GMVkvmW+cz9EyYf74pi5l6y3ZQtbg4v2Wt7pl9Xj32DDQ3ZE82yyLkjsitYu6argRa1iygNuX8Wtv1V+kLcWEDGq2TrKvrc/Ei8fBzsKgX39a5BRznoaFU3M0EZKGA1XWAeSBEtqhXLyn4nZv4zFuOgE3wGCBYQlC1YU8sj9iJNa06FqSLjTmSHJPjsYZkbYRm2Q7VWkNpRXWD3a/JL9iuF2QGPrzvDm+1aNp7fQgiNnT+Y7P2az7nZX5GSD6Wa4GWTu66GMabZlZS9eBXJZTXyEdwwUVFAhUZKWwAJ2+yxUhusDoSZAF0Um4u6CYmNyaxAjsXLWQwNRUWtM2b+z+IVghFzX3zBsrx+TtdpPfXGJnamEOqWEfzwEIUJkd3R3qcijVPnQKs9Rznw/1v+dDQQNpYgVbMiwRAptnUleh83zmolLaijSZsumPOSgCGzEKsZJv1/bcm/WvXMVvml2IIkzqITbMpq+zB56XhpQFI3YikMe5QzcGSOfbkg7oUg0rMuHiKO9pyDyr7D/GNMZk1cLyqgINRqKCLVAtLCzAtW9fodfGBRTbxMAFTyJcwWLKjUaIrgZonElKbrht2H13+zfARWEwzA4ctH7kDNqpEuHEQKlkc47i7+MiTYc2R/dLqaAHYwG0HTpw6FDnDMznYSZZ+x+MIFDBFgwLswW5QFgF32H3HSwv3BtCiA1ShEvJ1TQek6eIFNEkxAbR4QhYnvD821d/aRtfpq1EqG2rC8VJZdc2k2YKYvnf9QZnWo88sBavOdSt+2wYVosORE7zSGwh+10odO6PNuHoyFsSDLAKYYGwIBe0ymxh4UTPvig9XJw8D7kUIZc7UlTceqy9jh4bRLdEigucn/HWy9u/+rD+JbPzTMUvdaenh65r/vwH7jWlb0BAeRsslcPq5MPfB5RDslVNxPRA+nm/Qfc9uarAqTMBWG0bt3KtFUYzt4qhglWGhUIwC7ks5URz+Vt2+rGwuA8lpCQkpgSsTEbI3AKs4iLQt+krX9/+3U38lvHMISIYDahwgM8ztwyFuSbZI6TBayOfmzQOHY/pcxSkcidNfU6nWS52lBQMpYhzmyqcpLVDryCD00Azq8CKDDAjAy3QiBDMKrhvn/5mqO4FnqemMXc4FKWmZmoYZSml5vVN881t/DaQmIUcYDRi37F1EInsG/O703m6Ot5c11yBIHFu38wPDt72yQ8qz3sUUI1OzT1ML8U0Wx6JteZ+x+4seoIVWNEWtAWsogWwAiplIQDQgYAlmsd1ei2lhrH2uPG08dgo1SldKW2QdpCTSyE3s5cqMnsA7hA+08qQD7VSj5Z/OalhXHuG3tv9KXqb5NU0/xrys7uDQ/t5KrUi+kM+mQlihAKNpIEBFtjNASzQKoaFrKKRDB0tVZJgITiESARiacz97EshC/k3QpPHnSACKRs2lrLTj/WSrnNDKZPiUXhgvDRylrPXvDlPdL902pZzDU+PRnlIrThX5h1RPLvs0dg241k74qxggWYIoSXAWh+25/K9S5JHee2KUJJHeSNFIHURS1745ReVVfUhPZujavBNu8Y5eyQjruHKHamsHYQFaPseXuZ8sj1ft69glEdC5BqN4FYy3fYHj1ooOhcCzEADK5rBKiEYg7rxUiZet8x0Qrn9xpUiUkMlIQFRSlCSe7vdDC2BbJ/d2Sh3KSKQshh5Q9WOEn8ugWEeh50P2aIi2pkGqdYtl9xDo0rUCECXRu6FcLaLXTPaBG2nNY0w0cRAM7ISKtCUVz36XnuXQAX1Z3+nRI/yvPajPKvEucFT2xlqnJSfOhOkKaB/7ehr7kid7lOOItY45FpuYG1SC9ROcCeVJ/20tBRyVrH4mgknxVI/35TZdnkTsRe9sCw3SLNWlEkEIwR5kkRvlCKU6NE9UlFKUuyPZC0U6DASTThq39+BeyQmNfAbutw5gOAQwFy+7lUpi37g+9QXvPYgUot/5pjEWm0v5iEPYtVqPjIoc0CYT1rwfMpn9wUuT0i1vHGv4Q1TA09ZbAZ0ugAjfch7LSPF8nRFn/xyvfmehJ7hZibrEOfVu1OURuGsFzS6ksOgasogPxY+9Tvd2OZcaJMh0MxCeQp75yS6Hk3JGNUKr1CSKcKTvGaK9Jj3gRShhvAsVj5sxR/XGm8oFH4DKPTanVGS0g45Z41Ouzo07+WKr6R0KMaaXqHzAUJGYNRaf8+NN2Cr+NElDZkekqtnyHpn7IMutSOeari7GqnJvlfeehuwX/Lq4P7B43HYV/IOJuCaQ20naE1nxO1tRasHCV6KFTwhVH2Xy0GT2ku55iFWn4gGgMbsdQmaELqRckGUEwal7CBccsBSklJC8hSRRWVy6Ompo5J6Qbq3WY9aniAxJ1FrN4mCupVohw3XyDjbEZLP4TRiWu/KuhBeedqGcAKOv222VL2v6/Zcv4I3R9JBwlDiYnJ5d4BpjqgUXYAcqYGSEKkId+QX4TxKvj4ADHC4FXjzHfBOJWrfibkbFUqTN5WnTcW7g3lUju+6NExDvwFrIc82sDG14Iw6NFToad8dLaU4X02Cw5PcoWRy9wRPjkTPRwQkZA0JarK+fGSRh0vErrUDw1V17dBzDpk4bqAOhr8j60ICMPe6is3lUo62X77t//M9/93QUw3azxW6XqL6DdAelZj/LdIgdmoK+0Km3AFHSoAcDk/wrC0Wc/CTu4cPxJS82YrWcPg0DJl041BVc354dkp65MOPI4PlzEnwVFcpbt0bMghNKfHRPowPsnXSOiWcDncbgNXIyt9dz0cfU/fElkS4uwOJkrlLTY76pdie6nWYFHvTYGEwWzx8LupNIigNd8OUgKwydT2ODA5CKZjUuJpKkDeXtryNCHJfXO92Q6fUmhUS+jDTij6pQYXNQVDWdqrAOpZOkjs9062zoIfDM/aQoNQp8OkAh5LF6PuB7T962w3dpt9sUn1uK7CDqvh2vQGr4OkZJAPQNE/I0B0KeHRdiIPi2KhaJsHVtk61fNNcXPe2n0BdR22K8OjyPujsWAGDFOs686pDr4yihwP//YH8jJGPI6dGlR8ymsdNuzpi84yqGRYOtzxS+w2VFVIwwqK7cy80qjJAWWI/QQ53uZQSFOGy9ugth6f2gAklKMqT4KToMEI8UqgaD3enMTOdAz80AcVH/MbLf14WqQthxzJa8zQsFQrFrKDoccusl5l95nJ5O8a6tewd16bbD7nAwo5l35+xyQy09bFcGyCpO+IReeF7NkPwCCUosj1uNh97l+htr7I4OtR138nVc/+LButOYf7tID/X1r2P5U3D0Kis+RyBpybdqaiqdWzeSmkLdKS+lLbL9R1YcDm7QzD3zSbcl7raKMqsUwsJfehTnHfprYh93iXei8c5MtQszzLDkqTIvjuBZZTGsvw5CR9/X/H726XzHwpe31bVoYviK6PXuwct9tStXpfH5fpeSjXzaTVtoGntuusQn3bd5UaYTnGxjRDahEttx4G3zcBZHRlyKAneYm0tvS7tpVv2y9+HdoOFKjeKdeDv1JrzgGeef71Y+zaZ9WtuYMLQVlWt691D96w83qrkA2BK26pah+rMvSn6wsoCzUA3xWzUSeVoZahz56s6x5v3Qer6+lzuhLfg6MzoX+/0brjuZnn9R1Gjm+dl8y7huF4MqCqcuK6a3WPMoa9M8dlqdU8I9NgJ6TLXHAemlq0JQic6yi5WRSfKzGzK6JBniS9IYuqOVBbodG91cqi3ORAzTu+I3TjSHPD7CXhuUJMozZ2MCyN2m9dKGxgwEKDwFK9WJ895q3FlXe5bNkparxTVVWTUTkJvNCTrTiNnK1csIcE9Rz/W6pqrGFIVqU3pb0vjMD3J/Z01Z71zOOfa06jn3DvzoVghrHbbV+RNmR6O6g90bzxtVifPOxwdUr3H3fplV1x8D8q3Qrmee7t6Flr3f6lLklvnXBwBP0pZyz6v3u4bif/fRvtthUlDkIczNFNWi7Cqt6952ow+FaYfTmnnabs6eZcEeeoa9rSfif6MpVKppeMt9qJ82S8LDnQOgN5G4q2f7vWAiRnpaesLkGzr+GFAkPmDHvEjfduHGlQP2f2i5OJkVYVlvX0jxcvplcO44iKQltLG07Pl+j4Rktf9YWYYnkIA7kOevtG13SaZqQjv39Ebeu5jVR9mrfvovj+YdU9+AcsXC8f2BwMnT0lEh0Q8pgyJ0dBzH0Qr2Mos1NvXUrqa/Xgov29/oAuZUh3rJ8vlabU4c28TyH1+0BlEtudt9M/gw1xfguj5jLnMhxD3LR49bKBhdN/XVH0S/Iyt8M36Wd7G2p+eUzKajJ4XPcuwaz0BRLKqVlCst6+572aNFeaSulJ0QABWJ8+vTp93R4xbKaEtubTLv8tFVbYesD9nGP0hIt4apCIjL4bSp6FegSD62wTOrrEtRxrnjluk4+eFl1ezsCTQ1E9i/WgWlN1voCOoaTY7giwsVycvLBZ3XEjeyBt1pXnCtD/OO5cB8hr3bgLQh0ZZkLdwvNOoZja//X1NwLWZAW7QCXxgbvrT17x1jFYFWwCe4lWs3/RWQ+EILg0eB0zKPWFhtVjdqRZ3EZZwz8w1tYcY9YWEVMKlgg9EkV3FzjgU4WkSm/mkNqtpG/u0cjk6a+QQRYe0w700GuksFEV863lERiMNpDx6vGri006+Yp5bxZES6CEBiuE/2/CDsLA4q5YXVTilrdWdh100Tfa6Tu0EoOOeDr5Wyo2Wag/uGsm3l75ZpQRQb7s4KB/t1e0mWbKK8iaReVA9mNnVrWmcrT1zPwGtlokEs15mjqRctaddihtP2/ZJD8jVTE+h+f8AVQunOHZFKlkAAAAASUVORK5CYII=" alt="FaultPass" style="width:100%;height:100%;object-fit:contain"></div><div><b>FaultPass</b><small>Subscription center</small></div></div>
  <div class="top-actions">
    <span class="badge success live" id="liveBadge"><i class="dot"></i><span id="liveState">سرویس آنلاین</span></span>
    <button class="btn sm" id="themeBtn" type="button" onclick="toggleTheme()" aria-label="تغییر حالت نمایش"><i class="ti ti-moon"></i><span id="themeLabel">تیره</span></button>
  </div>
</div></header>

<main class="wrap">

<section class="page-head">
  <div class="who">
    <div class="avatar">__INITIAL__</div>
    <div style="min-width:0">
      <h1>__LABEL__</h1>
      <p>وضعیت مصرف، اعتبار و لینک اشتراک شما</p>
      <div class="chips">
        <span class="badge brand"><i class="ti ti-shield-lock"></i><b class="ltr">__PROTOCOL__</b></span>
        <span class="badge __STATUS_CLS__" id="statusChip"><i class="dot"></i><b id="heroStatus">__STATUS__</b></span>
        <span class="badge"><i class="ti ti-calendar"></i><b id="expires" class="ltr">__EXPIRES__</b></span>
      </div>
    </div>
  </div>
  <div class="head-actions">
    <button class="btn primary" onclick="copyLink()"><i class="ti ti-copy"></i> کپی لینک اشتراک</button>
  </div>
</section>

<section class="metrics">
  <div class="metric"><div class="metric-top"><span class="fi"><i class="ti ti-chart-donut"></i></span><span>مصرف شده</span></div><b id="used">__USED__</b></div>
  <div class="metric"><div class="metric-top"><span class="fi success"><i class="ti ti-database"></i></span><span>باقی‌مانده</span></div><b id="remaining">__REMAINING__</b></div>
  <div class="metric"><div class="metric-top"><span class="fi"><i class="ti ti-box"></i></span><span>سقف اشتراک</span></div><b id="limit">__LIMIT__</b></div>
  <div class="metric"><div class="metric-top"><span class="fi"><i class="ti ti-percentage"></i></span><span>درصد مصرف</span></div><b id="summaryPct">__PCT__%</b></div>
</section>

<div class="stack">
<section class="grid-2">
  <div class="card">
    <div class="card-head"><div><h2>مصرف اشتراک</h2><p>مصرف واقعی ثبت‌شده روی سرویس</p></div><span class="badge"><i class="ti ti-refresh"></i><span id="updated" class="ltr">—</span></span></div>
    <div class="card-body">
      <div class="usage">
        <div class="ring" id="gauge" style="--pct:__PCT__"><div class="ring-c"><small>مصرف شده</small><b id="pct">__PCT__%</b></div></div>
        <div>
          <div class="kv">
            <div class="kv-row"><span>پروتکل</span><b>__PROTOCOL__</b></div>
            <div class="kv-row"><span>محدودیت IP</span><b id="ipLimit">__IP_LIMIT__</b></div>
            <div class="kv-row"><span>محدودیت اتصال</span><b id="connectionLimit">__CONN_LIMIT__</b></div>
          </div>
          <div class="progress"><div class="bar"><i id="meter" style="width:__PCT__%"></i></div><span id="meterPct">__PCT__%</span></div>
        </div>
      </div>
    </div>
  </div>

  <div class="card">
    <div class="card-head"><div><h2>اتصال‌های فعال</h2><p>دستگاه‌های آنلاین همین لحظه</p></div><span class="badge __STATUS_CLS__" id="statusBadge">__STATUS__</span></div>
    <div class="card-body">
      <div class="live-num">
        <div><b id="liveConnections">__ACTIVE_CONN__</b><small>دستگاه / IP یکتا</small></div>
        <span class="fi lg success"><i class="ti ti-devices"></i></span>
      </div>
      <div class="kv"><div class="kv-row" style="border:0"><span>Session فنی</span><b id="sessions">__ACTIVE_SESSIONS__ session</b></div></div>
      <div class="alert"><i class="ti ti-info-circle"></i><div>هر IP فقط یک کاربر فعال حساب می‌شود؛ Sessionهای فنی جدا نمایش داده می‌شوند.</div></div>
      <div class="actions"><a class="btn" href="__INFO_URL__"><i class="ti ti-info-circle"></i> اطلاعات سرویس</a></div>
    </div>
  </div>
</section>

<section class="card">
  <div class="card-head"><div><h2>روند مصرف</h2><p>تغییرات ثبت‌شده مصرف اشتراک</p></div><span class="badge" id="chartState">در حال همگام‌سازی</span></div>
  <div class="card-body"><div class="chart" id="chart"><svg viewBox="0 0 900 190" preserveAspectRatio="none"><defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--fg-brand);stop-opacity:.22"/><stop offset="1" style="stop-color:var(--fg-brand);stop-opacity:0"/></linearGradient></defs><g id="gridLines"></g><path id="areaPath" class="area"></path><path id="linePath" class="line"></path><g id="chartPoints"></g></svg></div></div>
</section>

<section class="card">
  <div class="expire">
    <span class="fi lg warning"><i class="ti ti-calendar-due"></i></span>
    <div class="t"><span>انقضای اشتراک</span><strong id="expireStrong">__EXPIRES__</strong></div>
    <span class="badge __STATUS_CLS__"><i class="ti ti-shield-check"></i>محافظت‌شده</span>
  </div>
</section>

<section class="card" id="linkCard">
  <div class="card-head"><div><h2>لینک اصلی اشتراک</h2><p>برای وارد کردن در کلاینت سازگار</p></div>
    <button class="btn sm" onclick="toggleQr()"><i class="ti ti-qrcode"></i> QR</button>
  </div>
  <div class="card-body">
    <div class="qr-wrap" id="qrWrap"><img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=__QR__" alt="QR"></div>
    <label class="field-label">Subscription URL</label>
    <div class="input-group"><div class="url" id="subUrl">__RAW__</div><button type="button" onclick="copyLink()"><i class="ti ti-copy"></i>Copy</button></div>
    <div class="hint">این لینک را در بخش Subscription برنامه کلاینت وارد کنید.</div>
    <div class="actions">
      <button class="btn primary" onclick="copyLink()"><i class="ti ti-copy"></i> کپی لینک</button>
      <a class="btn" href="__RAW_URL__" target="_blank" rel="noopener"><i class="ti ti-external-link"></i> باز کردن لینک</a>
    </div>
  </div>
</section>

</div>

<div class="footer">FaultPass · وضعیت و مصرف به‌صورت زنده از سرویس خوانده می‌شود</div>
</main>

<nav class="bottom-nav">
  <button class="active" onclick="copyLink()"><i class="ti ti-link"></i><small>کپی لینک</small></button>
  <button onclick="toggleTheme()"><i class="ti ti-sun-moon"></i><small>تم</small></button>
</nav>

<div class="toast" id="toast">کپی شد ✓</div>
<script>
const SUB_URL=__RAW_JS__;
function fmt(n){n=Number(n)||0;if(!n)return'0 B';const u=['B','KB','MB','GB','TB'];let i=0;while(n>=1024&&i<u.length-1){n/=1024;i++}return(n>=100?Math.round(n):n>=10?n.toFixed(1):n.toFixed(2))+' '+u[i]}

function showToast(text){
  const toast=document.getElementById('toast');
  toast.textContent=text;
  toast.classList.add('show');
  clearTimeout(window.toastTimer);
  window.toastTimer=setTimeout(()=>toast.classList.remove('show'),2200);
}

async function copyLink(){
  try{
    await navigator.clipboard.writeText(SUB_URL);
    showToast('لینک اشتراک کپی شد ✓');
  }catch(e){
    try{
      const ta=document.createElement('textarea');
      ta.value=SUB_URL;ta.style.position='fixed';ta.style.opacity='0';
      document.body.appendChild(ta);ta.select();document.execCommand('copy');ta.remove();
      showToast('لینک اشتراک کپی شد ✓');
    }catch(e2){ prompt('لینک اشتراک:',SUB_URL); }
  }
}

function quickConnect(deepLink){
  copyLink();
  window.location.href=deepLink;
}

function toggleQr(){
  document.getElementById('qrWrap').classList.toggle('show');
}

function applyTheme(){
  const t=localStorage.getItem('vw_sub_theme')||((window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light');
  document.body.dataset.theme=t;
  const light=t==='light';
  document.getElementById('themeLabel').textContent=light?'تیره':'روشن';
  document.querySelector('#themeBtn i').className=light?'ti ti-moon':'ti ti-sun';
  const m=document.querySelector('meta[name=theme-color]');if(m)m.setAttribute('content',light?'#FFFFFF':'#0C111D');
}
function toggleTheme(){
  const next=(document.body.dataset.theme||'light')==='dark'?'light':'dark';
  localStorage.setItem('vw_sub_theme',next);
  applyTheme();
}
applyTheme();

function drawChart(history,limit){
  const line=document.getElementById('linePath'),area=document.getElementById('areaPath'),grid=document.getElementById('gridLines'),points=document.getElementById('chartPoints');
  const clean=Array.isArray(history)?history.filter(x=>Number.isFinite(Number(x.used))).slice(-144):[];
  if(clean.length===1)clean.unshift({ts:'',used:clean[0].used});
  if(clean.length<2){
    line.setAttribute('d','M 0 158 L 900 158');area.setAttribute('d','M 0 158 L 900 158 L 900 170 L 0 170 Z');grid.innerHTML='';points.innerHTML='';document.getElementById('chartState').textContent='در حال جمع‌آوری داده واقعی';return;
  }
  const vals=clean.map(x=>Number(x.used)||0),max=Math.max(Number(limit)||0,...vals,1),min=0;
  const top=14,bottom=162,height=bottom-top;
  grid.innerHTML=[0,.25,.5,.75,1].map(r=>{const y=bottom-height*r;return `<line class="gridline" x1="0" y1="${y}" x2="900" y2="${y}"></line><text x="0" y="${y-4}">${fmt(vals.length?max*r:0)}</text>`}).join('');
  const pts=vals.map((v,i)=>{const x=i*(900/Math.max(1,vals.length-1));const y=bottom-((v-min)/(max-min))*height;return[x,y]});
  const d=pts.map((p,i)=>(i?'L':'M')+' '+p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' ');
  line.setAttribute('d',d);area.setAttribute('d',d+' L '+pts[pts.length-1][0].toFixed(1)+' '+bottom+' L 0 '+bottom+' Z');
  points.innerHTML=pts.map((p,i)=>{const h=clean[i]?.ts?new Date(clean[i].ts).toLocaleString('fa-IR',{hour:'2-digit',minute:'2-digit'}):'';return `<circle class="point ${i===pts.length-1?'last':''}" cx="${p[0].toFixed(1)}" cy="${p[1].toFixed(1)}" r="${i===pts.length-1?5:2.2}"><title>${h} · ${fmt(vals[i])}</title></circle>`}).join('');
  document.getElementById('chartState').textContent=`${clean.length} نقطه واقعی · آخرین مقدار ${fmt(vals[vals.length-1])}`;
}

async function refresh(){
  try{
    const r=await fetch('/api/subscription/__UUID__',{cache:'no-store'});
    if(!r.ok)return;
    const d=await r.json();
    const lim=Number(d.traffic_limit||0),used=Number(d.traffic_used||0),p=lim?Math.min(100,Math.round(used/lim*1000)/10):0;
    document.getElementById('gauge').style.setProperty('--pct',p);
    document.getElementById('pct').textContent=p+'%';
    document.getElementById('summaryPct').textContent=p+'%';
    document.getElementById('used').textContent=fmt(used);
    document.getElementById('limit').textContent=lim?fmt(lim):'نامحدود';
    document.getElementById('remaining').textContent=lim?fmt(Math.max(0,lim-used)):'نامحدود';
    document.getElementById('meter').style.width=p+'%';
    document.getElementById('meterPct').textContent=p+'%';
    const active=Number(d.active_connections||0);
    document.getElementById('liveConnections').textContent=active;
    document.getElementById('sessions').textContent=Number(d.active_sessions||0)+' session';
    document.getElementById('connectionLimit').textContent=Number(d.connection_limit||0)?'حداکثر '+d.connection_limit+' اتصال':'بدون محدودیت اتصال';
    document.getElementById('ipLimit').textContent=Number(d.ip_limit||0)?'حداکثر '+d.ip_limit+' IP':'بدون محدودیت';
    const statusText=d.active?'فعال':'غیرفعال';
    document.getElementById('heroStatus').textContent=statusText;
    document.getElementById('liveState').textContent=d.active?'سرویس آنلاین':'سرویس غیرفعال';
    document.getElementById('liveBadge').classList.toggle('off',!d.active);
    document.getElementById('statusBadge').textContent=statusText;
    document.getElementById('statusBadge').classList.toggle('off',!d.active);
    ['statusChip','statusBadge','liveBadge'].forEach(id=>{const el=document.getElementById(id);el.classList.toggle('success',!!d.active);el.classList.toggle('off',!d.active);});
    const now=new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
    document.getElementById('updated').textContent=now;
    drawChart(d.usage_history,lim);
  }catch(e){
    document.getElementById('chartState').textContent='همگام‌سازی ناموفق';
  }
}
refresh();setInterval(()=>{if(!document.hidden)refresh()},10000);
</script></body></html>'''
    replacements={
      '__LABEL__':escape_html(label),'__PROTOCOL__':escape_html(protocol),'__EXPIRES__':escape_html(expires[:19]),
      '__STATUS__':'فعال' if active else 'غیرفعال','__PCT__':str(pct),'__USED__':escape_html(fmt_bytes(used)),
      '__REMAINING__':escape_html(fmt_bytes(remaining) if remaining is not None else 'نامحدود'),
      '__LIMIT__':escape_html(fmt_bytes(limit) if limit else 'نامحدود'),'__ACTIVE_CONN__':str(active_people),
      '__ACTIVE_SESSIONS__':str(active_sessions),'__CONN_LIMIT__':('حداکثر '+str(conn_limit)+' اتصال') if conn_limit else 'بدون محدودیت اتصال',
      '__IP_LIMIT__':('حداکثر '+str(ip_limit)+' IP') if ip_limit else 'بدون محدودیت','__RAW__':escape_html(raw_url),
      '__RAW_URL__':escape_html(raw_url),'__INFO_URL__':escape_html(info_url),'__QR__':qr,'__UUID__':escape_html(uuid),
      '__RAW_JS__':repr(raw_url),'__INITIAL__':escape_html(initial),
      '__STATUS_CLS__':'success' if active else 'off',
    }
    for k,v in replacements.items(): html=html.replace(k,v)
    return HTMLResponse(html)

@app.get("/sub-all")
async def subscription_all(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)

    async with LINKS_LOCK:

        lines = [
            vless_link_for_link(
                {**vlink, "label": f"{vtag} | {vlink.get('label') or 'Config'}" if vtag else vlink.get("label")},
                vuid,
                host,
            )

            for uid, link
            in LINKS.items()

            if is_link_allowed(link)

            for vlink, vuid, vtag in expand_outbound_variants(link, uid)
        ]

    content = (
        base64
        .b64encode(
            "\n".join(
                lines
            ).encode()
        )
        .decode()
    )

    return Response(
        content=content,
        media_type="text/plain",
    )


# ============================================================
# INFO PAGE
# ============================================================

@app.get(
    "/info/{uid}",
    response_class=HTMLResponse,
)
async def info_page(uid: str, request: Request):
    """Premium client portal. Keeps the stable /info/{uid} route but replaces the legacy card layout."""
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link:
            return HTMLResponse("<html lang=\"fa\" dir=\"rtl\"><body style=\"margin:0;background:#070a10;color:#fff;font-family:sans-serif;padding:40px\"><h2>سرویس پیدا نشد</h2></body></html>", status_code=404)
        snapshot = dict(link)

    host = get_host(request)
    vless_url = vless_link_for_link(snapshot, uid, host)
    sub_url = f"{get_scheme()}://{host}/sub/{uid}"
    label = str(snapshot.get("label") or "FaultPass")
    protocol = protocol_display_label(snapshot)
    used = int(snapshot.get("used_bytes", 0) or 0)
    limit = int(snapshot.get("limit_bytes", 0) or 0)
    pct = max(0, min(100, round((used / limit) * 100, 1))) if limit else 0
    remaining = fmt_bytes(max(0, limit-used)) if limit else "نامحدود"
    expires_at = snapshot.get("expires_at")
    expiry_display = str(expires_at) if expires_at else "نامحدود"
    expiry_remaining = "نامحدود"
    if expires_at:
        try:
            expiry_dt = datetime.fromisoformat(str(expires_at))
            now_dt = datetime.now(expiry_dt.tzinfo) if expiry_dt.tzinfo else datetime.now()
            seconds = int((expiry_dt - now_dt).total_seconds())
            if seconds <= 0:
                expiry_remaining = "منقضی شده"
            else:
                days, rem = divmod(seconds, 86400)
                hours, rem = divmod(rem, 3600)
                minutes, _ = divmod(rem, 60)
                expiry_remaining = f"{days} روز" if days else (f"{hours} ساعت" if hours else f"{minutes} دقیقه")
        except Exception:
            expiry_remaining = "نامشخص"
    active = is_link_allowed(snapshot)
    ip_limit = "نامحدود" if not snapshot.get("ip_limit", 0) else str(snapshot.get("ip_limit"))
    conn_limit = "نامحدود" if not snapshot.get("connection_limit", 0) else str(snapshot.get("connection_limit"))
    speed_limit = "نامحدود" if not snapshot.get("speed_limit_bytes", 0) else fmt_bytes(snapshot.get("speed_limit_bytes", 0)) + "/s"
    ips = len(unique_ips_for_uuid(uid))

    esc = lambda x: escape_html(str(x))
    label_e = esc(label); protocol_e = esc(protocol); uid_e = esc(uid)
    sub_e = esc(sub_url); vless_e = esc(vless_url); expiry_e = esc(expiry_display)
    rem_e = esc(remaining); speed_e = esc(speed_limit); ip_e = esc(ip_limit); conn_e = esc(conn_limit)
    used_e = esc(fmt_bytes(used)); limit_e = esc(fmt_bytes(limit) if limit else "نامحدود")
    status_e = "فعال" if active else "غیرفعال"
    raw_js = json.dumps(raw_url if 'raw_url' in locals() else sub_url)
    vless_js = json.dumps(vless_url)
    sub_js = json.dumps(sub_url)

    html = """<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#070a12"><meta name="color-scheme" content="dark"><title>__LABEL__ · FaultPass</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js"></script>
<style>
:root{--bg:#060812;--panel:#0d1220;--panel2:#111827;--line:rgba(255,255,255,.08);--muted:#8b97ad;--text:#f5f7fb;--accent:#3b82f6;--cyan:#3dd8ff;--good:#2dd4a0;--warn:#f5b942;--danger:#ff6175}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;font-family:Vazirmatn,Inter,sans-serif;background:var(--bg);color:var(--text)}body{overflow-x:hidden;background:radial-gradient(900px 420px at 85% -10%,rgba(59,130,246,.18),transparent 60%),radial-gradient(700px 380px at 5% 25%,rgba(61,216,255,.08),transparent 62%),linear-gradient(180deg,#070a12,#05070d)}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.28;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:48px 48px;mask-image:linear-gradient(#000,transparent 90%)}
.wrap{width:min(1180px,calc(100% - 28px));margin:auto;padding:22px 0 70px;position:relative;z-index:1}.top{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}.brand{display:flex;align-items:center;gap:11px}.mark{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(145deg,#1b1730,#111c2c);border:1px solid rgba(59,130,246,.35);box-shadow:0 10px 35px rgba(0,0,0,.3);font-size:18px}.brand b{display:block;font-size:15px}.brand small{display:block;color:#66738a;font-size:9px;letter-spacing:.14em;margin-top:3px}.top-actions{display:flex;gap:8px;flex-wrap:wrap}.btn{border:1px solid var(--line);background:rgba(255,255,255,.035);color:#dce3ef;border-radius:11px;padding:10px 13px;font:800 11px inherit;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:7px}.btn.primary{border-color:rgba(59,130,246,.45);background:linear-gradient(135deg,#3b82f6,#5d72ff);color:#fff;box-shadow:0 12px 32px rgba(92,91,255,.2)}.btn.good{color:#7bf0c6;border-color:rgba(45,212,160,.25);background:rgba(45,212,160,.07)}
.hero{display:grid;grid-template-columns:1fr 250px;gap:18px;padding:28px;border:1px solid var(--line);border-radius:26px;background:linear-gradient(135deg,rgba(17,24,39,.92),rgba(8,12,21,.88));box-shadow:0 30px 100px rgba(0,0,0,.25);overflow:hidden;position:relative}.hero:after{content:"";position:absolute;width:360px;height:360px;left:-140px;top:-220px;border-radius:50%;background:radial-gradient(circle,rgba(59,130,246,.22),transparent 68%)}.hero-main{position:relative;z-index:1}.eyebrow{font-size:9px;letter-spacing:.18em;color:#8290a8;font-weight:900;text-transform:uppercase}.hero h1{font-size:clamp(28px,5vw,50px);line-height:1.08;letter-spacing:-.045em;margin:10px 0 8px}.hero p{margin:0;color:var(--muted);font-size:12px;line-height:2;max-width:700px}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:15px}.chip{border:1px solid var(--line);background:rgba(255,255,255,.035);padding:7px 9px;border-radius:10px;color:#b9c4d5;font-size:9.5px}.chip b{color:#fff}.hero-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:17px}.qr-card{position:relative;z-index:1;border:1px solid var(--line);border-radius:20px;background:rgba(0,0,0,.18);padding:14px;text-align:center}.qr-card img{width:174px;height:174px;background:#fff;border-radius:14px;padding:8px}.qr-card small{display:block;color:#69768c;font-size:9px;margin-top:8px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:12px 0}.kpi{border:1px solid var(--line);border-radius:17px;background:rgba(13,18,32,.82);padding:16px}.kpi .cap{font-size:9px;color:#6e7b90}.kpi .num{font-size:19px;font-weight:900;margin-top:6px}.kpi.good .num{color:#5ee7ba}.kpi.warn .num{color:#ffd067}.kpi.blue .num{color:#72cfff}.kpi.purple .num{color:#b8a7ff}
.grid{display:grid;grid-template-columns:1.35fr .65fr;gap:12px}.panel{border:1px solid var(--line);border-radius:20px;background:rgba(13,18,32,.84);overflow:hidden}.head{padding:16px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:10px}.head b{font-size:12px}.head small{display:block;color:#6e7b90;font-size:9px;margin-top:3px}.body{padding:18px}.usage-top{display:flex;align-items:center;gap:18px}.ring{width:130px;height:130px;border-radius:50%;background:conic-gradient(var(--accent) __PCT__%,#1b2332 0);position:relative;display:grid;place-items:center;flex-shrink:0}.ring:before{content:"";position:absolute;inset:9px;border-radius:50%;background:#0d1220}.ring>div{position:relative;text-align:center}.ring strong{font-size:22px}.ring small{display:block;color:#6d7890;font-size:8px;margin-top:2px}.usage-val{font-size:26px;font-weight:950;letter-spacing:-.04em}.usage-val span{font-size:11px;color:#69768c;font-weight:600}.bar{height:10px;border-radius:99px;background:#1a2230;overflow:hidden;margin:13px 0 9px}.bar i{display:block;height:100%;width:__PCT__%;background:linear-gradient(90deg,var(--accent),var(--cyan));border-radius:inherit}.remaining{display:flex;justify-content:space-between;gap:10px;color:#768297;font-size:9.5px;flex-wrap:wrap}.trend{margin-top:15px;border:1px solid var(--line);background:rgba(0,0,0,.12);border-radius:14px;padding:10px}.trend svg{width:100%;height:80px}.facts{display:grid;grid-template-columns:1fr 1fr;gap:9px}.fact{padding:13px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018)}.fact small{display:block;color:#6d7890;font-size:8.5px}.fact b{display:block;margin-top:6px;font-size:11px;word-break:break-word}.linkbox{margin-top:12px;padding:13px;border:1px solid var(--line);border-radius:14px;background:#080c15;direction:ltr;text-align:left;color:#b8c7ff;font:10px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace;word-break:break-all}.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.wide{grid-column:1/-1}.tech{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}.tech .fact{min-height:76px}.apps{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.app{padding:13px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018);text-decoration:none}.app b{font-size:11px}.app small{display:block;color:#6d7890;font-size:8.5px;margin-top:4px}.footer{text-align:center;color:#566174;font-size:9px;padding:22px 0}.toast{position:fixed;bottom:22px;left:50%;transform:translate(-50%,18px);opacity:0;pointer-events:none;background:#111827;border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:10px;transition:.2s;z-index:20}.toast.show{opacity:1;transform:translate(-50%,0)}
@media(max-width:900px){.hero{grid-template-columns:1fr}.qr-card{max-width:240px}.grid{grid-template-columns:1fr}.kpis{grid-template-columns:repeat(2,1fr)}.tech{grid-template-columns:repeat(2,1fr)}}@media(max-width:540px){.wrap{width:calc(100% - 18px);padding-top:12px}.hero{padding:20px;border-radius:21px}.kpis{grid-template-columns:1fr 1fr}.usage-top{align-items:flex-start}.ring{width:100px;height:100px}.usage-val{font-size:21px}.facts{grid-template-columns:1fr}.tech,.apps{grid-template-columns:1fr}.actions{grid-template-columns:1fr}.top{align-items:flex-start}.top-actions{justify-content:flex-end}.hero h1{font-size:32px}}
</style></head><body>
<main class="wrap">
<div class="top"><div class="brand"><div class="mark">✦</div><div><b>FaultPass</b><small>SECURE CLIENT PORTAL</small></div></div><div class="top-actions"><button class="btn" onclick="toggleTheme()">◐ پوسته</button><button class="btn" onclick="openQr()">▦ QR</button><span class="btn good">● __STATUS__</span></div></div>
<section class="hero"><div class="hero-main"><div class="eyebrow">Private Access Workspace</div><h1>__LABEL__</h1><p>مرکز حرفه‌ای مدیریت دسترسی شما؛ وضعیت مصرف، اعتبار سرویس، لینک اشتراک و مشخصات اتصال در یک فضای سریع و تمیز.</p><div class="chips"><span class="chip">پروتکل <b>__PROTOCOL__</b></span><span class="chip">شناسه <b>__UID_SHORT__</b></span><span class="chip">انقضا <b>__EXPIRY__</b></span></div><div class="hero-actions"><button class="btn primary" onclick="copy(SUB)">کپی Subscription</button><button class="btn" onclick="copy(VLESS)">کپی کانفیگ</button><a class="btn" href="__SUB_URL__">دریافت Subscription</a></div></div><div class="qr-card"><img id="qrImg" alt="QR"><small>اسکن برای اتصال سریع</small></div></section>
<section class="kpis"><div class="kpi good"><div class="cap">مصرف‌شده</div><div class="num">__USED__</div></div><div class="kpi warn"><div class="cap">باقی‌مانده</div><div class="num">__REMAINING__</div></div><div class="kpi blue"><div class="cap">IP فعال</div><div class="num">__IPS__</div></div><div class="kpi purple"><div class="cap">زمان باقی‌مانده</div><div class="num">__EXPIRY_REMAINING__</div></div></section>
<section class="grid"><div class="panel"><div class="head"><div><b>مصرف و سلامت سرویس</b><small>Real-time service overview</small></div><span style="color:#68e6b7;font-size:9px">● LIVE</span></div><div class="body"><div class="usage-top"><div class="ring"><div><strong>__PCT__%</strong><small>مصرف</small></div></div><div style="flex:1;min-width:0"><div class="usage-val">__USED__ <span>/ __LIMIT__</span></div><div class="bar"><i></i></div><div class="remaining"><span>باقی‌مانده: <b style="color:#dce3ef">__REMAINING__</b></span><span>انقضا: <b style="color:#dce3ef">__EXPIRY__</b></span></div></div></div><div class="trend"><small style="color:#6d7890;font-size:8.5px">روند مصرف</small><svg viewBox="0 0 700 90" preserveAspectRatio="none"><polyline points="0,78 80,68 150,72 230,48 310,55 390,34 470,43 550,24 700,18" fill="none" stroke="#6f83ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><polyline points="0,78 80,68 150,72 230,48 310,55 390,34 470,43 550,24 700,18 700,90 0,90" fill="url(#g)" opacity=".22"/><defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#6f83ff"/><stop offset="1" stop-color="#6f83ff" stop-opacity="0"/></linearGradient></defs></svg></div></div></div>
<aside class="panel"><div class="head"><div><b>مشخصات دسترسی</b><small>Limits & connection</small></div></div><div class="body"><div class="facts"><div class="fact"><small>IP Limit</small><b>__IP__</b></div><div class="fact"><small>Connection</small><b>__CONN__</b></div><div class="fact"><small>Speed</small><b>__SPEED__</b></div><div class="fact"><small>Expiry</small><b>__EXPIRY__</b></div></div><div class="linkbox" id="subLink">__SUB_URL__</div><div class="actions"><button class="btn primary" onclick="copy(SUB)">کپی لینک</button><button class="btn" onclick="openQr()">نمایش QR</button></div></div></aside></section>
<section class="panel" style="margin-top:12px"><div class="head"><div><b>اطلاعات فنی</b><small>Connection profile</small></div></div><div class="body"><div class="tech"><div class="fact"><small>Protocol</small><b dir="ltr">__PROTOCOL__</b></div><div class="fact"><small>Fingerprint</small><b dir="ltr">__FINGERPRINT__</b></div><div class="fact"><small>UUID</small><b dir="ltr">__UUID__</b></div><div class="fact"><small>Public subscription</small><b>READY</b></div></div></div></section>
<section class="panel" style="margin-top:12px"><div class="head"><div><b>کلاینت‌های پیشنهادی</b><small>Import the subscription link into a compatible client</small></div></div><div class="body"><div class="apps"><a class="app" href="https://github.com/2dust/v2rayNG/releases/latest" target="_blank" rel="noopener"><b>v2rayNG</b><small>Android</small></a><a class="app" href="https://github.com/2dust/v2rayN/releases/latest" target="_blank" rel="noopener"><b>v2rayN</b><small>Windows / macOS / Linux</small></a><a class="app" href="https://github.com/hiddify/hiddify-app/releases/latest" target="_blank" rel="noopener"><b>Hiddify</b><small>Android / Desktop</small></a></div></div></section>
<div class="footer">FaultPass Secure Client Portal · اطلاعات اتصال فقط برای صاحب این لینک</div>
</main><div id="toast" class="toast"></div>
<div id="qrModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.86);backdrop-filter:blur(6px);z-index:10;align-items:center;justify-content:center;padding:20px"><div style="width:min(360px,100%);background:#0c1220;border:1px solid var(--line);border-radius:22px;padding:22px;text-align:center"><button class="btn" onclick="closeQr()" style="float:left">بستن</button><h3 style="margin:4px 0 16px">QR اتصال</h3><div style="background:#fff;padding:12px;border-radius:16px;display:inline-block"><div id="qrBox"></div></div><p id="qrText" style="font:9px/1.7 ui-monospace;color:#aebcff;word-break:break-all;direction:ltr;margin-top:14px"></p></div></div>
<script>
const SUB=__SUB_JS__, VLESS=__VLESS_JS__;
function toast(t){const e=document.getElementById('toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),1600)}
async function copy(v){try{await navigator.clipboard.writeText(v);toast('کپی شد ✓')}catch(e){const x=document.createElement('textarea');x.value=v;document.body.appendChild(x);x.select();document.execCommand('copy');x.remove();toast('کپی شد ✓')}}
function toggleTheme(){document.body.classList.toggle('light');localStorage.setItem('vw_portal_theme',document.body.classList.contains('light')?'light':'dark')}
(function(){if(localStorage.getItem('vw_portal_theme')==='light'){document.body.classList.add('light');document.documentElement.style.setProperty('--bg','#eef1f7');document.documentElement.style.setProperty('--panel','#fff');document.documentElement.style.setProperty('--panel2','#f5f7fb');document.documentElement.style.setProperty('--text','#151827');document.documentElement.style.setProperty('--muted','#667085')}})();
function qrFor(v){try{const q=qrcode(0,'M');q.addData(v);q.make();document.getElementById('qrImg').src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(q.createSvgTag(4,4));document.getElementById('qrBox').innerHTML=q.createSvgTag(5,4);document.getElementById('qrText').textContent=v}catch(e){}}
function openQr(){document.getElementById('qrModal').style.display='flex'}function closeQr(){document.getElementById('qrModal').style.display='none'}qrFor(VLESS);
</script></body></html>"""
    repl = {
        "__LABEL__": label_e, "__PROTOCOL__": protocol_e, "__UID_SHORT__": esc(uid[:18]+'…'),
        "__EXPIRY__": expiry_e, "__STATUS__": status_e, "__USED__": used_e, "__REMAINING__": rem_e,
        "__IPS__": str(ips), "__EXPIRY_REMAINING__": esc(expiry_remaining), "__LIMIT__": limit_e,
        "__IP__": ip_e, "__CONN__": conn_e, "__SPEED__": speed_e, "__FINGERPRINT__": esc(snapshot.get("fingerprint", "chrome")),
        "__UUID__": uid_e, "__SUB_URL__": sub_e, "__VLESS_URL__": vless_e, "__PCT__": str(pct),
        "__SUB_JS__": sub_js, "__VLESS_JS__": vless_js,
    }
    for k,v in repl.items(): html = html.replace(k,v)
    return HTMLResponse(_uui(html, "public"))

# ============================================================
# SUB GROUP API
# ============================================================

@app.post("/api/subs")
async def create_sub_api(
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    sub_id, sub = await create_sub_group(
        name=body.get(
            "name",
            "گروه جدید",
        ),
        desc=body.get(
            "desc",
            "",
        ),
        password=body.get(
            "password",
            "",
        ),
    )

    host = get_host(request)

    return {
        "sub_id":
            sub_id,

        **sub,

        "password_hash":
            None,

        "public_url":
            (
                f"{get_scheme()}://{host}"
                f"/p/{sub['uuid_key']}"
            ),

        "sub_url":
            (
                f"{get_scheme()}://{host}"
                f"/sub-group/{sub['uuid_key']}"
            ),
    }


@app.get("/api/subs")
async def list_subs_api(
    request: Request,
    _=Depends(require_auth),
):

    host = get_host(request)

    async with SUBS_LOCK:
        snapshot_subs = dict(SUBS)

    async with LINKS_LOCK:
        snapshot_links = dict(LINKS)

    result = []

    for sid, sub in snapshot_subs.items():

        link_ids = sub.get(
            "link_ids",
            [],
        )

        active_count = sum(
            1
            for lid in link_ids
            if is_link_allowed(
                snapshot_links.get(
                    lid
                )
            )
        )

        total_used = sum(
            snapshot_links[
                lid
            ].get(
                "used_bytes",
                0,
            )

            for lid in link_ids

            if lid in snapshot_links
        )

        result.append(
            {
                "sub_id":
                    sid,

                **sub,

                "password_hash":
                    None,

                "has_password":
                    sub.get(
                        "password_hash"
                    ) is not None,

                "links_count":
                    len(link_ids) + len(sub.get("remote_links", [])),

                "local_count":
                    len(link_ids),

                "remote_count":
                    len(sub.get("remote_links", [])),

                "active_count":
                    active_count,

                "total_used_bytes":
                    total_used,

                "total_used_fmt":
                    fmt_bytes(
                        total_used
                    ),

                "public_url":
                    (
                        f"{get_scheme()}://{host}"
                        f"/p/{sub['uuid_key']}"
                    ),

                "sub_url":
                    (
                        f"{get_scheme()}://{host}"
                        f"/sub-group/{sub['uuid_key']}"
                    ),

                # جایگزین نسخه‌ی خامِ **sub (که رشته‌ی vless کامل را دارد)
                "remote_links":
                    public_remote_links(sub.get("remote_links", [])),
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "created_at",
                "",
            ),
        reverse=True,
    )

    return {
        "subs": result
    }


@app.patch("/api/subs/{sub_id}")
async def update_sub_api(
    sub_id: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    async with SUBS_LOCK:

        if sub_id not in SUBS:
            raise HTTPException(
                status_code=404,
                detail="sub not found",
            )

        sub = SUBS[sub_id]

        if "name" in body:
            sub["name"] = str(
                body["name"]
            )[:60]

        if "desc" in body:
            sub["desc"] = str(
                body["desc"]
            )[:200]

        if "password" in body:

            password = str(
                body.get(
                    "password",
                    "",
                )
            ).strip()

            sub["password_hash"] = (
                hash_password(password)
                if password
                else None
            )

        if "link_ids" in body:

            sub["link_ids"] = list(
                body["link_ids"]
            )

    await save_state()

    return {
        "ok": True
    }


@app.delete("/api/subs/{sub_id}")
async def delete_sub_api(
    sub_id: str,
    _=Depends(require_auth),
):

    name = await remove_sub_group(
        sub_id
    )

    if name is None:
        raise HTTPException(
            status_code=404,
            detail="sub not found",
        )

    return {
        "ok": True,
        "deleted": sub_id,
    }


@app.post("/api/subs/{sub_id}/links")
async def assign_link_to_sub(
    sub_id: str,
    request: Request,
    _=Depends(require_auth),
):

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="JSON نامعتبر است",
        )

    link_id = str(
        body.get(
            "link_id",
            "",
        )
    )

    action = str(
        body.get(
            "action",
            "add",
        )
    )

    if action == "add":

        success = await set_link_sub(
            link_id,
            sub_id,
        )

    else:

        success = await set_link_sub(
            link_id,
            None,
        )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="link or sub not found",
        )

    return {
        "ok": True
    }


# ============================================================
# NODE LINKS IN A SUBSCRIPTION  ·  دقیقاً مثل «Nodes» در پنل سنایی:
# یک اینباند در این پنل + یک اینباند روی یک نودِ دیگر، هر دو در یک اشتراک
# ============================================================

MAX_REMOTE_LINKS_PER_SUB = 200


@app.get("/api/nodes/{node_id}/inbounds")
async def api_node_inbounds(node_id: str, _=Depends(require_owner)):
    """لیست اینباندهای واقعی (نه کلاینت‌ها) روی یک نود، برای انتخاب و اتصال به یک ساب‌گروه اینجا."""
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        raise HTTPException(status_code=503, detail="ماژول نودها در دسترس نیست")
    node = get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")
    try:
        data = await call_node_json(node_id, "GET", "/api/links")
    except NodeCallError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
    items = [l for l in (data.get("links") or []) if not l.get("is_client")]
    items.sort(key=lambda l: l.get("created_at") or "", reverse=True)
    return {
        "ok": True,
        "node": {"id": node_id, "name": node.get("name", "")},
        "inbounds": [
            {
                "uuid": l.get("uuid"),
                "label": l.get("label", ""),
                "protocol_display": l.get("protocol_display", ""),
                "network": l.get("network", ""),
                "port": l.get("port"),
                "active": bool(l.get("active", True)),
                "outbound": l.get("outbound"),
                "client_count": l.get("client_count", 0),
            }
            for l in items
        ],
    }


@app.post("/api/subs/{sub_id}/remote-links")
async def add_remote_links_to_sub(sub_id: str, request: Request, _=Depends(require_owner)):
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        raise HTTPException(status_code=503, detail="ماژول نودها در دسترس نیست")
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر است")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات معتبر نیست")
    node_id = str(body.get("node_id") or "").strip()
    uuids = body.get("uuids")
    if uuids is None:
        uuids = [body.get("uuid")]
    if not isinstance(uuids, list) or not uuids:
        raise HTTPException(status_code=400, detail="حداقل یک اینباند از نود انتخاب کن")
    node = get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="نود پیدا نشد")

    async with SUBS_LOCK:
        entries = sub.setdefault("remote_links", [])
        existing_keys = {(e["node_id"], e["uuid"]) for e in entries}

    added, failed = [], []
    for raw_uid in dict.fromkeys(str(u) for u in uuids):
        if (node_id, raw_uid) in existing_keys:
            continue
        if len(existing_keys) + len(added) >= MAX_REMOTE_LINKS_PER_SUB:
            failed.append({"uuid": raw_uid, "error": f"حداکثر {MAX_REMOTE_LINKS_PER_SUB} عضو ریموت در هر ساب"})
            continue
        try:
            data = await call_node_json(node_id, "GET", f"/api/links/{raw_uid}/info", timeout=10.0)
        except NodeCallError as exc:
            failed.append({"uuid": raw_uid, "error": str(exc)})
            continue
        entry = {
            "node_id": node_id,
            "uuid": raw_uid,
            "label": str(data.get("label") or ""),
            "protocol_display": str(data.get("protocol_display") or ""),
            "vless": str(data.get("vless_full") or data.get("vless") or ""),
            "vless_variants": [str(x) for x in (data.get("vless_variants") or []) if x],
            "active": bool(data.get("active", True)),
            "used_bytes": int(data.get("used_bytes") or 0),
            "limit_bytes": int(data.get("limit_bytes") or 0),
            "expires_at": data.get("expires_at"),
            "added_at": datetime.now().isoformat(),
            "last_synced_at": datetime.now().isoformat(),
            "last_error": "",
        }
        added.append(entry)

    if added:
        async with SUBS_LOCK:
            sub.setdefault("remote_links", []).extend(added)
        await save_state()
        log_activity("sub", f"{len(added)} اینباند از نود «{node['name']}» به گروه «{sub.get('name','')}» اضافه شد", "ok")

    return {"ok": True, "added": len(added), "failed": failed, "remote_links": public_remote_links(sub.get("remote_links", []))}


@app.delete("/api/subs/{sub_id}/remote-links/{ref_id}")
async def remove_remote_link_from_sub(sub_id: str, ref_id: str, _=Depends(require_owner)):
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
        node_id, _, uid = ref_id.partition(":")
        before = len(sub.get("remote_links", []))
        sub["remote_links"] = [e for e in sub.get("remote_links", []) if not (e["node_id"] == node_id and e["uuid"] == uid)]
        removed = before - len(sub["remote_links"])
    if removed:
        await save_state()
        log_activity("sub", f"یک عضو ریموت از گروه «{sub.get('name','')}» حذف شد", "warn")
    return {"ok": True, "removed": bool(removed)}


@app.post("/api/subs/{sub_id}/remote-links/refresh")
async def refresh_remote_links_api(sub_id: str, _=Depends(require_owner)):
    async with SUBS_LOCK:
        sub = SUBS.get(sub_id)
        if not sub:
            raise HTTPException(status_code=404, detail="گروه ساب پیدا نشد")
    await refresh_remote_links_if_stale(sub, sub_id=sub_id, force=True)
    return {"ok": True, "remote_links": public_remote_links(sub.get("remote_links", []))}


REMOTE_LINK_TTL = 300.0  # ثانیه؛ کش لینک‌های نود تا این مدت بدون تماس با نود سرو می‌شود


async def refresh_remote_link_entry(entry: dict) -> dict:
    """کش یک عضو ریموت (لینک روی یک نود) را با یک تماس به همان نود تازه می‌کند.
    اگر نود جواب ندهد، آخرین نسخه‌ی کش‌شده دست‌نخورده می‌ماند (فقط last_error ست می‌شود)."""
    try:
        from nodes import call_node_json, NodeCallError, get_node
    except Exception:
        entry["last_error"] = "ماژول نودها در دسترس نیست"
        return entry
    if not get_node(entry["node_id"]):
        # نود از رجیستری پنل اصلی حذف شده؛ دیگه سعی نمی‌کنیم بهش وصل بشیم و
        # این عضو رو توی خروجی اشتراک نمی‌ذاریم (تا کانفیگِ یتیم بی‌صدا سرو نشه)
        entry["node_missing"] = True
        entry["last_error"] = "این نود از پنل اصلی حذف شده است"
        return entry
    entry.pop("node_missing", None)
    try:
        data = await call_node_json(entry["node_id"], "GET", f"/api/links/{entry['uuid']}/info", timeout=6.0)
        entry.update(
            label=str(data.get("label") or entry.get("label") or ""),
            protocol_display=str(data.get("protocol_display") or entry.get("protocol_display") or ""),
            vless=str(data.get("vless_full") or data.get("vless") or ""),
            vless_variants=[str(x) for x in (data.get("vless_variants") or []) if x],
            active=bool(data.get("active", True)),
            used_bytes=int(data.get("used_bytes") or 0),
            limit_bytes=int(data.get("limit_bytes") or 0),
            expires_at=data.get("expires_at"),
            last_synced_at=datetime.now().isoformat(),
            last_error="",
        )
    except NodeCallError as exc:
        entry["last_error"] = str(exc)[:200]
    except Exception as exc:
        entry["last_error"] = f"{type(exc).__name__}: {str(exc)[:150]}"
    return entry


async def mark_node_removed_in_subs(node_id: str):
    """وقتی یک نود از رجیستری پنل اصلی حذف می‌شه، بلافاصله (نه فقط بعد از TTL کش)
    عضوهای ریموتی که به همون نود اشاره می‌کنن رو «یتیم» علامت می‌زنیم تا از سرو شدن
    یک کانفیگ بدون نظارت جلوگیری بشه. صدا زده می‌شه از nodes.py، هنگام حذف نود."""
    changed = False
    async with SUBS_LOCK:
        for sub in SUBS.values():
            for entry in sub.get("remote_links", []):
                if entry.get("node_id") == node_id and not entry.get("node_missing"):
                    entry["node_missing"] = True
                    entry["last_error"] = "این نود از پنل اصلی حذف شده است"
                    changed = True
    if changed:
        await save_state()


async def refresh_remote_links_if_stale(sub: dict, sub_id: str | None = None, force: bool = False) -> list[dict]:
    entries = sub.get("remote_links", [])
    if not entries:
        return []
    now = time.time()

    def _is_stale(e):
        ts = e.get("last_synced_at")
        if not ts:
            return True
        try:
            return (now - datetime.fromisoformat(ts).timestamp()) > REMOTE_LINK_TTL
        except Exception:
            return True

    stale = entries if force else [e for e in entries if _is_stale(e)]
    if stale:
        await asyncio.gather(*(refresh_remote_link_entry(e) for e in stale), return_exceptions=True)
        if sub_id:
            await save_state()
    return entries


# ============================================================
# GROUP SUB
# ============================================================

@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(
    uuid_key: str,
    request: Request,
):

    async with SUBS_LOCK:

        sub = next(
            (
                item
                for item
                in SUBS.values()
                if item.get(
                    "uuid_key"
                ) == uuid_key
            ),
            None,
        )

    if not sub:
        raise HTTPException(
            status_code=404,
            detail="not found",
        )

    if sub.get(
        "password_hash"
    ):

        password = (
            request.query_params.get(
                "pw",
                "",
            )
        )

        if (
            hash_password(password)
            != sub["password_hash"]
        ):

            raise HTTPException(
                status_code=403,
                detail="wrong password",
            )

    host = get_host(request)

    async with LINKS_LOCK:

        lines = []

        for link_id in sub.get(
            "link_ids",
            [],
        ):

            link = LINKS.get(
                link_id
            )

            if (
                link
                and is_link_allowed(
                    link
                )
            ):

                for vlink, vuid, vtag in expand_outbound_variants(link, link_id):
                    lines.append(
                        vless_link_for_link(
                            {**vlink, "label": f"{vtag} | {vlink.get('label') or 'Config'}"} if vtag else vlink,
                            vuid,
                            host,
                        )
                    )

    # اعضای «ریموت» = لینک‌هایی که روی یک نود دیگر (پنل FaultPass دیگر، با لوکیشن دیگر)
    # ساخته شده‌اند و به این ساب‌گروه وصل شده‌اند؛ هر دو داخل یک اشتراک سرو می‌شوند.
    remote_entries = await refresh_remote_links_if_stale(
        sub,
        sub_id=next((k for k, v in SUBS.items() if v is sub), None),
    )
    remote_used = 0
    remote_limit = 0
    remote_expiries = []
    for entry in remote_entries:
        if not entry.get("active", True):
            continue
        remote_used += int(entry.get("used_bytes", 0) or 0)
        remote_limit += int(entry.get("limit_bytes", 0) or 0)
        if entry.get("expires_at"):
            remote_expiries.append(str(entry.get("expires_at")))
        if not entry.get("node_missing") and (entry.get("vless_variants") or entry.get("vless")):
            lines.extend(entry.get("vless_variants") or [entry["vless"]])

    content = (
        base64
        .b64encode(
            "\n".join(
                lines
            ).encode()
        )
        .decode()
    )

    total_used = remote_used
    total_limit = remote_limit
    expiries = list(remote_expiries)
    valid_ids = list(sub.get("link_ids", []))

    async with LINKS_LOCK:
        for link_id in valid_ids:
            link = LINKS.get(link_id)
            if not link or not link_visible_for_subscription(link):
                continue
            total_used += int(link.get("used_bytes", 0) or 0)
            total_limit += int(link.get("limit_bytes", 0) or 0)
            if link.get("expires_at"):
                expiries.append(str(link.get("expires_at")))

    # For a group subscription, expose aggregate usage/expiry in standard headers.
    group_limit = total_limit if total_limit > 0 else 0
    group_expiry = None
    if expiries:
        try:
            group_expiry = min(
                expiries,
                key=lambda x: datetime.fromisoformat(x)
            )
        except Exception:
            group_expiry = expiries[0]

    group_volume_text = (
        f"{fmt_bytes(total_used)}/{fmt_bytes(group_limit)}"
        if group_limit > 0
        else f"{fmt_bytes(total_used)}/∞"
    )
    group_expiry_text = group_expiry or "∞"
    group_title = (
        f"0.0.0.0 | {group_volume_text} | {group_expiry_text} | "
        f"{sub['name']} | کانال تلگرام: FaultPass"
    )
    headers = subscription_metadata_headers(
        total_used,
        group_limit,
        group_expiry,
        host,
        f"{get_scheme()}://{host}/public-sub/{uuid_key}",
        group_title,
    )

    return Response(
        content=content,
        media_type="text/plain; charset=utf-8",
        headers=headers,
    )


# ============================================================
# PUBLIC GROUP
# ============================================================

PUBLIC_SUB_HTML = r"""
<!doctype html><html lang="fa" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#080b12"><title>FaultPass · Subscription</title>
<style>
:root{--bg:#070a10;--panel:#0d121b;--panel2:#111823;--line:rgba(255,255,255,.08);--text:#f5f7fb;--muted:#8e9aae;--soft:#647086;--accent:#3b82f6;--cyan:#39d6ff;--green:#36d399;--red:#ff7088}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 10% 0%,rgba(59,130,246,.18),transparent 28%),radial-gradient(circle at 92% 8%,rgba(57,214,255,.09),transparent 25%),#070a10;color:var(--text);font-family:Inter,Tahoma,Arial,sans-serif}.wrap{width:min(1120px,calc(100% - 28px));margin:auto;padding:25px 0 70px}.top{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:16px}.brand{display:flex;align-items:center;gap:10px;font-weight:900}.mark{width:40px;height:40px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(145deg,#17132a,#111b2a);border:1px solid rgba(59,130,246,.35);box-shadow:inset 0 0 25px rgba(59,130,246,.09)}.brand small{display:block;color:var(--soft);font-size:9px;margin-top:3px}.badge{padding:8px 12px;border-radius:999px;border:1px solid rgba(54,211,153,.22);background:rgba(54,211,153,.07);color:#7ceabf;font-size:10px;font-weight:800}.hero{border:1px solid var(--line);border-radius:28px;padding:27px;background:linear-gradient(135deg,rgba(17,24,35,.94),rgba(9,13,20,.9));box-shadow:0 30px 100px rgba(0,0,0,.24);margin-bottom:14px}.eyebrow{font-size:9px;color:#8995aa;letter-spacing:.15em;text-transform:uppercase;font-weight:900}.hero h1{font-size:clamp(28px,5vw,46px);margin:8px 0}.hero p{color:var(--muted);font-size:12px;line-height:2;margin:0;max-width:760px}.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:20px}.stat{padding:14px;border:1px solid var(--line);background:rgba(255,255,255,.018);border-radius:16px}.stat label{display:block;color:var(--soft);font-size:9px;margin-bottom:7px}.stat b{font-size:18px}.layout{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(300px,.6fr);gap:14px}.panel{border:1px solid var(--line);background:rgba(13,18,27,.84);border-radius:23px;overflow:hidden;box-shadow:0 20px 65px rgba(0,0,0,.17)}.head{padding:16px 18px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center}.head b{font-size:12px}.head small{display:block;color:var(--soft);font-size:9px;margin-top:4px}.body{padding:17px}.url{padding:13px;border-radius:14px;background:#090d15;border:1px solid var(--line);direction:ltr;text-align:left;word-break:break-all;color:#b9c7ff;font:10px/1.7 ui-monospace,SFMono-Regular,Consolas,monospace}.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px}.btn{border:0;cursor:pointer;text-decoration:none;color:#fff;background:linear-gradient(135deg,#3b82f6,#4d7cff);padding:11px 13px;border-radius:12px;font-size:10px;font-weight:850;text-align:center}.btn.alt{background:#121925;border:1px solid var(--line);color:#dce2eb}.full{grid-column:1/-1}.link{padding:14px;border:1px solid var(--line);border-radius:16px;background:rgba(255,255,255,.015);margin-bottom:9px}.link:last-child{margin-bottom:0}.linktop{display:flex;justify-content:space-between;gap:12px;align-items:center}.linkname{font-weight:850;font-size:12px}.proto{color:#a998ff;font-size:9px;margin-top:4px}.online{padding:5px 8px;border-radius:999px;font-size:8px;background:rgba(54,211,153,.08);color:#79e9bc;border:1px solid rgba(54,211,153,.18)}.offline{background:rgba(255,112,136,.08);color:#ff9aae;border-color:rgba(255,112,136,.18)}.linkmeta{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px}.mini{padding:9px;border-radius:11px;background:#0b1018;border:1px solid rgba(255,255,255,.05)}.mini small{display:block;color:var(--soft);font-size:8px}.mini b{display:block;margin-top:4px;font-size:10px}.qr{text-align:center}.qr img{width:190px;height:190px;background:#fff;padding:9px;border-radius:17px}.notice{margin-top:12px;padding:12px;border-radius:13px;background:rgba(57,214,255,.045);border:1px solid rgba(57,214,255,.11);color:#9eb3c9;font-size:9px;line-height:1.9}.footer{text-align:center;color:#566174;font-size:9px;padding-top:22px}.locked{max-width:500px;margin:14vh auto}.field{display:flex;gap:8px}.field input{flex:1;background:#0a0f17;border:1px solid var(--line);color:#fff;padding:12px;border-radius:12px;direction:ltr}.toast{position:fixed;left:50%;bottom:22px;transform:translate(-50%,20px);opacity:0;background:#121925;border:1px solid var(--line);padding:10px 14px;border-radius:12px;font-size:10px;transition:.2s}.toast.show{opacity:1;transform:translate(-50%,0)}@media(max-width:800px){.layout{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr 1fr}}@media(max-width:520px){.wrap{width:calc(100% - 18px);padding-top:12px}.hero{padding:20px}.stats{grid-template-columns:1fr 1fr}.linkmeta{grid-template-columns:1fr 1fr}.actions{grid-template-columns:1fr}}
</style></head><body><main class="wrap"><div class="top"><div class="brand"><div class="mark">✦</div><div>FaultPass<small>GROUP SUBSCRIPTION</small></div></div><div class="badge">● آماده استفاده</div></div><div id="app"></div><div class="footer">FaultPass · Secure subscription delivery</div></main><div class="toast" id="toast">کپی شد</div>
<script>
const key=location.pathname.split('/').pop();const qs=location.search||'';function esc(s){return String(s??'').replace(/[&<>'"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[m]))}function toast(t){const e=document.getElementById('toast');e.textContent=t;e.classList.add('show');setTimeout(()=>e.classList.remove('show'),1600)}async function copy(v){try{await navigator.clipboard.writeText(v);toast('لینک کپی شد ✓')}catch(e){prompt('کپی کنید:',v)}}function fmt(n){if(!n)return'0 B';const u=['B','KB','MB','GB','TB'];let i=0,x=Number(n)||0;while(x>=1024&&i<u.length-1){x/=1024;i++}return(x>=100?Math.round(x):x>=10?x.toFixed(1):x.toFixed(2))+' '+u[i]}function render(d){if(d.locked){document.getElementById('app').innerHTML='<section class="panel locked"><div class="body"><div class="eyebrow">Protected subscription</div><h2>'+esc(d.name||'اشتراک')+'</h2><p style="color:var(--muted);font-size:11px;line-height:2">این اشتراک با رمز محافظت می‌شود. رمز را وارد کنید تا اطلاعات و لینک‌ها نمایش داده شوند.</p><form class="field" onsubmit="event.preventDefault();location.search='?pw='+encodeURIComponent(document.getElementById(\'pw\').value)"><input id="pw" type="password" placeholder="Subscription password"><button class="btn">ورود</button></form></div></section>';return}const links=d.links||[];const qr='https://api.qrserver.com/v1/create-qr-code/?size=220x220&data='+encodeURIComponent(d.sub_url||'');document.getElementById('app').innerHTML='<section class="hero"><div class="eyebrow">Subscription center</div><h1>'+esc(d.name||'Subscription')+'</h1><p>'+esc(d.desc||'مدیریت متمرکز کانفیگ‌ها و لینک اشتراک در یک صفحه حرفه‌ای.')+'</p><div class="stats"><div class="stat"><label>کانفیگ فعال</label><b>'+links.filter(x=>x.active).length+'</b></div><div class="stat"><label>اتصال فعال</label><b>'+Number(d.active_connections||0)+'</b></div><div class="stat"><label>مصرف کل</label><b>'+esc(d.total_used_fmt||'0 B')+'</b></div></div></section><section class="layout"><div class="panel"><div class="head"><div><b>کانفیگ‌های این اشتراک</b><small>وضعیت هر مسیر و مصرف آن</small></div><span style="color:var(--soft);font-size:9px">'+links.length+' مورد</span></div><div class="body">'+(links.length?links.map(l=>'<article class="link"><div class="linktop"><div><div class="linkname">'+esc(l.label||'Config')+'</div><div class="proto">'+esc(l.protocol||'VLESS')+'</div></div><span class="online '+(l.active?'':'offline')+'">'+(l.active?'فعال':'غیرفعال')+'</span></div><div class="linkmeta"><div class="mini"><small>مصرف</small><b>'+esc(l.used_fmt||'0 B')+' / '+esc(l.limit_fmt||'∞')+'</b></div><div class="mini"><small>اتصال</small><b>'+Number(l.connections||0)+' / '+(Number(l.connection_limit||0)||'∞')+'</b></div><div class="mini"><small>انقضا</small><b>'+esc((l.expires_at||'نامحدود').toString().slice(0,16))+'</b></div></div><div class="actions"><button class="btn" onclick="copy('+esc(JSON.stringify(l.sub_url||''))+')">کپی ساب</button><a class="btn alt" href="'+esc(l.info_url||'#')+'">جزئیات</a></div></article>').join(''):'<div style="padding:35px;text-align:center;color:var(--soft);font-size:11px">کانفیگ فعالی برای این اشتراک وجود ندارد.</div>')+'</div></div><aside class="panel"><div class="head"><div><b>لینک اصلی اشتراک</b><small>مناسب برای کلاینت‌های سازگار</small></div></div><div class="body"><div class="qr"><img src="'+qr+'" alt="QR"></div><div class="url">'+esc(d.sub_url||'')+'</div><div class="actions"><button class="btn" onclick="copy('+esc(JSON.stringify(d.sub_url||''))+')">کپی لینک</button><a class="btn alt" href="'+esc(d.sub_url||'#')+'">دریافت</a></div><div class="notice">برای استفاده، لینک بالا را در بخش Subscription کلاینت خود وارد کنید. لینک خام و API بدون تغییر باقی می‌مانند تا سازگاری حفظ شود.</div></div></aside></section>'}async function load(){try{const r=await fetch('/api/public/sub/'+encodeURIComponent(key)+qs,{cache:'no-store'});const d=await r.json();if(!r.ok)throw Error(d.detail||'خطا');render(d)}catch(e){document.getElementById('app').innerHTML='<section class="panel"><div class="body"><h2>اشتراک پیدا نشد</h2><p style="color:var(--muted)">لینک اشتراک منقضی شده، حذف شده یا در دسترس نیست.</p></div></section>'}}load();
</script></body></html>
"""
PUBLIC_SUB_HTML = _uui(PUBLIC_SUB_HTML, "public")



@app.get(
    "/p/{uuid_key}",
    response_class=HTMLResponse,
)
async def public_sub_page(
    uuid_key: str,
):

    async with SUBS_LOCK:

        exists = any(
            item.get(
                "uuid_key"
            ) == uuid_key
            for item in SUBS.values()
        )

    if not exists:

        return HTMLResponse(
            """
            <h2
            style="
            font-family:sans-serif;
            padding:40px;
            "
            >
            گروه پیدا نشد
            </h2>
            """,
            status_code=404,
        )

    return HTMLResponse(
        PUBLIC_SUB_HTML
    )


@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(
    uuid_key: str,
    request: Request,
):

    async with SUBS_LOCK:

        entry = next(
            (
                (
                    sid,
                    item,
                )

                for sid, item
                in SUBS.items()

                if item.get(
                    "uuid_key"
                ) == uuid_key
            ),
            None,
        )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="not found",
        )

    _, sub = entry

    has_password = (
        sub.get(
            "password_hash"
        ) is not None
    )

    if has_password:

        password = (
            request
            .query_params
            .get(
                "pw",
                "",
            )
        )

        if (
            hash_password(password)
            != sub[
                "password_hash"
            ]
        ):

            return JSONResponse(
                {
                    "locked": True,
                    "name":
                        sub["name"],
                }
            )

    host = get_host(request)

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    links_out = []

    active_ip_set = set()
    active_session_count = 0

    for link_id in sub.get(
        "link_ids",
        [],
    ):

        link = snapshot.get(
            link_id
        )

        if not link:
            continue

        allowed = is_link_allowed(
            link
        )

        link_ips = {
            str(item.get("ip") or "").strip()
            for item in connections.values()
            if item.get("uuid") == link_id and str(item.get("ip") or "").strip()
        }
        connection_count = len(link_ips)
        active_session_count += sum(1 for item in connections.values() if item.get("uuid") == link_id)
        active_ip_set.update(link_ips)

        links_out.append(
            {
                "uuid":
                    link_id,

                "label":
                    link.get(
                        "label"
                    ),

                "active":
                    allowed,

                "protocol":
                    link.get(
                        "protocol",
                        DEFAULT_PROTOCOL,
                    ),

                "used_bytes":
                    link.get(
                        "used_bytes",
                        0,
                    ),

                "used_fmt":
                    fmt_bytes(
                        link.get(
                            "used_bytes",
                            0,
                        )
                    ),

                "limit_bytes":
                    link.get(
                        "limit_bytes",
                        0,
                    ),

                "limit_fmt":
                    (
                        "∞"
                        if not link.get(
                            "limit_bytes",
                            0,
                        )
                        else fmt_bytes(
                            link[
                                "limit_bytes"
                            ]
                        )
                    ),

                "expires_at":
                    link.get(
                        "expires_at"
                    ),

                "vless_link":
                    vless_link_for_link(
                        link,
                        link_id,
                        host,
                    ),

                "sub_url":
                    (
                        f"{get_scheme()}://{host}"
                        f"/sub/{link_id}"
                    ),

                "info_url":
                    (
                        f"{get_scheme()}://{host}"
                        f"/info/{link_id}"
                    ),

                "connections":
                    connection_count,

                "ip_limit":
                    link.get(
                        "ip_limit",
                        0,
                    ),

                "speed_limit_bytes":
                    link.get(
                        "speed_limit_bytes",
                        0,
                    ),

                "connection_limit":
                    link.get(
                        "connection_limit",
                        0,
                    ),
            }
        )

    total_used = sum(
        item["used_bytes"]
        for item in links_out
    )

    return {
        "locked": False,

        "name":
            sub["name"],

        "desc":
            sub.get(
                "desc",
                "",
            ),

        "sub_url":
            (
                f"{get_scheme()}://{host}"
                f"/sub-group/{uuid_key}"
            ),

        "active_connections":
            len(active_ip_set),

        "active_sessions":
            active_session_count,

        "active_ips":
            sorted(active_ip_set),

        "total_used_fmt":
            fmt_bytes(
                total_used
            ),

        "support":
            SUPPORT_USERNAME,

        "links":
            links_out,
    }




@app.post("/api/mix-sub")
async def mix_subscription(request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    ids = body.get("link_ids") or []
    if not isinstance(ids, list) or len(ids) < 2:
        raise HTTPException(status_code=400, detail="حداقل ۲ کانفیگ انتخاب کنید")
    if len(ids) > 40:
        raise HTTPException(status_code=400, detail="حداکثر ۴۰ کانفیگ")
    host = get_host(request)
    lines = []
    used_names = set()
    total_used = 0
    total_limit = 0
    labels = []
    async with LINKS_LOCK:
        for lid in ids:
            link = LINKS.get(lid)
            if not link or not link_visible_for_subscription(link):
                continue
            labels.append(str(link.get("label") or lid[:8]))
            total_used += int(link.get("used_bytes", 0) or 0)
            total_limit += int(link.get("limit_bytes", 0) or 0)
            for vlink, vuid, vtag in expand_outbound_variants(link, lid):
                name = random_config_name(used_names)
                used_names.add(name)
                if vtag:
                    name = f"{vtag} | {name}"
                lines.append(vless_link_for_link({**vlink, "label": name}, vuid, host))
    if not lines:
        raise HTTPException(status_code=400, detail="هیچ کانفیگ معتبری انتخاب نشده")
    # stats first line
    vol = f"{fmt_bytes(total_used)}/{fmt_bytes(total_limit)}" if total_limit > 0 else f"{fmt_bytes(total_used)}/∞"
    mix_label = "Mix-" + random_config_name()[:6]
    stats = f"{mix_label} | {vol} | {len(lines)} configs"
    first = generate_vless_link(ids[0], "127.0.0.1", remark=stats, protocol="vless-ws")
    content = base64.b64encode(("\n".join([first] + lines)).encode()).decode()
    # store as a sub group for reuse
    sub_id, sub = await create_sub_group(name=mix_label, desc="مخلوط‌سازی کانفیگ‌ها")
    async with SUBS_LOCK:
        if sub_id in SUBS:
            SUBS[sub_id]["link_ids"] = list(ids)
    await save_state()
    return {
        "ok": True,
        "sub_url": f"{get_scheme()}://{host}/sub-group/{sub['uuid_key']}",
        "name": mix_label,
        "count": len(lines),
        "content_preview": stats,
    }


@app.get("/api/categories")
async def list_categories(_=Depends(require_auth)):
    items = [{**cat, "id": cid} for cid, cat in CATEGORIES.items()]
    items.sort(key=lambda x: int(x.get("number", 0)))
    return {"categories": items}

@app.post("/api/categories")
async def create_category(request: Request, _=Depends(require_auth)):
    if len(CATEGORIES) >= 10:
        raise HTTPException(status_code=400, detail="حداکثر ۱۰ دسته‌بندی")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    name = str(body.get("name") or "دسته جدید").strip()[:40]
    used = {int(x.get("number", 0)) for x in CATEGORIES.values()}
    num = 0
    while num in used:
        num += 1
    cid = str(num)
    limit_value = safe_float(body.get("limit_value", 0))
    limit_unit = str(body.get("limit_unit") or "GB").upper()
    limit_bytes = 0 if limit_value <= 0 else parse_size_to_bytes(limit_value, limit_unit)
    speed_value = safe_float(body.get("speed_limit_value", 0))
    speed_bytes = 0 if speed_value <= 0 else parse_speed_to_bytes(speed_value, "MBIT")
    raw_clean = body.get("clean_ips") or ""
    if isinstance(raw_clean, list):
        clean_ips = [str(x).strip() for x in raw_clean if str(x).strip()]
    else:
        clean_ips = [x.strip() for x in str(raw_clean).replace(",", "\n").splitlines() if x.strip()]
    record = {
        "id": cid, "name": name, "number": num,
        "limit_bytes": limit_bytes,
        "expires_days": safe_int(body.get("expires_days", 0), minimum=0),
        "connection_limit": safe_int(body.get("connection_limit", 0), minimum=0),
        "speed_limit_bytes": speed_bytes,
        "ip_limit": safe_int(body.get("ip_limit", 0), minimum=0),
        "clean_ips": clean_ips,
        "random_name": bool(body.get("random_name", False)),
        "single_user": bool(body.get("single_user", False)),
        "created_at": datetime.now().isoformat(),
    }
    CATEGORIES[cid] = record
    await save_state()
    return {"ok": True, **record}


@app.patch("/api/categories/{cid}")
async def update_category(cid: str, request: Request, _=Depends(require_auth)):
    if cid not in CATEGORIES:
        raise HTTPException(status_code=404, detail="یافت نشد")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON نامعتبر")
    cat = CATEGORIES[cid]
    if "name" in body:
        cat["name"] = str(body.get("name") or cat["name"]).strip()[:40]
    if "limit_value" in body:
        lv = safe_float(body.get("limit_value", 0))
        unit = str(body.get("limit_unit") or "GB").upper()
        cat["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, unit)
    if "expires_days" in body:
        cat["expires_days"] = safe_int(body.get("expires_days", 0), minimum=0)
    if "connection_limit" in body:
        cat["connection_limit"] = safe_int(body.get("connection_limit", 0), minimum=0)
    if "speed_limit_value" in body:
        sv = safe_float(body.get("speed_limit_value", 0))
        cat["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, "MBIT")
    if "ip_limit" in body:
        cat["ip_limit"] = safe_int(body.get("ip_limit", 0), minimum=0)
    if "clean_ips" in body:
        raw = body.get("clean_ips") or ""
        if isinstance(raw, list):
            cat["clean_ips"] = [str(x).strip() for x in raw if str(x).strip()]
        else:
            cat["clean_ips"] = [x.strip() for x in str(raw).replace(",", "\n").splitlines() if x.strip()]
    if "random_name" in body:
        cat["random_name"] = bool(body.get("random_name"))
    if "single_user" in body:
        cat["single_user"] = bool(body.get("single_user"))
    await save_state()
    return {"ok": True, **cat}

@app.delete("/api/categories/{cid}")
async def delete_category(cid: str, _=Depends(require_auth)):
    if cid in ("0", "1"):
        raise HTTPException(status_code=400, detail="پیش‌فرض قابل حذف نیست")
    if cid not in CATEGORIES:
        raise HTTPException(status_code=404, detail="یافت نشد")
    del CATEGORIES[cid]
    for link in LINKS.values():
        if str(link.get("category_id")) == cid:
            link["category_id"] = "0"
    await save_state()
    return {"ok": True}

# ============================================================
# STATS
# ============================================================

@app.get("/stats")
async def get_stats(
    _=Depends(require_auth),
):

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    return {
        "service":
            APP_NAME,

        "version":
            APP_VERSION,

        "active_connections":
            len(connections),

        "total_traffic_mb":
            round(
                stats[
                    "total_bytes"
                ]
                / (
                    1024 ** 2
                ),
                2,
            ),

        "total_traffic_bytes":
            stats[
                "total_bytes"
            ],

        "total_requests":
            stats[
                "total_requests"
            ],

        "total_errors":
            stats[
                "total_errors"
            ],

        "uptime":
            uptime(),

        "timestamp":
            datetime.now().isoformat(),

        "hourly":
            dict(
                hourly_traffic
            ),

        "recent_errors":
            list(
                error_logs
            )[-10:],

        "links_count":
            len(snapshot),

        "active_links":
            sum(
                1
                for link
                in snapshot.values()
                if is_link_allowed(
                    link
                )
            ),

        "expired_links":
            sum(
                1
                for link
                in snapshot.values()
                if is_link_expired(
                    link
                )
            ),

        "subs_count":
            len(SUBS),
    }


@app.get("/api/errors")
async def get_errors(
    _=Depends(require_auth),
):
    rows = list(error_logs)[-100:]
    warnings = sum(1 for x in rows if x.get("level") == "warn")
    client_errors = sum(1 for x in rows if x.get("source") == "client")
    return {
        "ok": True,
        "errors": rows,
        "total_errors": len(rows),
        "warnings": warnings,
        "client_errors": client_errors,
        "healthy": not any(x.get("level", "err") == "err" for x in rows[-20:]),
    }


@app.post("/api/errors/client")
async def report_client_error(request: Request, _=Depends(require_auth)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    message = str(body.get("message") or "Unknown browser error").strip()[:1200]
    path = str(body.get("path") or request.url.path).strip()[:500]
    stack = str(body.get("stack") or "").strip()[:4000]
    details = str(body.get("details") or "").strip()[:1500]
    error_logs.append({
        "error": message,
        "path": path,
        "method": "CLIENT",
        "source": "client",
        "level": "err",
        "stack": stack,
        "details": details,
        "time": datetime.now().isoformat(),
    })
    stats["total_errors"] += 1
    logger.error("Client error: %s | %s", path, message)
    return {"ok": True}


@app.post("/api/errors/clear")
async def clear_errors(_=Depends(require_owner)):
    count = len(error_logs)
    error_logs.clear()
    stats["total_errors"] = 0
    log_activity("system", f"مرکز پیام پاک شد؛ {count} خطا حذف شد", "warn" if count else "info")
    return {"ok": True, "cleared": count}


@app.get("/api/activity")
async def get_activity(
    _=Depends(require_auth),
):

    return {
        "logs":
            list(
                activity_logs
            )[-150:]
    }


# ============================================================
# CONNECTIONS
# ============================================================

@app.get("/api/connections")
async def get_connections(
    _=Depends(require_auth),
):

    async with LINKS_LOCK:
        snapshot = dict(LINKS)

    grouped = {}

    for connection in connections.values():

        ip = connection.get(
            "ip",
            "نامشخص",
        )

        link = snapshot.get(
            connection.get(
                "uuid"
            )
        )

        label = (
            link.get(
                "label"
            )
            if link
            else "نامشخص"
        )

        group = grouped.get(ip)

        if group is None:

            group = {
                "ip":
                    ip,

                "sessions":
                    0,

                "bytes":
                    0,

                "labels":
                    set(),

                "transports":
                    set(),

                "first_connected_at":
                    connection.get(
                        "connected_at"
                    ),

                "last_connected_at":
                    connection.get(
                        "connected_at"
                    ),
            }

            grouped[ip] = group

        group["sessions"] += 1

        group["bytes"] += int(
            connection.get(
                "bytes",
                0,
            )
            or 0
        )

        group["labels"].add(
            label
        )

        group["transports"].add(
            connection.get(
                "transport",
                DEFAULT_PROTOCOL,
            )
        )

    result = []

    for group in grouped.values():

        result.append(
            {
                "ip":
                    group["ip"],

                "sessions":
                    group["sessions"],

                "labels":
                    sorted(
                        group["labels"]
                    ),

                "label":
                    (
                        " · ".join(
                            sorted(
                                group["labels"]
                            )
                        )
                        if group["labels"]
                        else "نامشخص"
                    ),

                "transports":
                    sorted(
                        group["transports"]
                    ),

                "bytes":
                    group["bytes"],

                "bytes_fmt":
                    fmt_bytes(
                        group["bytes"]
                    ),

                "connected_at":
                    group[
                        "first_connected_at"
                    ],

                "last_connected_at":
                    group[
                        "last_connected_at"
                    ],
            }
        )

    result.sort(
        key=lambda item:
            item.get(
                "last_connected_at"
            )
            or "",
        reverse=True,
    )

    return {
        "connections":
            result,

        "count":
            len(result),

        "raw_count":
            len(connections),
    }


# ============================================================
# OPTIONAL EXISTING PROJECT MODULES
# ============================================================

# ============================================================
# IMPORTANT:
# DO NOT REPLACE THIS VLESS CORE.
# ============================================================

try:

    from relay_vless import (
        RELAY_BUF,
        parse_vless_header,
        check_and_use,
        relay_ws_to_tcp,
        relay_tcp_to_ws,
        websocket_tunnel,
    )

    app.add_api_websocket_route(
        "/ws/{uuid}",
        websocket_tunnel,
    )

    logger.info(
        "VLESS relay loaded."
    )

except Exception as exc:

    logger.warning(
        "VLESS relay module unavailable: %s",
        exc,
    )


# ============================================================
# XHTTP
# ============================================================

try:

    from xhttp_siz10 import (
        router as xhttp_router
    )

    app.include_router(
        xhttp_router
    )

    logger.info(
        "XHTTP module loaded."
    )

except Exception as exc:

    logger.warning(
        "XHTTP module unavailable: %s",
        exc,
    )


# ============================================================
# OUTBOUND PROXY (SOCKS5 / SOCKS4 / HTTP)  +  NODES (multi-location)
# ============================================================
try:

    from outbound_proxy import (
        router as outbound_proxy_router
    )

    app.include_router(
        outbound_proxy_router
    )

    logger.info(
        "Outbound proxy module loaded."
    )

except Exception as exc:

    logger.warning(
        "Outbound proxy module unavailable: %s",
        exc,
    )

# نودها: توکن API این پنل + اتصال به پنل‌های دیگر (nodes.py)
try:

    from nodes import router as nodes_router

    app.include_router(nodes_router)

    logger.info("Nodes module loaded.")

except Exception as exc:

    logger.warning(
        "Nodes module unavailable: %s",
        exc,
    )


# ============================================================
# TELEGRAM
# ============================================================

try:

    from telegram_bot import (
        start_bot as _tg_start_bot,
        stop_bot as _tg_stop_bot,
    )

except Exception:

    async def _tg_start_bot():
        return None

    async def _tg_stop_bot():
        return None


@app.on_event("startup")
async def start_optional_telegram():

    try:

        await _tg_start_bot()

        logger.info(
            "Telegram module initialized."
        )

    except Exception as exc:

        logger.warning(
            "Telegram bot disabled/error: %s",
            exc,
        )


# ============================================================
# HTTP PROXY
# ============================================================

_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-encoding",
    "content-length",
}


@app.api_route(
    "/proxy/{target_url:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "HEAD",
        "OPTIONS",
    ],
)
async def http_proxy(
    target_url: str,
    request: Request,
):

    if not target_url.startswith("http"):
        target_url = (
            "https://"
            + target_url
        )

    if http_client is None:
        raise HTTPException(
            status_code=503,
            detail="HTTP client not ready",
        )

    try:

        body = await request.body()

        headers = {
            key: value
            for key, value
            in request.headers.items()
            if (
                key.lower()
                not in _HOP
            )
            and (
                key.lower()
                != "host"
            )
        }

        response = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
        )

        stats["total_bytes"] += len(
            response.content
        )

        bump_daily_stat("traffic_bytes", len(response.content))

        stats["total_requests"] += 1

        hourly_traffic[
            now_ir().strftime(
                "%H:00"
            )
        ] += len(
            response.content
        )

        output_headers = {
            key: value
            for key, value
            in response.headers.items()
            if key.lower() not in _HOP
        }

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=output_headers,
        )

    except Exception as exc:

        stats["total_errors"] += 1

        error_logs.append(
            {
                "error":
                    str(exc),

                "url":
                    target_url,

                "time":
                    datetime.now().isoformat(),
            }
        )

        logger.exception(
            "Proxy error: %s",
            target_url,
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Proxy error: "
                f"{exc}"
            ),
        )


# ============================================================
# DASHBOARD
# ============================================================

from pages import DASHBOARD_HTML


@app.get(
    "/dashboard",
    response_class=HTMLResponse,
)
async def dashboard(
    request: Request,
):

    if not await is_valid_session(
        request.cookies.get(
            SESSION_COOKIE
        )
    ):
        return RedirectResponse(
            "/login"
        )

    await ensure_default_categories()
    await ensure_default_link()

    return HTMLResponse(
        DASHBOARD_HTML
    )


# ============================================================
# TEST
# ============================================================

@app.get(
    "/test-ws",
    response_class=HTMLResponse,
)
async def test_ws():

    return HTMLResponse(
        """
        <script>
        location.href='/dashboard'
        </script>
        """
    )


# ============================================================
# ADMIN MANAGEMENT (multi-admin / sub-admins)
# ============================================================

def _admin_public(admin_id: str, admin: dict) -> dict:
    return {
        "id": admin_id,
        "username": admin.get("username", admin_id),
        "role": admin.get("role", "admin"),
        "permissions": sorted(admin.get("permissions") or {"dashboard"}),
        "active": admin.get("active", True),
        "created_at": admin.get("created_at"),
        "last_login_at": admin.get("last_login_at"),
        "last_login_ip": admin.get("last_login_ip"),
        "credit_stars": admin.get("credit_stars", 0),
        "full_name": admin.get("full_name", ""),
        "telegram_id": admin.get("telegram_id", ""),
    }


@app.get("/api/admins")
async def api_list_admins(token=Depends(require_owner)):
    owner_entry = {
        "id": "owner",
        "username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),
        "role": "owner",
        "active": True,
        "created_at": None,
        "last_login_at": None,
        "last_login_ip": None,
    }
    admins = [owner_entry] + [
        _admin_public(aid, a) for aid, a in ADMINS.items()
    ]
    return {"ok": True, "admins": admins}


@app.post("/api/admins")
async def api_create_admin(request: Request, token=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    password = str(body.get("password", "")).strip()

    if not username or username.lower() == "owner":
        raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")

    if len(password) < LOGIN_MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
        )

    if username.lower() == AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower():
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    for a in ADMINS.values():
        if a.get("username", "").lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    admin_id = secrets.token_hex(6)

    ADMINS[admin_id] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "admin",
        "permissions": list(body.get("permissions") or {"dashboard", "inbounds", "subscriptions"}),
        "active": True,
        "created_at": datetime.now().isoformat(),
        "last_login_at": None,
        "last_login_ip": None,
    }

    await save_state()

    log_activity("auth", f"ادمین جدید «{username}» ایجاد شد", "ok")

    return {"ok": True, "admin": _admin_public(admin_id, ADMINS[admin_id])}


@app.patch("/api/admins/{admin_id}")
async def api_update_admin(admin_id: str, request: Request, token=Depends(require_owner)):
    admin = ADMINS.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="ادمین یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    if "username" in body:
        new_username = str(body["username"]).strip()
        if not new_username or new_username.lower() == "owner":
            raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")
        for aid, a in ADMINS.items():
            if aid != admin_id and a.get("username", "").lower() == new_username.lower():
                raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
        admin["username"] = new_username

    password_changed = False
    if "password" in body and str(body["password"]).strip():
        new_password = str(body["password"]).strip()
        if len(new_password) < LOGIN_MIN_PASSWORD_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
            )
        admin["password_hash"] = hash_password(new_password)
        password_changed = True

    if "permissions" in body:
        raw_permissions = body.get("permissions") or []
        if not isinstance(raw_permissions, list):
            raise HTTPException(status_code=400, detail="لیست دسترسی‌ها نامعتبر است")
        admin["permissions"] = [p for p in raw_permissions if p in ALL_PERMISSIONS]

    if "active" in body:
        admin["active"] = bool(body["active"])

    # Password changes must invalidate existing sessions for that account.
    # Otherwise an old stolen/remembered session would remain usable after a
    # credential reset. Deactivation also revokes every session.
    if password_changed or not admin.get("active", True):
        async with SESSIONS_LOCK:
            for tok in [t for t, info in SESSIONS.items()
                        if isinstance(info, dict) and info.get("admin_id") == admin_id]:
                SESSIONS.pop(tok, None)

    await save_state()

    log_activity("auth", f"اطلاعات ادمین «{admin.get('username')}» ویرایش شد", "ok")

    return {"ok": True, "admin": _admin_public(admin_id, admin)}


@app.delete("/api/admins/{admin_id}")
async def api_delete_admin(admin_id: str, token=Depends(require_owner)):
    admin = ADMINS.pop(admin_id, None)
    if not admin:
        raise HTTPException(status_code=404, detail="ادمین یافت نشد")

    async with SESSIONS_LOCK:
        for tok in [t for t, info in SESSIONS.items() if isinstance(info, dict) and info.get("admin_id") == admin_id]:
            SESSIONS.pop(tok, None)

    await save_state()

    log_activity("auth", f"ادمین «{admin.get('username')}» حذف شد", "warn")

    return {"ok": True}


# ============================================================
# ADMIN REGISTRATION REQUESTS ("ثبت‌نام ادمینی" روی صفحه لاگین)
# ============================================================

def _admin_request_public(req_id: str, req: dict) -> dict:
    return {
        "id": req_id,
        "full_name": req.get("full_name", ""),
        "telegram_id": req.get("telegram_id", ""),
        "note": req.get("note", ""),
        "status": req.get("status", "pending"),
        "created_at": req.get("created_at"),
        "decided_at": req.get("decided_at"),
        "admin_id": req.get("admin_id"),
        "ip": req.get("ip"),
    }


@app.post("/api/admin-requests")
async def api_submit_admin_request(request: Request):
    """صفحه لاگین این را صدا می‌زند؛ نیازی به احراز هویت ندارد."""

    ip = request.client.host if request.client else "unknown"

    now = time.time()
    last = ADMIN_REQUEST_RATE.get(ip, 0)
    if now - last < ADMIN_REQUEST_COOLDOWN_SECONDS:
        raise HTTPException(
            status_code=429,
            detail="کمی صبر کنید و دوباره تلاش کنید",
        )

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    full_name = str(body.get("full_name", "")).strip()
    telegram_id = str(body.get("telegram_id", "")).strip().lstrip("@")
    note = str(body.get("note", "")).strip()[:500]

    if not full_name or len(full_name) < 3:
        raise HTTPException(status_code=400, detail="نام و نام خانوادگی را کامل وارد کنید")
    if not telegram_id or len(telegram_id) < 3:
        raise HTTPException(status_code=400, detail="آیدی تلگرام معتبر وارد کنید")

    ADMIN_REQUEST_RATE[ip] = now

    async with ADMIN_REQUESTS_LOCK:
        req_id = secrets.token_hex(6)
        ADMIN_REQUESTS[req_id] = {
            "full_name": full_name[:120],
            "telegram_id": telegram_id[:120],
            "note": note,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "decided_at": None,
            "admin_id": None,
            "ip": ip,
        }

    await save_state()

    log_activity(
        "auth",
        f"درخواست ثبت‌نام ادمین جدید از «{full_name}» (@{telegram_id})",
        "info",
    )

    return {"ok": True, "id": req_id}


@app.get("/api/admin-requests")
async def api_list_admin_requests(token=Depends(require_owner)):
    pending = sum(1 for r in ADMIN_REQUESTS.values() if r.get("status") == "pending")
    requests_list = sorted(
        (_admin_request_public(rid, r) for rid, r in ADMIN_REQUESTS.items()),
        key=lambda r: r.get("created_at") or "",
        reverse=True,
    )
    return {"ok": True, "requests": requests_list, "pending": pending}


@app.post("/api/admin-requests/{req_id}/approve")
async def api_approve_admin_request(req_id: str, request: Request, token=Depends(require_owner)):
    """مالک اینجا تصمیم می‌گیرد چه نام‌کاربری/رمز/دسترسی/شارژی به درخواست‌کننده بدهد
    و همان لحظه حساب ادمین واقعی برایش ساخته می‌شود."""

    req = ADMIN_REQUESTS.get(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    if req.get("status") != "pending":
        raise HTTPException(status_code=409, detail="این درخواست قبلاً بررسی شده است")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    username = str(body.get("username", "")).strip()
    password = str(body.get("password", "")).strip()

    if not username or username.lower() == "owner":
        raise HTTPException(status_code=400, detail="نام کاربری نامعتبر است")
    if len(password) < LOGIN_MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"رمز عبور باید حداقل {LOGIN_MIN_PASSWORD_LENGTH} کاراکتر باشد",
        )
    if username.lower() == AUTH.get("username", DEFAULT_ADMIN_USERNAME).lower():
        raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")
    for a in ADMINS.values():
        if a.get("username", "").lower() == username.lower():
            raise HTTPException(status_code=409, detail="این نام کاربری قبلاً استفاده شده است")

    credit_stars = safe_int(body.get("credit_stars"), default=0, minimum=0)

    admin_id = secrets.token_hex(6)
    ADMINS[admin_id] = {
        "username": username,
        "password_hash": hash_password(password),
        "role": "admin",
        "permissions": list(body.get("permissions") or {"dashboard", "inbounds", "subscriptions"}),
        "active": True,
        "created_at": datetime.now().isoformat(),
        "last_login_at": None,
        "last_login_ip": None,
        "credit_stars": credit_stars,
        "full_name": req.get("full_name", ""),
        "telegram_id": req.get("telegram_id", ""),
    }

    req["status"] = "approved"
    req["decided_at"] = datetime.now().isoformat()
    req["admin_id"] = admin_id

    await save_state()

    log_activity(
        "auth",
        f"درخواست «{req.get('full_name')}» تایید و حساب ادمین «{username}» ساخته شد",
        "ok",
    )

    delivery_message = (
        f"سلام {req.get('full_name','')} عزیز 👋\n\n"
        f"حساب ادمین شما در FaultPass فعال شد.\n\n"
        f"نام کاربری: {username}\n"
        f"رمز عبور: {password}\n\n"
        f"از طریق صفحه ورود پنل وارد شوید و رمز خود را در اولین فرصت تغییر دهید."
    )

    return {
        "ok": True,
        "admin": _admin_public(admin_id, ADMINS[admin_id]),
        "telegram_id": req.get("telegram_id", ""),
        "delivery_message": delivery_message,
    }


@app.post("/api/admin-requests/{req_id}/reject")
async def api_reject_admin_request(req_id: str, request: Request, token=Depends(require_owner)):
    req = ADMIN_REQUESTS.get(req_id)
    if not req:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    if req.get("status") != "pending":
        raise HTTPException(status_code=409, detail="این درخواست قبلاً بررسی شده است")

    try:
        body = await request.json()
    except Exception:
        body = {}

    reason = str((body or {}).get("reason", "")).strip()[:300]

    req["status"] = "rejected"
    req["decided_at"] = datetime.now().isoformat()
    req["note"] = reason or req.get("note", "")

    await save_state()

    log_activity("auth", f"درخواست ادمینی «{req.get('full_name')}» رد شد", "warn")

    return {"ok": True}


@app.delete("/api/admin-requests/{req_id}")
async def api_delete_admin_request(req_id: str, token=Depends(require_owner)):
    if req_id not in ADMIN_REQUESTS:
        raise HTTPException(status_code=404, detail="درخواست یافت نشد")
    ADMIN_REQUESTS.pop(req_id, None)
    await save_state()
    return {"ok": True}


# ============================================================
# BOT CONTROL CENTER
@app.get("/api/bot/texts")
async def api_bot_texts(token=Depends(require_owner)):
    return {"ok": True, "texts": BOT_TEXTS}

@app.post("/api/bot/texts")
async def api_bot_texts_save(request: Request, token=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")
    texts = body.get("texts") if isinstance(body, dict) else None
    if not isinstance(texts, dict):
        raise HTTPException(status_code=400, detail="ساختار متن‌ها نامعتبر است")
    for key in list(BOT_TEXTS):
        if key in texts:
            BOT_TEXTS[key] = str(texts[key])[:4000]
    await save_state()
    log_activity("bot", "متن‌های ربات از پنل بروزرسانی شد", "ok")
    return {"ok": True, "texts": BOT_TEXTS}

# PANEL SETTINGS (آدرس عمومی پنل + مدیریت ربات فروش از داخل پنل)
# ============================================================

@app.get("/api/settings")
async def api_get_settings(request: Request, token=Depends(require_owner)):
    bot_cfg = _bot_settings_snapshot()
    override_scheme, override_host = _split_base_url(CONFIG.get("public_base_url"))
    return {
        "ok": True,
        "public_base_url": CONFIG.get("public_base_url", ""),
        "effective_host": get_host(request),
        "effective_scheme": get_scheme(),
        "tcp_public_host": CONFIG.get("tcp_public_host", ""),
        "tcp_public_port": CONFIG.get("tcp_public_port", ""),
        "tcp_listen_port": _tcp_listen_port_snapshot(),
        "bot_token": bot_cfg.get("bot_token", ""),
        "bot_admin_ids": bot_cfg.get("admin_ids", ""),
        "bot_running": bot_cfg.get("running", False),
        "bot_auto_start": bool(CONFIG.get("bot_auto_start", False)),
        "admin_username": AUTH.get("username", DEFAULT_ADMIN_USERNAME),
        "sub_remark_show_name": bool(CONFIG.get("sub_remark_show_name", True)),
        "sub_remark_show_volume": bool(CONFIG.get("sub_remark_show_volume", False)),
        "sub_remark_show_id": bool(CONFIG.get("sub_remark_show_id", False)),
        "sub_remark_show_inbound": bool(CONFIG.get("sub_remark_show_inbound", False)),
        "sales_enabled": sales_enabled_now(),
        "name_style_enabled": name_style_on(),
    }


@app.post("/api/settings")
async def api_update_settings(request: Request, token=Depends(require_owner)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    bot_settings_changed = False

    if "public_base_url" in body:
        raw = str(body.get("public_base_url") or "").strip()
        # اعتبارسنجی سبک: اگه چیزی وارد شده، باید حداقل یک هاست معتبر ازش دربیاد
        if raw:
            _, parsed_host = _split_base_url(raw)
            if not parsed_host:
                raise HTTPException(status_code=400, detail="آدرس عمومی نامعتبر است (مثال درست: https://panel.example.com)")
        CONFIG["public_base_url"] = raw

    if "bot_auto_start" in body:
        CONFIG["bot_auto_start"] = bool(body.get("bot_auto_start"))

    if "tcp_public_host" in body:
        CONFIG["tcp_public_host"] = str(body.get("tcp_public_host") or "").strip()

    if "tcp_public_port" in body:
        raw_port = str(body.get("tcp_public_port") or "").strip()
        if raw_port and not raw_port.isdigit():
            raise HTTPException(status_code=400, detail="پورت عمومی TCP باید عدد باشد")
        CONFIG["tcp_public_port"] = raw_port

    for flag in ("sub_remark_show_name", "sub_remark_show_volume", "sub_remark_show_id", "sub_remark_show_inbound", "sales_enabled", "name_style_enabled"):
        if flag in body:
            CONFIG[flag] = bool(body.get(flag))

    try:
        import telegram_bot

        if "bot_token" in body or "bot_admin_ids" in body:
            new_token = body.get("bot_token")
            new_admin_ids = body.get("bot_admin_ids")
            telegram_bot.configure(
                token=(str(new_token).strip() if new_token is not None else None),
                admin_ids_raw=(str(new_admin_ids).strip() if new_admin_ids is not None else None),
            )
            bot_settings_changed = True
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("Bot configure error: %s", exc)

    await save_state()

    # اگه ربات از قبل روشن بوده و توکن/آیدی‌ها عوض شده، برای اعمال شدنِ واقعی
    # باید دوباره راه‌اندازی بشه (وگرنه با کانکشن قدیمی به توکن قبلی وصل می‌مونه)
    restarted = False
    try:
        import telegram_bot
        if bot_settings_changed and telegram_bot.is_running():
            await telegram_bot.restart_bot()
            restarted = True
    except Exception as exc:
        logger.warning("Bot restart error: %s", exc)

    log_activity("system", "تنظیمات پنل (آدرس عمومی/ربات) به‌روزرسانی شد", "ok")

    return {"ok": True, "bot_restarted": restarted, **_bot_settings_snapshot()}


@app.post("/api/settings/bot/start")
async def api_bot_start(token=Depends(require_owner)):
    try:
        import telegram_bot
        await telegram_bot.start_bot()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"خطا در روشن کردن ربات: {exc}")
    import telegram_bot
    if not telegram_bot.is_running():
        err = telegram_bot.last_start_error() or "ربات روشن نشد (دلیل نامشخص)"
        raise HTTPException(status_code=400, detail=err)
    log_activity("system", "ربات مدیریت پنل از داخل پنل روشن شد", "ok")
    return {"ok": True, **_bot_settings_snapshot()}


@app.post("/api/settings/bot/stop")
async def api_bot_stop(token=Depends(require_owner)):
    try:
        import telegram_bot
        await telegram_bot.stop_bot()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"خطا در خاموش کردن ربات: {exc}")
    log_activity("system", "ربات مدیریت پنل از داخل پنل خاموش شد", "warn")
    return {"ok": True, **_bot_settings_snapshot()}


# ============================================================
# PLAN MANAGEMENT (graphical, editable store plans)
# ============================================================

@app.get("/api/plans")
async def api_list_plans(token=Depends(require_auth)):
    import sales
    return {"ok": True, "plans": sales.list_plans()}


@app.post("/api/plans")
async def api_create_plan(request: Request, token=Depends(require_auth)):
    import sales

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    name = str(body.get("name", "")).strip() or "پلن جدید"

    raw_id = str(body.get("id") or name).strip().lower()
    plan_id = "".join(ch if (ch.isalnum() or ch == "-") else "-" for ch in raw_id.replace(" ", "-")).strip("-")
    plan_id = plan_id or f"plan-{secrets.token_hex(3)}"

    if sales.get_plan(plan_id):
        plan_id = f"{plan_id}-{secrets.token_hex(2)}"

    data = {
        "name": name,
        "days": safe_int(body.get("days"), default=30, minimum=0),
        "volume_gb": safe_float(body.get("volume_gb"), default=10, minimum=0),
        "speed_mbps": safe_float(body.get("speed_mbps"), default=0, minimum=0),
        "ip_limit": safe_int(body.get("ip_limit"), default=1, minimum=0),
        "stars": safe_int(body.get("stars"), default=99, minimum=0),
        "badge": str(body.get("badge", "")).strip(),
        "featured": bool(body.get("featured", False)),
        "order": safe_int(body.get("order"), default=len(sales.PLANS) + 1, minimum=0),
    }

    await sales.upsert_plan(plan_id, data)

    log_activity("plan", f"پلن «{name}» ایجاد شد", "ok")

    return {"ok": True, "plan": sales.get_plan(plan_id)}


@app.patch("/api/plans/{plan_id}")
async def api_update_plan(plan_id: str, request: Request, token=Depends(require_auth)):
    import sales

    existing = sales.get_plan(plan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="پلن یافت نشد")

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="اطلاعات نامعتبر است")

    updated = dict(existing)

    if "name" in body:
        updated["name"] = str(body["name"]).strip() or updated.get("name")
    if "badge" in body:
        updated["badge"] = str(body["badge"]).strip()
    if "days" in body:
        updated["days"] = safe_int(body["days"], default=existing.get("days", 0), minimum=0)
    if "ip_limit" in body:
        updated["ip_limit"] = safe_int(body["ip_limit"], default=existing.get("ip_limit", 0), minimum=0)
    if "stars" in body:
        updated["stars"] = safe_int(body["stars"], default=existing.get("stars", 0), minimum=0)
    if "order" in body:
        updated["order"] = safe_int(body["order"], default=existing.get("order", 0), minimum=0)
    if "volume_gb" in body:
        updated["volume_gb"] = safe_float(body["volume_gb"], default=existing.get("volume_gb", 0), minimum=0)
    if "speed_mbps" in body:
        updated["speed_mbps"] = safe_float(body["speed_mbps"], default=existing.get("speed_mbps", 0), minimum=0)
    if "featured" in body:
        updated["featured"] = bool(body["featured"])

    await sales.upsert_plan(plan_id, updated)

    log_activity("plan", f"پلن «{updated.get('name')}» ویرایش شد", "ok")

    return {"ok": True, "plan": sales.get_plan(plan_id)}


@app.delete("/api/plans/{plan_id}")
async def api_delete_plan(plan_id: str, token=Depends(require_auth)):
    import sales

    existing = sales.get_plan(plan_id)
    if not existing:
        raise HTTPException(status_code=404, detail="پلن یافت نشد")

    await sales.delete_plan(plan_id)

    log_activity("plan", f"پلن «{existing.get('name')}» حذف شد", "warn")

    return {"ok": True}


# ============================================================
# ADVANCED REPORTING
# ============================================================

@app.get("/api/reports/summary")
async def api_reports_summary(request: Request, token=Depends(require_auth)):
    days = safe_int(request.query_params.get("days"), default=14, minimum=1, maximum=180)

    today = datetime.now(IRAN_TZ) if IRAN_TZ else datetime.now()
    date_keys = [
        (today - timedelta(days=offset)).strftime("%Y-%m-%d")
        for offset in range(days - 1, -1, -1)
    ]

    series = []
    for key in date_keys:
        bucket = DAILY_STATS.get(key, {})
        series.append({
            "date": key,
            "traffic_mb": round(bucket.get("traffic_bytes", 0) / (1024 ** 2), 2),
            "new_links": bucket.get("new_links", 0),
            "orders": bucket.get("orders", 0),
            "stars": bucket.get("stars", 0),
        })

    now_ts = time.time()
    active_links = 0
    expired_links = 0
    unlimited_links = 0
    protocol_counts = defaultdict(int)
    top_links = []

    for uid, link in LINKS.items():
        protocol_counts[protocol_display_label(link)] += 1

        expires_at = link.get("expires_at")
        is_expired = False
        if expires_at:
            try:
                is_expired = datetime.fromisoformat(expires_at).timestamp() < now_ts
            except Exception:
                is_expired = False

        if is_expired:
            expired_links += 1
        else:
            active_links += 1

        if not link.get("limit_bytes"):
            unlimited_links += 1

        top_links.append({
            "uid": uid,
            "label": link.get("label", ""),
            "used_bytes": link.get("used_bytes", 0),
            "limit_bytes": link.get("limit_bytes", 0),
            "protocol": link.get("protocol", DEFAULT_PROTOCOL),
        })

    top_links.sort(key=lambda x: x["used_bytes"], reverse=True)

    import sales
    sales_totals = sales.sales_stats()

    return {
        "ok": True,
        "series": series,
        "totals": {
            "links": len(LINKS),
            "active_links": active_links,
            "expired_links": expired_links,
            "unlimited_links": unlimited_links,
            "subs": len(SUBS),
            "admins": len(ADMINS) + 1,
            "orders": sales_totals.get("orders", 0),
            "stars": sales_totals.get("stars", 0),
            "customers": sales_totals.get("customers", 0),
        },
        "protocol_distribution": [
            {"protocol": proto, "count": count} for proto, count in protocol_counts.items()
        ],
        "top_links": top_links[:10],
    }


@app.get("/api/reports/export.csv")
async def api_reports_export_csv(token=Depends(require_auth)):
    lines = ["uid,label,protocol,used_bytes,limit_bytes,expires_at,created_at"]

    for uid, link in LINKS.items():
        row = [
            uid,
            str(link.get("label", "")).replace(",", " "),
            link.get("protocol", DEFAULT_PROTOCOL),
            str(link.get("used_bytes", 0)),
            str(link.get("limit_bytes", 0)),
            str(link.get("expires_at", "") or ""),
            str(link.get("created_at", "") or ""),
        ]
        lines.append(",".join(row))

    csv_content = "\n".join(lines)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=faultpass-links-report.csv"},
    )


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):

    stats[
        "total_errors"
    ] += 1

    error_logs.append(
        {
            "error": str(exc) or "internal server error",
            "path": str(request.url.path),
            "method": request.method,
            "source": "server",
            "level": "err",
            "time": datetime.now().isoformat(),
        }
    )

    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url,
    )

    # API requests
    if (
        request.url.path.startswith(
            "/api/"
        )
        or request.url.path == "/stats"
    ):

        return JSONResponse(
            {
                "ok": False,
                "error":
                    str(exc)
                or "internal server error",
            },
            status_code=500,
        )

    return HTMLResponse(
        """
        <html lang="fa" dir="rtl">
        <body style="
            background:#07070a;
            color:#fff;
            font-family:sans-serif;
            padding:40px;
        ">
            <h2>
            خطای داخلی FaultPass
            </h2>

            <p>
            لطفاً لاگ Railway را بررسی کنید.
            </p>
        </body>
        </html>
        """,
        status_code=500,
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        workers=1,
    )
