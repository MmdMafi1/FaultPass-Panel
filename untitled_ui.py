"""Untitled UI v2.0 design system — shared theme for the whole FaultPass panel.

Same tokens as the subscription page (main.py /subscription/{uuid}).
`inject(html)` appends the theme right before </head> so it overrides the
legacy styles without touching page logic / JS.
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
         '&family=Vazirmatn:wght@400;500;600;700&display=swap" rel="stylesheet">')

TOKENS = r"""
:root{
  --gray-25:#FCFCFD;--gray-50:#F9FAFB;--gray-100:#F2F4F7;--gray-200:#EAECF0;--gray-300:#D0D5DD;--gray-400:#98A2B3;--gray-500:#667085;--gray-600:#475467;--gray-700:#344054;--gray-800:#182230;--gray-900:#101828;--gray-950:#0C111D;
  --brand-25:#FCFAFF;--brand-50:#F9F5FF;--brand-100:#F4EBFF;--brand-200:#E9D7FE;--brand-300:#D6BBFB;--brand-400:#B692F6;--brand-500:#9E77ED;--brand-600:#7F56D9;--brand-700:#6941C6;--brand-800:#53389E;--brand-900:#42307D;
  --success-50:#ECFDF3;--success-200:#ABEFC6;--success-500:#17B26A;--success-600:#079455;--success-700:#067647;
  --error-50:#FEF3F2;--error-200:#FECDCA;--error-500:#F04438;--error-600:#D92D20;--error-700:#B42318;
  --warning-50:#FFFAEB;--warning-200:#FEDF89;--warning-500:#F79009;--warning-600:#DC6803;--warning-700:#B54708;
  --radius-sm:6px;--radius-md:8px;--radius-lg:10px;--radius-xl:12px;--radius-2xl:16px;--radius-full:9999px;
  --ring-brand:0 0 0 4px rgba(158,119,237,.24);--ring-error:0 0 0 4px rgba(240,68,56,.24);
}
/* ---- dark (default) : Untitled UI dark mode ---- */
:root,[data-theme="dark"]{
  --bg-primary:#0C111D;--bg-secondary:#161B26;--bg-tertiary:#1F242F;--bg-active:#1F242F;
  --border-primary:#333741;--border-secondary:#1F242F;
  --text-primary:#F5F5F6;--text-secondary:#CECFD2;--text-tertiary:#94969C;--text-placeholder:#85888E;
  --b-success-bg:#053321;--b-success-bd:#085D3A;--b-success-tx:#75E0A7;
  --b-error-bg:#55160C;--b-error-bd:#912018;--b-error-tx:#FDA29B;
  --b-warning-bg:#4E1D09;--b-warning-bd:#93370D;--b-warning-tx:#FEC84B;
  --b-gray-bg:#161B26;--b-gray-bd:#333741;--b-gray-tx:#CECFD2;
  --b-brand-bg:#2C1C5F;--b-brand-bd:#53389E;--b-brand-tx:#D6BBFB;
  --shadow-xs:0 1px 2px rgba(0,0,0,.4);--shadow-sm:0 1px 3px rgba(0,0,0,.4),0 1px 2px rgba(0,0,0,.3);
  --shadow-md:0 4px 8px -2px rgba(0,0,0,.45);--shadow-lg:0 12px 16px -4px rgba(0,0,0,.5);--shadow-xl:0 20px 24px -4px rgba(0,0,0,.55);
  /* legacy aliases used all over the panel */
  --bg:var(--bg-primary);--panel:var(--bg-primary);--panel2:var(--bg-secondary);--line:var(--border-secondary);--line2:var(--border-primary);
  --text:var(--text-primary);--sub:var(--text-tertiary);--sub2:var(--text-placeholder);--muted:var(--text-tertiary);--soft:var(--text-placeholder);
  --accent:var(--brand-600);--accent-d:var(--brand-700);--accent2:var(--brand-700);--accent3:var(--success-500);
  --good:var(--success-500);--green:var(--success-500);--warn:var(--warning-500);--bad:var(--error-500);--danger:var(--error-500);--red:var(--error-500);
}
[data-theme="light"]{
  --bg-primary:#FFFFFF;--bg-secondary:var(--gray-50);--bg-tertiary:var(--gray-100);--bg-active:var(--gray-50);
  --border-primary:var(--gray-300);--border-secondary:var(--gray-200);
  --text-primary:var(--gray-900);--text-secondary:var(--gray-700);--text-tertiary:var(--gray-600);--text-placeholder:var(--gray-500);
  --b-success-bg:var(--success-50);--b-success-bd:var(--success-200);--b-success-tx:var(--success-700);
  --b-error-bg:var(--error-50);--b-error-bd:var(--error-200);--b-error-tx:var(--error-700);
  --b-warning-bg:var(--warning-50);--b-warning-bd:var(--warning-200);--b-warning-tx:var(--warning-700);
  --b-gray-bg:var(--gray-50);--b-gray-bd:var(--gray-200);--b-gray-tx:var(--gray-700);
  --b-brand-bg:var(--brand-50);--b-brand-bd:var(--brand-200);--b-brand-tx:var(--brand-700);
  --shadow-xs:0 1px 2px rgba(16,24,40,.05);--shadow-sm:0 1px 3px rgba(16,24,40,.10),0 1px 2px rgba(16,24,40,.06);
  --shadow-md:0 4px 8px -2px rgba(16,24,40,.10),0 2px 4px -2px rgba(16,24,40,.06);--shadow-lg:0 12px 16px -4px rgba(16,24,40,.08),0 4px 6px -2px rgba(16,24,40,.03);
  --shadow-xl:0 20px 24px -4px rgba(16,24,40,.08),0 8px 8px -4px rgba(16,24,40,.03);
  --bg:var(--bg-secondary);--panel:var(--bg-primary);--panel2:var(--bg-secondary);--line:var(--border-secondary);--line2:var(--border-primary);
  --text:var(--text-primary);--sub:var(--text-tertiary);--sub2:var(--text-placeholder);--muted:var(--text-tertiary);--soft:var(--text-placeholder);
}
"""

BASE = r"""
html,body{background:var(--bg-secondary)!important;background-image:none!important;color:var(--text-primary)}
body:before,body:after{display:none!important}
body{font-family:Inter,Vazirmatn,Tahoma,sans-serif;font-size:14px;line-height:20px;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{color:var(--text-primary);letter-spacing:-.01em}
::selection{background:var(--brand-200);color:var(--brand-900)}
:focus-visible{outline:none;box-shadow:var(--ring-brand)}
input,select,textarea{font-family:inherit}
input[type=checkbox],input[type=radio]{accent-color:var(--brand-600)}
.mono,code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
"""

COMPONENTS = r"""
/* ============ buttons ============ */
.btn,.btn-main,.pro-action{border-radius:var(--radius-md)!important;font-weight:600!important;font-size:14px;line-height:20px;box-shadow:var(--shadow-xs)!important;transform:none!important;filter:none!important;transition:background-color .14s,border-color .14s,color .14s,box-shadow .14s}
.btn{padding:10px 16px;background:var(--bg-primary)!important;border:1px solid var(--border-primary)!important;color:var(--text-secondary)!important}
.btn:hover{background:var(--bg-secondary)!important;color:var(--text-primary)!important}
.btn:focus-visible{box-shadow:var(--shadow-xs),var(--ring-gray,0 0 0 4px rgba(152,162,179,.14))!important}
.btn.primary,.btn-main{background:var(--brand-600)!important;border:1px solid var(--brand-600)!important;color:#fff!important}
.btn.primary:hover,.btn-main:hover{background:var(--brand-700)!important;border-color:var(--brand-700)!important}
.btn.primary:focus-visible,.btn-main:focus-visible{box-shadow:var(--shadow-xs),var(--ring-brand)!important}
.btn.danger{background:var(--bg-primary)!important;color:var(--b-error-tx)!important;border-color:var(--b-error-bd)!important}
.btn.danger:hover{background:var(--b-error-bg)!important}
.btn.sm{padding:8px 14px;font-size:13px}
.btn:disabled,.btn-main:disabled{opacity:1;background:var(--bg-tertiary)!important;border-color:var(--border-secondary)!important;color:var(--text-placeholder)!important;box-shadow:none!important}
.iconbtn,.icon-btn,.hamburger,.areg-close{border-radius:var(--radius-md)!important;background:var(--bg-primary)!important;border:1px solid var(--border-primary)!important;color:var(--text-tertiary)!important;box-shadow:var(--shadow-xs)!important;transform:none!important}
.iconbtn:hover,.icon-btn:hover,.hamburger:hover,.areg-close:hover{background:var(--bg-secondary)!important;color:var(--text-primary)!important}
.iconbtn.danger{color:var(--b-error-tx)!important}

/* ============ inputs ============ */
.grp input,.grp select,.grp textarea,.search input,select.sel,.inp input,.endpoint-input,.bot-text-grid textarea,input[type=text],input[type=password],input[type=number],input[type=email],input[type=url],textarea,select{
  background:var(--bg-primary)!important;border:1px solid var(--border-primary)!important;border-radius:var(--radius-md)!important;color:var(--text-primary)!important;box-shadow:var(--shadow-xs)!important;font-size:14px}
.grp input:focus,.grp select:focus,.grp textarea:focus,.search input:focus,select.sel:focus,.inp input:focus,input:focus,textarea:focus,select:focus{border-color:var(--brand-300)!important;box-shadow:var(--shadow-xs),var(--ring-brand)!important;outline:none}
[data-theme="dark"] .grp input:focus,[data-theme="dark"] input:focus,[data-theme="dark"] textarea:focus,[data-theme="dark"] select:focus,:root:not([data-theme]) input:focus{border-color:var(--brand-500)!important}
input::placeholder,textarea::placeholder{color:var(--text-placeholder)!important}
.grp label,.field label,.appearance-field label{color:var(--text-secondary)!important;font-weight:500!important;font-size:14px!important}
.hint,.ib-help,.areg-hint{color:var(--text-tertiary)!important}
input.tpl-switch:checked{background:var(--brand-600)!important}

/* ============ cards / surfaces ============ */
.card,.stat-card,.resource-card,.message-stat,.admin-card,.ib-section,.appearance-card,.ib-hero,.admins-hero,.inbound-strip>div,.ib-quickstats>div,.tpl-row,.perm-item,.areq-row,.ib-mini,.sum,.diag-item,.health-row,.ob-box,.ib-status,.notice{
  background:var(--bg-primary)!important;background-image:none!important;border:1px solid var(--border-secondary)!important;border-radius:var(--radius-xl)!important;box-shadow:var(--shadow-xs)!important;transform:none!important}
.card,.stat-card,.resource-card,.message-stat,.admin-card,.appearance-card{box-shadow:var(--shadow-sm)!important}
.card:hover,.admin-card:hover,.stat-card:hover{transform:none!important}
.admin-card:before,.admin-avatar:after{display:none!important}
.admin-card.is-owner{border-color:var(--b-warning-bd)!important}
.panel-head,.ib-section-head{border-bottom:1px solid var(--border-secondary)!important;background:transparent!important}
.panel-head b,.panel-head h3{font-size:18px;font-weight:600;color:var(--text-primary)}
.stat-card .sc-val{font-size:30px;line-height:38px;font-weight:600;letter-spacing:-.02em}
.stat-card .sc-label{font-size:14px;color:var(--text-tertiary);font-weight:500}
.stat-card .sc-icon,.ib-hero .ib-icon,.admin-avatar,.feature-lock-icon,.ob-emoji{background:var(--b-brand-bg)!important;color:var(--brand-600)!important;border:1px solid var(--b-brand-bd);box-shadow:none!important;border-radius:var(--radius-md)!important}
[data-theme="dark"] .stat-card .sc-icon,:root:not([data-theme]) .stat-card .sc-icon{color:var(--brand-300)!important}
.ib-opt{background:var(--bg-primary)!important;border:1px solid var(--border-secondary)!important;border-radius:var(--radius-xl)!important;box-shadow:none!important;transform:none!important}
.ib-opt.on{border:2px solid var(--brand-600)!important;background:var(--b-brand-bg)!important}
.ib-opt .ib-opt-icon,.ib-step .num{background:var(--b-brand-bg)!important;color:var(--brand-600)!important}
.ib-choice span{border-radius:var(--radius-md)!important;background:var(--bg-primary)!important;border-color:var(--border-primary)!important}
.ib-choice input:checked+span{border-color:var(--brand-600)!important;background:var(--b-brand-bg)!important;color:var(--b-brand-tx)!important}
.ib-bulkbar{background:var(--b-brand-bg)!important;border:1px solid var(--b-brand-bd)!important;border-radius:var(--radius-xl)!important}
.divider,.ib-divider{background:var(--border-secondary)!important}

/* ============ page header ============ */
.pg-head h1{font-size:24px;line-height:32px;font-weight:600}
.pg-head p{font-size:14px;color:var(--text-tertiary)}
.section-title{color:var(--text-tertiary)!important;font-weight:600!important;text-transform:none!important;letter-spacing:0!important;font-size:14px!important}
.eyebrow,.command-badge{color:var(--brand-600)!important;background:var(--b-brand-bg)!important;border-color:var(--b-brand-bd)!important}

/* ============ table ============ */
table{font-size:14px}
thead th{background:var(--bg-secondary)!important;color:var(--text-tertiary)!important;font-size:12px!important;font-weight:500!important;line-height:18px;padding:12px 24px!important;border-bottom:1px solid var(--border-secondary)!important}
tbody td{padding:16px 24px!important;border-bottom:1px solid var(--border-secondary)!important;color:var(--text-tertiary)}
tbody td:first-child{color:var(--text-primary);font-weight:500}
tbody tr:hover{background:var(--bg-secondary)!important}

/* ============ badges (pill) ============ */
.badge,.admin-role-badge,.admin-perm-chip,.tpl-preview-proto,.ib-count{display:inline-flex;align-items:center;gap:6px;padding:2px 10px!important;border-radius:var(--radius-full)!important;border:1px solid var(--b-gray-bd)!important;background:var(--b-gray-bg)!important;color:var(--b-gray-tx)!important;font-size:12px!important;line-height:18px;font-weight:500!important}
.badge.green{border-color:var(--b-success-bd)!important;background:var(--b-success-bg)!important;color:var(--b-success-tx)!important}
.badge.red{border-color:var(--b-error-bd)!important;background:var(--b-error-bg)!important;color:var(--b-error-tx)!important}
.badge.orange{border-color:var(--b-warning-bd)!important;background:var(--b-warning-bg)!important;color:var(--b-warning-tx)!important}
.admin-role-badge.admin,.tpl-preview-proto{border-color:var(--b-brand-bd)!important;background:var(--b-brand-bg)!important;color:var(--b-brand-tx)!important}
.badge.green:before,.badge.red:before,.badge.orange:before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}

/* ============ sidebar / nav ============ */
.sidebar,[data-theme="dark"] .sidebar,[data-theme="light"] .sidebar,:root:not([data-theme]) .sidebar{background:var(--bg-primary)!important;background-image:none!important;border-left:1px solid var(--border-secondary)!important;box-shadow:none!important}
.sidebar-brand{border-bottom:0!important;padding:24px 20px 8px!important}
.sidebar-brand img{border-radius:var(--radius-md)!important;box-shadow:var(--shadow-xs)!important}
.sidebar-brand div{font-weight:600!important;font-size:16px!important}
.tab{padding:8px 12px!important;border-radius:var(--radius-sm)!important;font-size:16px;line-height:24px;font-weight:600!important;color:var(--text-secondary)!important;border:0!important;margin:1px 0!important;box-shadow:none!important;background:transparent!important}
.tab i{color:var(--text-placeholder)}
.tab:hover{background:var(--bg-secondary)!important;color:var(--text-primary)!important}
.tab.on{background:var(--bg-active)!important;color:var(--text-primary)!important;box-shadow:none!important}
.tab.on i{color:var(--brand-600)}
.tab .bd,.tab.on .bd{background:var(--b-gray-bg)!important;border:1px solid var(--b-gray-bd);color:var(--b-gray-tx);font-size:12px;font-weight:500}
.sidebar-foot{border-top:1px solid var(--border-secondary)!important}
.lang-mini,.lang-switch,.theme-pills{background:var(--bg-secondary)!important;border:1px solid var(--border-secondary)!important;border-radius:var(--radius-md)!important}
.lang-mini button,.lang-switch button{border-radius:var(--radius-sm)!important;color:var(--text-tertiary)!important}
.lang-mini button.on,.lang-switch button.on,.theme-pill.on{background:var(--bg-primary)!important;color:var(--text-secondary)!important;box-shadow:var(--shadow-sm)!important}
.topbar,[data-theme="dark"] .topbar,[data-theme="light"] .topbar,:root:not([data-theme]) .topbar{background:var(--bg-primary)!important;border-bottom:1px solid var(--border-secondary)!important;box-shadow:none!important;backdrop-filter:none!important}
.page-title{font-weight:600!important;font-size:18px!important}
.user-chip{background:var(--bg-primary)!important;border:1px solid var(--border-primary)!important;border-radius:var(--radius-full)!important;box-shadow:var(--shadow-xs)}
.user-chip .av{background:var(--b-brand-bg)!important;color:var(--brand-600)!important;font-weight:600!important}

/* ============ drawer / modal / toast ============ */
.overlay,.sidebar-overlay{background:rgba(12,17,29,.7)!important;backdrop-filter:blur(8px)!important}
.drawer,.areg-box{background:var(--bg-primary)!important;border:1px solid var(--border-secondary)!important;box-shadow:var(--shadow-xl)!important}
.areg-box{border-radius:var(--radius-2xl)!important}
.dr-head,.dr-foot{border-color:var(--border-secondary)!important}
.dr-head h3{font-size:18px;font-weight:600}
.toast{background:var(--bg-primary)!important;border:1px solid var(--border-primary)!important;border-radius:var(--radius-xl)!important;box-shadow:var(--shadow-lg)!important;color:var(--text-primary)}
.toast.ok i{color:var(--success-500)!important}.toast.err i{color:var(--error-500)!important}

/* ============ misc ============ */
.bar-mini{background:var(--bg-tertiary)!important;border-radius:var(--radius-full)!important}
.bar-mini i{background:var(--brand-600)!important}
.empty{color:var(--text-tertiary)!important}
::-webkit-scrollbar-thumb{background:var(--border-primary)!important}
"""

LOGIN_EXTRA = r"""
.card{border-radius:var(--radius-xl)!important;padding:32px!important;box-shadow:var(--shadow-xl)!important}
.badge{width:56px!important;height:56px!important;padding:0!important;border-radius:var(--radius-xl)!important;box-shadow:var(--shadow-sm)!important}
h1{font-size:30px!important;line-height:38px!important;font-weight:600!important}
.subtitle{color:var(--text-tertiary)!important;font-size:16px!important}
.inp input{padding-top:10px!important;padding-bottom:10px!important}
.security-strip span{background:var(--bg-primary)!important;border-color:var(--border-secondary)!important;border-radius:var(--radius-full)!important}
.security-strip i{color:var(--brand-600)!important}
.admin-reg-btn{border-radius:var(--radius-md)!important;border-style:solid!important;border-color:var(--border-primary)!important;background:var(--bg-primary)!important;color:var(--text-secondary)!important}
"""

PUBLIC_EXTRA = r"""
.hero,.panel,.kpi,.link,.mini,.qr-card,.tech>div,.stat,.box,.plan,.card{background:var(--bg-primary)!important;background-image:none!important;border:1px solid var(--border-secondary)!important;border-radius:var(--radius-xl)!important;box-shadow:var(--shadow-sm)!important}
.hero:after,.hero:before{display:none!important}
.btn,a.btn,button.btn{border-radius:var(--radius-md)!important;background:var(--brand-600)!important;border:1px solid var(--brand-600)!important;color:#fff!important;font-weight:600!important;box-shadow:var(--shadow-xs)!important;background-image:none!important}
.btn.alt{background:var(--bg-primary)!important;color:var(--text-secondary)!important;border-color:var(--border-primary)!important}
.mark,.ico,.logo{background:var(--b-brand-bg)!important;border:1px solid var(--b-brand-bd)!important;border-radius:var(--radius-md)!important;box-shadow:none!important}
.online,.badge,.tag{border-radius:var(--radius-full)!important;border:1px solid var(--b-success-bd)!important;background:var(--b-success-bg)!important;color:var(--b-success-tx)!important;font-weight:500}
.offline{border-color:var(--b-error-bd)!important;background:var(--b-error-bg)!important;color:var(--b-error-tx)!important}
.muted,.sub,.cap,small{color:var(--text-tertiary)!important}
.url{background:var(--bg-secondary)!important;border:1px solid var(--border-primary)!important;border-radius:var(--radius-md)!important}
"""

def css(kind: str = "app") -> str:
    extra = {"login": LOGIN_EXTRA, "public": PUBLIC_EXTRA}.get(kind, "")
    return FONTS + "<style id=\"untitled-ui\">" + TOKENS + BASE + COMPONENTS + extra + "</style>"

def inject(html: str, kind: str = "app") -> str:
    i = html.find("</head>")
    return html if i < 0 else html[:i] + css(kind) + html[i:]
