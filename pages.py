LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl" id="htmlRoot">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FaultPass | Login</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&family=Estedad:wght@400;500;600;700;800;900&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700;800&family=Shabnam:wght@400;500;700&family=Yekan+Bakh:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#08050f;--panel:rgba(255,255,255,.035);--line:rgba(255,255,255,.09);--line2:rgba(255,255,255,.16);
  --accent:#3b82f6;--accent2:#1d4ed8;--accent3:#22c55e;
  --text:#f3f0fa;--sub:#9c93b5;--sub2:#655d7e;
  --font-fa:'Vazirmatn',sans-serif;--font-en:'Inter',sans-serif;
}
html,body{background:var(--bg);color:var(--text);min-height:100%;font-family:var(--font-fa)}
html[data-lang="en"] body{font-family:var(--font-en)}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer}
body{
  min-height:100vh;min-height:100svh;min-height:100dvh;display:flex;align-items:center;justify-content:center;position:relative;overflow-x:hidden;overflow-y:auto;padding:24px;
  background:
    radial-gradient(48% 40% at 50% 8%, rgba(59,130,246,.30), transparent 60%),
    radial-gradient(40% 35% at 12% 85%, rgba(124,58,237,.22), transparent 60%),
    radial-gradient(40% 35% at 90% 80%, rgba(34,197,94,.10), transparent 60%),
    #08050f;
}
/* روی صفحات کوتاه (موبایل، زوم بالا، پنجره کوچک) اجازه می‌ده کاربر اسکرول کنه
   تا کل کارت (شامل دکمه‌ی «ثبت‌نام ادمینی» زیر کارت ورود) قابل دیدن و کلیک باشه؛
   وقتی محتوا داخل صفحه جا می‌شه ظاهر صفحه دقیقاً مثل قبل باقی می‌مونه. */
@media (max-height:760px){
  body{align-items:flex-start;padding-top:28px;padding-bottom:28px}
}
.grid-bg{position:absolute;inset:0;opacity:.35;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:38px 38px;mask-image:radial-gradient(65% 55% at 50% 30%,#000 20%,transparent 85%)}
 .grid-bg:before{content:"";position:absolute;inset:-2%;background:conic-gradient(from 0deg,transparent 0deg,rgba(59,130,246,.12) 65deg,transparent 130deg,rgba(62,166,255,.10) 210deg,transparent 290deg);filter:blur(24px);animation:ambientSpin 18s linear infinite;will-change:transform;contain:strict}
@keyframes ambientSpin{to{transform:rotate(360deg)}}
.scanline{position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,transparent 0%,rgba(255,255,255,.025) 48%,transparent 52%);background-size:100% 180px;animation:scan 7s linear infinite;mix-blend-mode:screen}
@keyframes scan{to{background-position:0 180px}}
.ambient-orb{position:absolute;border-radius:50%;filter:blur(2px);opacity:.45;animation:floatOrb 9s ease-in-out infinite}
.ambient-orb.a{width:180px;height:180px;right:9%;top:12%;background:radial-gradient(circle,rgba(59,130,246,.35),transparent 70%)}
.ambient-orb.b{width:240px;height:240px;left:3%;bottom:3%;background:radial-gradient(circle,rgba(62,166,255,.22),transparent 70%);animation-delay:-3s}
@keyframes floatOrb{0%,100%{transform:translate3d(0,0,0)}50%{transform:translate3d(0,-18px,0)}}
.dot{position:absolute;width:3px;height:3px;border-radius:50%;background:#c9a8ff;opacity:.6;animation:twinkle 3.4s ease-in-out infinite}
@keyframes twinkle{0%,100%{opacity:.15;transform:scale(1)}50%{opacity:.9;transform:scale(1.6)}}

.lang-switch{position:absolute;top:22px;left:22px;z-index:5;display:flex;background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:100px;padding:3px;gap:2px}
html[dir="rtl"] .lang-switch{left:auto;right:22px}
.lang-switch button{padding:6px 14px;border:0;background:transparent;color:var(--sub);font-size:12px;font-weight:700;border-radius:100px;transition:.15s}
.lang-switch button.on{background:linear-gradient(90deg,var(--accent2),var(--accent));color:#fff}

.wrap{position:relative;z-index:1;width:100%;max-width:420px;display:flex;flex-direction:column;align-items:center;animation:rise .55s cubic-bezier(.2,.8,.2,1) both}
.wrap{position:relative;z-index:1;width:100%;max-width:470px;display:flex;flex-direction:column;align-items:center;animation:rise .65s cubic-bezier(.2,.8,.2,1) both}
.login-status{display:flex;align-items:center;gap:8px;margin:0 0 12px;padding:7px 11px;border-radius:999px;border:1px solid rgba(62,166,255,.18);background:rgba(10,18,32,.58);box-shadow:0 8px 30px rgba(0,0,0,.18);font-size:9px;letter-spacing:.12em;color:#9ecfff;text-transform:uppercase}.login-status .live{width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 0 5px rgba(52,211,153,.08),0 0 14px rgba(52,211,153,.8);animation:statusPulse 1.8s ease-in-out infinite}@keyframes statusPulse{50%{transform:scale(1.25);opacity:.65}}
.security-strip{display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-top:14px}.security-strip span{font-size:8.5px;color:var(--sub);padding:6px 8px;border:1px solid var(--line);border-radius:8px;background:rgba(255,255,255,.025)}.security-strip i{color:#8fd9ff;margin-left:3px}
.login-card-glow{position:absolute;inset:-1px;border-radius:23px;background:conic-gradient(from 180deg,rgba(59,130,246,.0),rgba(59,130,246,.55),rgba(62,166,255,.35),rgba(59,130,246,.0));filter:blur(8px);opacity:.18;z-index:-1;animation:cardGlow 8s linear infinite;will-change:transform;contain:strict}@keyframes cardGlow{to{transform:rotate(360deg)}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

.badge-wrap{position:relative;width:92px;height:92px;margin:14px 0 30px}
.orbit-ring{position:absolute;inset:-24px;border-radius:50%;border:1px dashed rgba(59,130,246,.35);animation:orbitspin 7s linear infinite}
.orbit-ring2{position:absolute;inset:-38px;border-radius:50%;border:1px dashed rgba(62,166,255,.20);animation:orbitspin 12s linear infinite reverse}
.planet{position:absolute;top:-5px;left:50%;width:10px;height:10px;margin-left:-5px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#c9f0ff,#3ea6ff 55%,#1c5fa8 100%);box-shadow:0 0 12px 2px rgba(62,166,255,.85)}
.planet2{position:absolute;bottom:-4px;left:50%;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#f3d9ff,#3b82f6 60%,#1d4ed8 100%);box-shadow:0 0 9px 2px rgba(59,130,246,.85)}
@keyframes orbitspin{to{transform:rotate(360deg)}}
.badge-glow{position:absolute;inset:-14px;border-radius:50%;background:radial-gradient(circle,rgba(59,130,246,.55),transparent 70%);filter:blur(6px);animation:pulseGlow 2.6s ease-in-out infinite;will-change:transform,opacity;contain:strict}
@keyframes pulseGlow{0%,100%{opacity:.6;transform:scale(1)}50%{opacity:1;transform:scale(1.08)}}
.badge{position:relative;width:92px;height:92px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,255,255,.18);box-shadow:0 10px 40px -6px rgba(59,130,246,.7);background:#150c26;display:flex;align-items:center;justify-content:center}
.badge img{width:100%;height:100%;object-fit:cover}

.brand-caps{font-size:12px;font-weight:800;letter-spacing:.32em;color:#c9a8ff;margin-bottom:14px}
h1{font-size:29px;font-weight:900;text-align:center;line-height:1.5;color:var(--text)}
h1 .g{background:linear-gradient(90deg,#c9a8ff,#3b82f6,#8fd9ff);-webkit-background-clip:text;background-clip:text;color:transparent}
.subtitle{margin-top:10px;font-size:13.5px;color:var(--sub);text-align:center;line-height:1.9;max-width:340px}

.card{position:relative;
  width:100%;margin-top:28px;padding:30px 28px;border-radius:24px;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.015));
  border:1px solid var(--line);backdrop-filter:none;
  box-shadow:0 36px 100px -26px rgba(0,0,0,.62), inset 0 1px 0 rgba(255,255,255,.05);
}
.field{margin-bottom:16px}
.field label{display:block;font-size:12px;font-weight:700;color:var(--sub);margin-bottom:8px}
.inp{position:relative}
.inp input{width:100%;padding:14px 44px;border-radius:12px;border:1px solid var(--line);background:rgba(0,0,0,.28);color:var(--text);font-size:14px;outline:none;transition:.15s;font-family:inherit}
.inp input::placeholder{color:var(--sub2)}
.inp input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(59,130,246,.20)}
.inp i.i-lead{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--sub);font-size:16px;pointer-events:none}
html[dir="ltr"] .inp i.i-lead{right:auto;left:14px}
html[dir="ltr"] .inp input{padding:13px 42px}
.toggle-eye{position:absolute;left:12px;top:50%;transform:translateY(-50%);background:none;border:0;color:var(--sub);font-size:16px;padding:4px;border-radius:6px;transition:.15s}
html[dir="ltr"] .toggle-eye{left:auto;right:12px}
.toggle-eye:hover{color:var(--text);background:rgba(255,255,255,.07)}
.remember{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--sub);margin:2px 0 20px;user-select:none;cursor:pointer}
.remember input{accent-color:var(--accent);width:15px;height:15px}
.error{display:flex;gap:8px;align-items:center;background:rgba(239,68,68,.10);border:1px solid rgba(239,68,68,.30);color:#ff9b9b;border-radius:11px;padding:11px 13px;font-size:12.5px;margin-bottom:16px}
.error::before{content:"\ea87";font-family:"tabler-icons";font-size:15px;flex-shrink:0}
.btn-main{width:100%;padding:15px;border:0;border-radius:12px;background:linear-gradient(90deg,var(--accent2),var(--accent));color:#fff;font-weight:800;font-size:14.5px;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:.18s;box-shadow:0 14px 30px -10px rgba(59,130,246,.65)}
.btn-main:hover{filter:brightness(1.08);transform:translateY(-1px)}
.btn-main:active{transform:translateY(0)}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{animation:spin .7s linear infinite}
.foot{margin-top:22px;text-align:center;font-size:11.5px;color:var(--sub2)}
.admin-reg-row{margin-top:16px;padding-top:14px;border-top:1px dashed var(--line);text-align:center}
.admin-reg-btn{width:100%;background:rgba(255,255,255,.03);border:1px dashed var(--line2);color:var(--sub);padding:11px;border-radius:12px;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:8px;transition:.15s}
.admin-reg-btn:hover{color:var(--text);border-color:var(--accent);background:rgba(59,130,246,.07)}
.areg-overlay{position:fixed;inset:0;z-index:50;display:none;align-items:center;justify-content:center;background:rgba(4,2,10,.72);backdrop-filter:blur(3px);padding:18px}
.areg-overlay.show{display:flex}
.areg-box{width:100%;max-width:420px;max-height:88vh;overflow:auto;padding:24px;border-radius:20px;background:#100a1e;border:1px solid var(--line2);box-shadow:0 40px 100px -20px rgba(0,0,0,.7);animation:rise .35s ease both}
.areg-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:16px}
.areg-badge{display:inline-flex;align-items:center;gap:6px;font-size:9.5px;font-weight:800;color:#c9a8ff;background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.25);padding:5px 10px;border-radius:999px;margin-bottom:9px}
.areg-head h3{font-size:17px;font-weight:900;margin:0 0 6px}
.areg-head p{font-size:11.5px;color:var(--sub);line-height:1.8;margin:0;max-width:300px}
.areg-close{background:rgba(255,255,255,.06);border:1px solid var(--line);color:var(--sub);width:32px;height:32px;border-radius:10px;flex-shrink:0;display:grid;place-items:center}
.areg-close:hover{color:var(--text)}
.areg-msg{font-size:12px;border-radius:10px;padding:10px 12px;margin-bottom:14px;line-height:1.8}
.areg-msg.ok{background:rgba(34,197,94,.10);border:1px solid rgba(34,197,94,.28);color:#7cf0a8}
.areg-msg.err{background:rgba(239,68,68,.10);border:1px solid rgba(239,68,68,.30);color:#ff9b9b}
.areg-hint{margin-top:14px;font-size:10.5px;color:var(--sub2);line-height:1.9;text-align:center}
@media(max-width:480px){h1{font-size:24px}.card{padding:22px 18px}.login-status{font-size:7.5px}.security-strip span{font-size:7.5px}}
@media (prefers-reduced-motion: reduce){
  .grid-bg:before,.scanline,.ambient-orb,.dot,.login-card-glow,.orbit-ring,.orbit-ring2,.badge-glow,.login-status .live,.wrap{animation:none!important}
}
@media (max-width:820px), (pointer:coarse){
  /* Phones/low-end GPUs: the jank came from the blurred/filtered layers being
     repainted every frame (conic-gradient + blur, glow blur, scanline gradient
     shift) — those are the expensive ones and stay off on touch/small screens.
     .orbit-ring / .orbit-ring2 (the spinning "planet" rings) only animate a
     `transform`, which the compositor handles almost for free, so they keep
     spinning on mobile instead of being frozen along with the heavy effects. */
  .grid-bg:before,.scanline,.ambient-orb,.login-card-glow,.badge-glow{animation:none!important}
  .grid-bg:before{filter:blur(14px)}
  .login-card-glow{filter:blur(5px)}
  .badge-glow{filter:blur(4px)}
  .orbit-ring,.orbit-ring2{will-change:transform}
}
</style>
<style>
.perm-grid,.bot-text-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}.perm-item{display:flex;align-items:center;gap:9px;padding:11px 12px;border:1px solid var(--line);background:var(--panel2);border-radius:13px;font-size:12px}.perm-item input{accent-color:var(--accent)}.bot-text-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.bot-text-grid textarea{width:100%;resize:vertical;min-height:90px;background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:12px;padding:11px;font:inherit;line-height:1.8}@media(max-width:700px){.perm-grid,.bot-text-grid{grid-template-columns:1fr}}
.tpl-studio-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;flex-wrap:wrap}
.tpl-badge{display:flex;align-items:center;gap:6px;padding:6px 11px;border-radius:99px;background:rgba(59,130,246,.12);color:#b79bff;border:1px solid rgba(59,130,246,.22);font-size:10.5px;font-weight:800;white-space:nowrap}
.tpl-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:14px;margin-top:14px}
.tpl-fields{display:flex;flex-direction:column;gap:8px}
.tpl-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 13px;border:1px solid var(--line);background:var(--panel2);border-radius:13px;cursor:pointer;transition:border-color .12s ease}
.tpl-row:hover{border-color:var(--line2)}
.tpl-row-main{display:flex;align-items:center;gap:10px;min-width:0}
.tpl-row-main i{width:32px;height:32px;flex-shrink:0;display:grid;place-items:center;border-radius:9px;background:rgba(59,130,246,.12);color:#a997ff;font-size:15px}
.tpl-row-main b{display:block;font-size:12px}
.tpl-row-main small{display:block;color:var(--sub2);font-size:9.5px;margin-top:2px}
input.tpl-switch{appearance:none;-webkit-appearance:none;width:36px;height:20px;border-radius:99px;background:var(--line2);border:1px solid var(--line);position:relative;cursor:pointer;flex-shrink:0;margin:0;transition:background-color .16s ease}
input.tpl-switch:after{content:'';position:absolute;width:14px;height:14px;top:2px;right:2px;border-radius:50%;background:#fff;transition:right .16s ease;box-shadow:0 1px 3px rgba(0,0,0,.3)}
input.tpl-switch:checked{background:linear-gradient(90deg,var(--accent),var(--accent-d));border-color:transparent}
input.tpl-switch:checked:after{right:18px}
.tpl-preview{padding:14px;border:1px dashed var(--line2);border-radius:14px;background:linear-gradient(155deg,rgba(59,130,246,.06),rgba(255,255,255,.015))}
.tpl-preview-label{display:flex;align-items:center;gap:7px;font-size:10.5px;color:var(--sub);font-weight:700;margin-bottom:10px}
.tpl-preview-row{display:flex;align-items:center;gap:9px;padding:11px 12px;border-radius:12px;background:var(--panel);border:1px solid var(--line)}
.tpl-preview-dot{width:9px;height:9px;border-radius:50%;background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18);flex-shrink:0}
.tpl-preview-text{flex:1;min-width:0;font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;direction:ltr;text-align:left}
.tpl-preview-proto{font-size:9px;font-weight:800;color:var(--accent);background:rgba(59,130,246,.12);padding:3px 8px;border-radius:99px;flex-shrink:0}
@media(max-width:760px){.tpl-grid{grid-template-columns:1fr}}
.admin-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.admin-card{position:relative;overflow:hidden;padding:18px;border:1px solid var(--line);background:linear-gradient(155deg,var(--panel) 0%,var(--panel2) 100%);border-radius:18px;box-shadow:var(--shadow-sm);transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.admin-card:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);border-color:var(--line2)}
.admin-card.is-owner{border-color:rgba(245,165,36,.35);background:linear-gradient(155deg,rgba(245,165,36,.08) 0%,var(--panel2) 60%)}
.admin-card.is-inactive{opacity:.62}
.admin-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.admin-id{display:flex;align-items:center;gap:11px;min-width:0}
.admin-avatar{flex:none;width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;color:#fff;background:linear-gradient(135deg,var(--accent),var(--accent-d));box-shadow:0 6px 16px rgba(59,130,246,.28)}
.admin-card.is-owner .admin-avatar{background:linear-gradient(135deg,#f5a524,#c9820a);box-shadow:0 6px 16px rgba(245,165,36,.3)}
.admin-meta{min-width:0}
.admin-meta .admin-name{font-size:14px;font-weight:800;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.admin-meta .admin-sub{display:flex;align-items:center;gap:6px;margin-top:3px;font-size:11px;color:var(--sub)}
.admin-role-badge{flex:none;display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.02em}
.admin-role-badge.owner{color:#f5a524;background:rgba(245,165,36,.14);border:1px solid rgba(245,165,36,.3)}
.admin-role-badge.admin{color:var(--accent);background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.28)}
.admin-status-dot{width:7px;height:7px;border-radius:50%;background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.15)}
.admin-card.is-inactive .admin-status-dot{background:var(--bad);box-shadow:0 0 0 3px rgba(242,73,85,.15)}
.admin-perm-row{display:flex;flex-wrap:wrap;gap:5px;margin-top:14px}
.admin-perm-chip{font-size:10px;padding:3px 8px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);color:var(--sub)}
.admin-perm-chip.all{color:#f5a524;border-color:rgba(245,165,36,.3);background:rgba(245,165,36,.1)}
.admin-card-foot{display:flex;align-items:center;justify-content:space-between;margin-top:16px;padding-top:12px;border-top:1px dashed var(--line)}
.admin-card-foot .admin-login{font-size:10.5px;color:var(--sub2)}
.admin-card-foot .row-actions{gap:6px}
.admins-hero{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:center;margin-bottom:14px;padding:20px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(135deg,rgba(59,130,246,.11),rgba(57,214,255,.035));box-shadow:var(--shadow-sm)}.admins-hero h2{font-size:18px;margin:0 0 5px}.admins-hero p{font-size:10px;color:var(--sub);margin:0;line-height:1.9}.admins-summary{display:flex;gap:8px;flex-wrap:wrap}.admins-summary .sum{min-width:92px;padding:11px 13px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.025);text-align:center}.admins-summary b{display:block;font-size:18px}.admins-summary small{display:block;color:var(--sub2);font-size:8px;margin-top:3px}.admin-card{min-height:188px;display:flex;flex-direction:column}.admin-card-top{padding-bottom:13px;border-bottom:1px dashed var(--line)}.admin-id{flex:1}.admin-avatar{position:relative;overflow:hidden}.admin-avatar:after{content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent 35%,rgba(255,255,255,.18) 50%,transparent 65%);transform:translateX(-130%);transition:transform .55s ease}.admin-card:hover .admin-avatar:after{transform:translateX(130%)}.admin-perm-row{min-height:45px;align-content:flex-start}.admin-perm-chip{transition:.15s ease}.admin-perm-chip:hover{border-color:var(--line2);color:var(--text)}.admin-card-foot{margin-top:auto}.admin-login{direction:ltr;text-align:left}.admin-actions-label{display:none}.admin-card-foot .row-actions{gap:8px}.admin-card-foot .iconbtn{width:38px;height:34px;border-radius:11px;font-size:15px;background:linear-gradient(145deg,var(--panel2),rgba(59,130,246,.08));border-color:var(--line2);box-shadow:0 7px 18px rgba(0,0,0,.10)}.admin-card-foot .iconbtn.danger{color:var(--bad)}.admin-card-foot .iconbtn.power{color:var(--accent)}.admin-card-foot .iconbtn:hover{transform:translateY(-1px);box-shadow:0 10px 24px rgba(59,130,246,.18)}.access-command-copy{min-width:0}.command-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;border:1px solid rgba(59,130,246,.28);background:rgba(59,130,246,.10);color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.08em}.access-command-copy h2{font-size:22px;margin:12px 0 7px;letter-spacing:-.02em}.access-command-copy p{max-width:760px}.command-points{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}.command-points span{display:inline-flex;align-items:center;gap:5px;padding:6px 9px;border:1px solid var(--line);border-radius:9px;background:rgba(255,255,255,.025);font-size:9px;color:var(--sub)}.command-points i{color:var(--good)}.admin-directory{overflow:hidden}.directory-live{display:inline-flex;align-items:center;gap:6px;font-size:9px;color:var(--good);font-weight:800}.directory-live i{width:6px;height:6px;border-radius:50%;background:var(--good);box-shadow:0 0 0 4px rgba(34,197,139,.12)}.admin-directory .panel-head{border-bottom:1px solid var(--line)}@media(max-width:700px){.access-command-copy h2{font-size:18px}.command-points{display:grid;grid-template-columns:1fr}}.admin-login-block{display:flex;flex-direction:column;gap:4px}.admin-login-label{font-size:8px;color:var(--sub2)}.admin-card{position:relative;overflow:hidden}.admin-card:before{content:"";position:absolute;inset:0 0 auto 0;height:2px;background:linear-gradient(90deg,var(--accent),transparent);opacity:.7}.admin-card.is-owner:before{background:linear-gradient(90deg,#f5a524,transparent)}.feature-lock{text-align:center;padding:16px 6px 8px}.feature-lock-icon{width:68px;height:68px;margin:0 auto 14px;display:grid;place-items:center;border-radius:20px;background:linear-gradient(145deg,rgba(59,130,246,.18),rgba(53,214,255,.08));border:1px solid rgba(59,130,246,.28);font-size:28px;color:var(--accent)}.feature-lock h3{margin:0 0 8px;font-size:18px}.feature-lock p{margin:0 auto;max-width:520px;line-height:2;color:var(--sub);font-size:11px}.feature-lock-note{display:inline-flex;gap:7px;align-items:center;margin-top:16px;padding:8px 11px;border-radius:999px;border:1px solid var(--line);background:var(--panel2);font-size:9px;color:var(--sub2)}@media(max-width:700px){.admins-hero{grid-template-columns:1fr}.admins-summary{justify-content:flex-start}}
.areq-row{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 14px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.02);margin-bottom:10px}
.areq-row:last-child{margin-bottom:0}
.areq-info{display:flex;flex-direction:column;gap:3px;min-width:0}
.areq-name{font-weight:800;font-size:12.5px}
.areq-meta{font-size:10px;color:var(--sub2);display:flex;gap:10px;flex-wrap:wrap}
.areq-meta span{display:inline-flex;align-items:center;gap:4px}
.areq-note{font-size:10.5px;color:var(--sub);margin-top:2px}
.areq-actions{display:flex;gap:8px;flex-shrink:0}
.areq-empty{text-align:center;padding:22px 10px;color:var(--sub2);font-size:11px}
.areq-status{font-size:9px;font-weight:800;padding:4px 9px;border-radius:999px}
.areq-status.approved{background:rgba(34,197,94,.10);color:#7cf0a8;border:1px solid rgba(34,197,94,.25)}
.areq-status.rejected{background:rgba(239,68,68,.10);color:#ff9b9b;border:1px solid rgba(239,68,68,.25)}
@media(max-width:700px){.admin-grid{grid-template-columns:1fr}}
</style></head>
<body>
<div class="grid-bg"></div><div class="scanline"></div><div class="ambient-orb a"></div><div class="ambient-orb b"></div>
<div class="dot" style="top:14%;left:20%"></div>
<div class="dot" style="top:22%;left:78%;animation-delay:-1s"></div>
<div class="dot" style="top:62%;left:10%;animation-delay:-2s"></div>
<div class="dot" style="top:70%;left:88%;animation-delay:-1.6s"></div>
<div class="dot" style="top:40%;left:6%;animation-delay:-2.4s"></div>
<div class="dot" style="top:85%;left:45%;animation-delay:-.6s"></div>

<div class="lang-switch">
  <button id="langFa" class="on" onclick="setLang('fa')">فارسی</button>
  <button id="langEn" onclick="setLang('en')">EN</button>
</div>

<div class="wrap">
  <div class="badge-wrap">
    <div class="orbit-ring2"></div>
    <div class="orbit-ring"><span class="planet"></span><span class="planet2"></span></div>
    <div class="badge-glow"></div>
    <div class="badge"><img src="data:image/png;base64,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" alt="logo"></div>
  </div>
  <div class="brand-caps">FAULTPASS</div>
  <h1 data-i18n="h1"></h1>
  <p class="subtitle" data-i18n="subtitle"></p>

  <div class="login-status"><span class="live"></span><span>FAULTPASS · SECURE ADMIN CONSOLE</span><span style="margin-right:auto;color:#6ee7b7">ONLINE</span></div>
  <div class="card">
    <div class="login-card-glow"></div>
    <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:18px"><div><div style="font-size:10px;letter-spacing:.16em;color:#8fa1c0;font-weight:800">SECURE ADMIN</div><div style="font-size:16px;font-weight:900;margin-top:4px">ورود به مرکز کنترل</div></div><div style="width:38px;height:38px;border-radius:12px;display:grid;place-items:center;border:1px solid rgba(143,217,255,.18);background:rgba(62,166,255,.08);color:#8fd9ff;box-shadow:0 0 25px rgba(62,166,255,.12)"><i class="ti ti-shield-lock" style="font-size:18px"></i></div></div>
    <form method="post" action="/login" id="loginForm">
      <div class="field">
        <label data-i18n="emailLabel"></label>
        <div class="inp">
          <input type="text" name="username" id="username" data-i18n-placeholder="emailPh" autocomplete="username">
          <i class="ti ti-user-shield i-lead"></i>
        </div>
      </div>
      <div class="field">
        <label data-i18n="passLabel"></label>
        <div class="inp">
          <input type="password" name="password" id="password" placeholder="••••••••" autocomplete="current-password" required>
          <i class="ti ti-lock i-lead"></i>
          <button type="button" class="toggle-eye" onclick="togglePw()" id="pwToggle" tabindex="-1"><i class="ti ti-eye"></i></button>
        </div>
        <div id="capsWarn" style="display:none;align-items:center;gap:5px;margin-top:7px;font-size:11px;color:#fbbf24"><i class="ti ti-alert-triangle"></i> Caps Lock فعال است</div>
      </div>
      <label class="remember"><input type="checkbox" name="remember" value="1"><span data-i18n="remember"></span></label>
      <button class="btn-main" type="submit" id="submitBtn"><i class="ti ti-login-2"></i><span data-i18n="submit"></span></button>
    </form>
    <div class="security-strip"><span><i class="ti ti-shield-check"></i>Protected Session</span><span><i class="ti ti-lock"></i>Secure Cookie</span><span><i class="ti ti-activity"></i>System Monitor</span></div>
  </div>
  <div class="foot">FaultPass Control Center &copy; <span data-i18n="rights"></span></div>
</div>

<div class="areg-overlay" id="aregOverlay" onclick="if(event.target===this)closeAdminReg()">
  <div class="areg-box">
    <div class="areg-head">
      <div>
        <div class="areg-badge"><i class="ti ti-user-shield"></i><span data-i18n="adminRegBadge"></span></div>
        <h3 data-i18n="adminRegTitle"></h3>
        <p data-i18n="adminRegDesc"></p>
      </div>
      <button type="button" class="areg-close" onclick="closeAdminReg()"><i class="ti ti-x"></i></button>
    </div>
    <div class="field">
      <label data-i18n="adminRegNameLabel"></label>
      <div class="inp"><input type="text" id="aregName" data-i18n-placeholder="adminRegNamePh"><i class="ti ti-id i-lead"></i></div>
    </div>
    <div class="field">
      <label data-i18n="adminRegTgLabel"></label>
      <div class="inp"><input type="text" id="aregTg" dir="ltr" data-i18n-placeholder="adminRegTgPh"><i class="ti ti-brand-telegram i-lead"></i></div>
    </div>
    <div class="field">
      <label data-i18n="adminRegNoteLabel"></label>
      <div class="inp"><input type="text" id="aregNote" data-i18n-placeholder="adminRegNotePh"><i class="ti ti-message i-lead"></i></div>
    </div>
    <div id="aregMsg" class="areg-msg" style="display:none"></div>
    <button class="btn-main" type="button" id="aregSubmitBtn" onclick="submitAdminReg()"><i class="ti ti-send"></i><span data-i18n="adminRegSubmit"></span></button>
    <p class="areg-hint" data-i18n="adminRegHint"></p>
  </div>
</div>

<script>
var I18N = {
  fa: {
    title: "ورود | FaultPass",
    h1: 'ورود به <span class="g">FaultPass</span>',
    subtitle: "مرکز کنترل امن FaultPass برای مدیریت سرویس‌ها و شبکه",
    emailLabel: "نام کاربری",
    emailPh: "admin",
    passLabel: "رمز عبور",
    remember: "مرا به خاطر بسپار",
    submit: "ورود به پنل",
    rights: "همه‌ی حقوق محفوظ است",
    adminRegBtn: "ثبت‌نام ادمینی",
    adminRegBadge: "درخواست همکاری",
    adminRegTitle: "ثبت‌نام ادمینی FaultPass",
    adminRegDesc: "اطلاعاتت رو بفرست، مالک پنل درخواستت رو بررسی می‌کنه و اگر تایید بشه، نام کاربری و رمز از طریق تلگرام برات ارسال می‌شه.",
    adminRegNameLabel: "نام و نام خانوادگی",
    adminRegNamePh: "مثلاً: علی رضایی",
    adminRegTgLabel: "آیدی تلگرام",
    adminRegTgPh: "@username",
    adminRegNoteLabel: "توضیح (اختیاری)",
    adminRegNotePh: "چرا می‌خوای ادمین بشی؟",
    adminRegSubmit: "ارسال درخواست",
    adminRegHint: "پس از تایید مالک، اطلاعات ورود از طریق آیدی تلگرامی که وارد کردی برایت ارسال خواهد شد.",
    adminRegSent: "درخواست شما ثبت شد ✓ منتظر تایید مالک پنل بمانید.",
    adminRegNameErr: "نام و نام خانوادگی را کامل وارد کنید",
    adminRegTgErr: "آیدی تلگرام معتبر وارد کنید"
  },
  en: {
    title: "Login | FaultPass",
    h1: 'Sign in to <span class="g">FaultPass</span>',
    subtitle: "Secure FaultPass control center for services and network",
    emailLabel: "Username",
    emailPh: "admin",
    passLabel: "Password",
    remember: "Remember me",
    submit: "Sign in",
    rights: "All rights reserved",
    adminRegBtn: "Register as admin",
    adminRegBadge: "Collaboration request",
    adminRegTitle: "FaultPass admin registration",
    adminRegDesc: "Send your details. The panel owner will review your request and, if approved, send you a username and password via Telegram.",
    adminRegNameLabel: "Full name",
    adminRegNamePh: "e.g. John Smith",
    adminRegTgLabel: "Telegram ID",
    adminRegTgPh: "@username",
    adminRegNoteLabel: "Note (optional)",
    adminRegNotePh: "Why do you want to be an admin?",
    adminRegSubmit: "Send request",
    adminRegHint: "Once approved by the owner, your login details will be sent to the Telegram ID you provided.",
    adminRegSent: "Your request was submitted ✓ wait for the owner's approval.",
    adminRegNameErr: "Please enter your full name",
    adminRegTgErr: "Please enter a valid Telegram ID"
  }
};
function applyLang(lang){
  var d = I18N[lang];
  document.querySelectorAll('[data-i18n]').forEach(function(el){
    var k = el.getAttribute('data-i18n');
    if(d[k] !== undefined) el.innerHTML = d[k];
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el){
    var k = el.getAttribute('data-i18n-placeholder');
    if(d[k] !== undefined) el.setAttribute('placeholder', d[k]);
  });
  document.title = d.title;
  var html = document.getElementById('htmlRoot');
  html.setAttribute('lang', lang);
  html.setAttribute('dir', lang === 'fa' ? 'rtl' : 'ltr');
  html.setAttribute('data-lang', lang);
  document.getElementById('langFa').classList.toggle('on', lang==='fa');
  document.getElementById('langEn').classList.toggle('on', lang==='en');
}
function setLang(lang){
  try{ localStorage.setItem('vw_lang', lang); }catch(e){}
  applyLang(lang);
}
(function(){
  var saved = 'fa';
  try{ saved = localStorage.getItem('vw_lang') || 'fa'; }catch(e){}
  applyLang(saved);
})();
function togglePw(){
  var inp = document.getElementById('password');
  var icon = document.getElementById('pwToggle').querySelector('i');
  if(inp.type === 'password'){ inp.type = 'text'; icon.className = 'ti ti-eye-off'; }
  else { inp.type = 'password'; icon.className = 'ti ti-eye'; }
}
(function(){
  var pwInput = document.getElementById('password');
  var warn = document.getElementById('capsWarn');
  if(!pwInput || !warn) return;
  function checkCaps(e){
    var isCaps = typeof e.getModifierState === 'function' && e.getModifierState('CapsLock');
    warn.style.display = isCaps ? 'flex' : 'none';
  }
  pwInput.addEventListener('keyup', checkCaps);
  pwInput.addEventListener('keydown', checkCaps);
})();
document.getElementById('loginForm').addEventListener('submit', function(){
  var btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = '<i class="ti ti-loader-2 spin"></i>';
});
function curLang(){ try{ return localStorage.getItem('vw_lang') || 'fa'; }catch(e){ return 'fa'; } }
function openAdminReg(){
  document.getElementById('aregMsg').style.display = 'none';
  document.getElementById('aregOverlay').classList.add('show');
}
function closeAdminReg(){
  document.getElementById('aregOverlay').classList.remove('show');
}
function aregShowMsg(text, ok){
  var el = document.getElementById('aregMsg');
  el.textContent = text;
  el.className = 'areg-msg ' + (ok ? 'ok' : 'err');
  el.style.display = 'block';
}
async function submitAdminReg(){
  var d = I18N[curLang()];
  var name = document.getElementById('aregName').value.trim();
  var tg = document.getElementById('aregTg').value.trim().replace(/^@/, '');
  var note = document.getElementById('aregNote').value.trim();
  if(name.length < 3){ aregShowMsg(d.adminRegNameErr, false); return; }
  if(tg.length < 3){ aregShowMsg(d.adminRegTgErr, false); return; }
  var btn = document.getElementById('aregSubmitBtn');
  btn.disabled = true;
  var originalHtml = btn.innerHTML;
  btn.innerHTML = '<i class="ti ti-loader-2 spin"></i>';
  try{
    var res = await fetch('/api/admin-requests', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({full_name: name, telegram_id: tg, note: note})
    });
    var data = {};
    try{ data = await res.json(); }catch(e){}
    if(!res.ok) throw new Error(data.detail || 'خطا');
    aregShowMsg(d.adminRegSent, true);
    document.getElementById('aregName').value = '';
    document.getElementById('aregTg').value = '';
    document.getElementById('aregNote').value = '';
  }catch(e){
    aregShowMsg(e.message || 'خطا', false);
  }finally{
    btn.disabled = false;
    btn.innerHTML = originalHtml;
  }
}
</script>
</body>
</html>
"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FaultPass Control Center</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&family=Estedad:wght@400;500;600;700;800;900&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700;800&family=Shabnam:wght@400;500;700&family=Yekan+Bakh:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:var(--font-ui,'Vazirmatn'),sans-serif}
:root{
  --bg:#0b0e14;--panel:#111623;--panel2:#161c2b;--line:#212838;--line2:#2a3348;
  --accent:#3b82f6;--accent-d:#2563eb;--good:#22c58b;--warn:#f5a524;--bad:#f24955;
  --text:#e7ebf3;--sub:#8792a8;--sub2:#5b6478;
  --shadow-sm:0 2px 8px rgba(0,0,0,.18);--shadow-md:0 10px 28px rgba(0,0,0,.28);
}
[data-theme="light"]{
  --bg:#ffffff;--panel:#ffffff;--panel2:#f7f8fb;--line:#e5e7eb;--line2:#d1d5db;
  --accent:#1d4ed8;--accent-d:#1d4ed8;--good:#17a673;--warn:#c9820a;--bad:#e0324a;
  --text:#191c2b;--sub:#666f8a;--sub2:#98a1b8;
  --shadow-sm:0 2px 8px rgba(30,34,60,.05);--shadow-md:0 14px 32px rgba(30,34,60,.08);
}
html{transition:background-color .2s ease}
html,body{background:var(--bg);color:var(--text);height:100%}
html{scrollbar-gutter:stable;overflow-anchor:none}
.body-wrap{overflow-anchor:none}
@media (prefers-reduced-motion: no-preference){
  /* Keep the original look, but avoid expensive perpetual compositor work. */
}
@media (max-width:1100px){
  *{scroll-behavior:auto!important}
}

/* Performance: never animate the entire DOM. Only interactive controls transition. */
button,.btn,.tab,.nav-btn,.icon-btn,input,select,textarea,.card,.drawer,.toast{
  transition:background-color .14s ease,border-color .14s ease,color .14s ease,box-shadow .14s ease;
}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:8px}

/* ===== Shell ===== */
#app{display:flex;height:100vh;position:relative}

/* ============ SIDEBAR ============ */
.sidebar{
  width:252px;flex-shrink:0;height:100vh;display:flex;flex-direction:column;
  background:var(--panel);border-left:1px solid var(--line);position:relative;z-index:30;
  transition:transform .22s ease;
}
.sidebar-brand{display:flex;align-items:center;gap:10px;padding:20px 18px;border-bottom:1px solid var(--line)}
.sidebar-brand img{width:34px;height:34px;border-radius:9px;box-shadow:0 4px 14px rgba(59,130,246,.35)}
.sidebar-brand div{font-weight:800;font-size:14.5px}
.sidebar-brand small{display:block;font-weight:400;font-size:10.5px;color:var(--sub)}
.tabnav{flex:1;display:flex;flex-direction:column;gap:2px;padding:14px 12px;overflow-y:auto}
.tab{
  padding:10px 13px;border-radius:10px;font-size:13px;font-weight:600;color:var(--sub);
  display:flex;align-items:center;gap:10px;white-space:nowrap;transition:.14s;
  border:1px solid transparent;position:relative;
}
.tab i{font-size:17px;width:18px;text-align:center;flex-shrink:0}
.tab:hover{color:var(--text);background:rgba(255,255,255,.04)}
.tab.on{color:#fff;background:linear-gradient(90deg,var(--accent),#2563eb);box-shadow:0 6px 18px -4px rgba(59,130,246,.55)}
.tab .bd{background:rgba(255,255,255,.16);border-radius:100px;font-size:10px;padding:1px 7px;margin-right:auto}
.tab.on .bd{background:rgba(255,255,255,.28)}
.sidebar-foot{padding:14px 16px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:10px}
.lang-mini{display:flex;background:var(--panel2);border:1px solid var(--line);border-radius:100px;padding:3px;gap:2px}
.lang-mini button{flex:1;padding:6px 10px;border:0;background:transparent;color:var(--sub);font-size:11px;font-weight:700;border-radius:100px;cursor:pointer}
.lang-mini button.on{background:linear-gradient(90deg,var(--accent-d),var(--accent));color:#fff}

/* ============ TOP BAR (slim) ============ */
.main-col{flex:1;min-width:0;display:flex;flex-direction:column;height:100vh;position:relative}
.topbar{
  height:60px;flex-shrink:0;display:flex;align-items:center;gap:16px;padding:0 22px;
  background:var(--panel);border-bottom:1px solid var(--line);position:relative;z-index:20;
}
.hamburger{display:none;width:34px;height:34px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);align-items:center;justify-content:center;color:var(--sub);font-size:17px}
.page-title{font-weight:800;font-size:14.5px;color:var(--text)}
.page-title span{display:block;font-weight:400;font-size:11px;color:var(--sub);margin-top:1px}
.top-right{display:flex;align-items:center;gap:10px;flex-shrink:0;margin-right:auto}
.user-chip{display:flex;align-items:center;gap:9px;background:var(--panel2);border:1px solid var(--line);padding:6px 12px 6px 8px;border-radius:100px;font-size:12.5px;cursor:pointer}
.user-chip .av{width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#3ea6ff);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:12px;color:#fff}
.icon-btn{width:36px;height:36px;border-radius:9px;background:var(--panel2);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;color:var(--sub);font-size:16px}
.icon-btn:hover{color:var(--text);border-color:var(--line2)}
.sidebar-overlay{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:29;display:none}
.wide-sidebar .sidebar{width:292px}
.wide-sidebar .main-col{min-width:0}
@media(max-width:980px){
  .hamburger{display:flex}
  .sidebar{position:fixed;top:0;right:0;transform:translateX(105%)}
  #app.sb-open .sidebar{transform:translateX(0)}
  #app.sb-open .sidebar-overlay{display:block}
}

.body-wrap{flex:1;overflow:auto;padding:22px 26px 70px}
.page{display:none;max-width:1320px;margin:0 auto}
.page.on{display:block;animation:fade .18s ease}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{display:inline-block;animation:spin .7s linear infinite}
.no-motion .spin{animation:none}

.pg-head{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;margin-bottom:20px;flex-wrap:wrap}
.pg-head h1{font-size:19px;font-weight:800}
.pg-head p{font-size:12.5px;color:var(--sub);margin-top:3px}
.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.search{position:relative}
.search input{width:230px;padding:9px 34px 9px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.search input:focus{border-color:var(--accent)}
.search i{position:absolute;right:11px;top:50%;transform:translateY(-50%);color:var(--sub2);font-size:15px}
select.sel{padding:9px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.btn{padding:9px 16px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;font-weight:600;display:inline-flex;align-items:center;gap:7px}
.btn:hover{border-color:var(--line2)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-d)}
.btn.danger{color:var(--bad);border-color:rgba(242,73,85,.3)}
.btn.danger:hover{background:rgba(242,73,85,.08)}
.btn.sm{padding:6px 11px;font-size:12px}
.btn:disabled{opacity:.5;cursor:not-allowed}

/* stat cards */
.stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:22px}
.stat-card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.stat-card .sc-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.stat-card .sc-icon{width:34px;height:34px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px}
.stat-card .sc-val{font-size:22px;font-weight:800}
.stat-card .sc-label{font-size:11.5px;color:var(--sub);margin-top:2px}

/* table */
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden}
table{width:100%;border-collapse:collapse;font-size:13px}
thead th{text-align:right;padding:12px 14px;background:var(--panel2);color:var(--sub);font-weight:700;font-size:11.5px;border-bottom:1px solid var(--line)}
tbody td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:middle}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:rgba(255,255,255,.015)}
.mono{font-family:ui-monospace,Consolas,monospace;direction:ltr;text-align:left;font-size:12px;color:var(--sub)}
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:100px;font-size:11px;font-weight:700}
.badge.green{background:rgba(34,197,139,.14);color:var(--good)}
.badge.red{background:rgba(242,73,85,.14);color:var(--bad)}
.badge.gray{background:rgba(135,146,168,.14);color:var(--sub)}
.badge.orange{background:rgba(245,165,36,.14);color:var(--warn)}
.row-actions{display:flex;gap:6px;justify-content:flex-end}
.iconbtn{width:29px;height:29px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;color:var(--sub);font-size:14px}
.iconbtn:hover{color:var(--text);border-color:var(--line2)}
.empty{padding:50px 20px;text-align:center;color:var(--sub2)}
.empty i{font-size:30px;display:block;margin-bottom:10px}
.bar-mini{width:70px;height:6px;background:var(--line2);border-radius:99px;overflow:hidden;display:inline-block;vertical-align:middle;margin-left:6px}
.bar-mini i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--good))}


/* ===== Appearance Studio ===== */
.appearance-studio{display:grid;grid-template-columns:1.25fr .75fr;gap:14px;margin-bottom:18px}.appearance-card{padding:18px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(145deg,rgba(59,130,246,.07),rgba(255,255,255,.018));overflow:hidden}.appearance-card h3{font-size:14px;margin-bottom:4px}.appearance-card p{font-size:10.5px;color:var(--sub);line-height:1.8}.appearance-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}.appearance-field{padding:11px;border:1px solid var(--line);border-radius:12px;background:var(--panel2)}.appearance-field label{display:block;color:var(--sub);font-size:10px;margin-bottom:7px}.appearance-field select{width:100%;padding:9px 10px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--text);outline:none}.theme-pills,.accent-pills{display:flex;gap:7px;flex-wrap:wrap}.theme-pill,.accent-pill{border:1px solid var(--line);background:var(--panel);color:var(--sub);border-radius:9px;padding:8px 11px;font-size:10px;cursor:pointer}.theme-pill.on,.accent-pill.on{color:#fff;border-color:var(--accent);background:rgba(59,130,246,.14)}.accent-pill{display:flex;align-items:center;gap:6px}.accent-dot{width:10px;height:10px;border-radius:50%;display:inline-block}.appearance-preview{min-height:100%;position:relative;display:flex;align-items:center;justify-content:center}.preview-window{width:100%;max-width:330px;border:1px solid var(--line);border-radius:15px;background:var(--panel);overflow:hidden;box-shadow:0 25px 60px rgba(0,0,0,.22)}.preview-top{height:36px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:6px;padding:0 10px}.preview-top i{font-size:10px;color:var(--sub)}.preview-main{display:grid;grid-template-columns:82px 1fr;min-height:140px}.preview-side{padding:10px;border-left:1px solid var(--line);background:var(--panel2)}.preview-side div{height:22px;border-radius:6px;margin-bottom:6px;background:rgba(255,255,255,.04)}.preview-side div.active{background:linear-gradient(90deg,var(--accent),var(--accent-d))}.preview-content{padding:12px}.preview-content .pv-title{font-size:12px;font-weight:800}.preview-content .pv-sub{font-size:8px;color:var(--sub);margin-top:3px}.pv-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:14px}.pv-cards span{height:45px;border-radius:9px;border:1px solid var(--line);background:rgba(255,255,255,.02)}.appearance-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:13px}.appearance-toggle{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 11px;border:1px solid var(--line);border-radius:11px;background:var(--panel2);font-size:10.5px;color:var(--sub)}.switch{width:38px;height:21px;border-radius:99px;background:var(--line2);position:relative;cursor:pointer;border:0}.switch:after{content:'';position:absolute;width:15px;height:15px;top:2px;right:2px;border-radius:50%;background:#fff;transition:.16s}.switch.on{background:var(--accent)}.switch.on:after{right:21px}.density-compact .tab{padding-top:8px;padding-bottom:8px}.density-compact .body-wrap{padding-top:16px;padding-bottom:45px}.density-compact .card{border-radius:12px}.no-motion *, .no-motion *:before, .no-motion *:after{transition:none!important;animation:none!important;scroll-behavior:auto!important}
@media(max-width:900px){.appearance-studio{grid-template-columns:1fr}}@media(max-width:600px){.appearance-grid{grid-template-columns:1fr}.preview-window{max-width:none}}

.advanced-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:14px}.pro-action{border:1px solid var(--line);background:linear-gradient(145deg,var(--panel2),rgba(59,130,246,.05));color:var(--text);border-radius:14px;padding:15px;text-align:right;cursor:pointer;box-shadow:var(--ui-glow);}.pro-action i{font-size:20px;color:var(--accent);display:block;margin-bottom:10px}.pro-action b{display:block;font-size:11px}.pro-action small{display:block;color:var(--sub);font-size:9px;margin-top:4px}.accent-pills{max-height:92px;overflow:auto}.radius-sharp .card,.radius-sharp .appearance-card,.radius-sharp .appearance-field,.radius-sharp .btn,.radius-sharp .tab,.radius-sharp .search input{border-radius:6px}.radius-pill .card,.radius-pill .appearance-card,.radius-pill .appearance-field{border-radius:24px}.radius-pill .btn,.radius-pill .tab,.radius-pill .search input{border-radius:999px}.font-small{font-size:92%}.font-large{font-size:108%}.appearance-card,.card,.pro-action{box-shadow:var(--ui-glow)}
@media(max-width:900px){.advanced-grid{grid-template-columns:1fr 1fr}}@media(max-width:600px){.advanced-grid{grid-template-columns:1fr}}

.ib-quickstats{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 14px}.ib-quickstats>div{position:relative;overflow:hidden;display:flex;align-items:center;gap:10px;padding:12px 15px;border:1px solid var(--line);background:linear-gradient(155deg,rgba(255,255,255,.03),rgba(255,255,255,.01));border-radius:14px;flex:1;min-width:150px;transition:transform .15s ease,border-color .15s ease}.ib-quickstats>div:hover{transform:translateY(-2px);border-color:var(--line2)}.ib-quickstats i{width:32px;height:32px;display:grid;place-items:center;border-radius:9px;background:rgba(59,130,246,.12);color:#a997ff;font-size:15px;flex-shrink:0}.ib-quickstats b{display:block;font-size:17px;line-height:1.2}.ib-quickstats small{display:block;color:var(--sub2);font-size:9.5px;margin-top:2px}
/* ===== Inbound cards (grid) ===== */
.ib-listbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 12px;flex-wrap:wrap}
.ib-selectall{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--sub);cursor:pointer;user-select:none}
.ib-selectall input{width:15px;height:15px;accent-color:var(--accent);cursor:pointer}
.ib-count{font-size:11px;color:var(--sub2)}
.ib-bulkbar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 16px;background:linear-gradient(90deg,rgba(59,130,246,.12),rgba(59,130,246,.04));border:1px solid rgba(59,130,246,.28);border-radius:13px;font-size:11.5px;color:var(--sub);flex-wrap:wrap;margin-bottom:12px}
.ib-bulkbar b{color:var(--text)}.ib-bulkactions{display:flex;gap:6px}
.ib-check{width:15px;height:15px;accent-color:var(--accent);cursor:pointer}

.ib-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(328px,1fr));gap:14px}
.ib-card{position:relative;display:flex;flex-direction:column;gap:13px;padding:16px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(165deg,rgba(255,255,255,.035),rgba(255,255,255,.012));box-shadow:var(--shadow-sm);overflow:hidden;transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease}
.ib-card:before{content:'';position:absolute;inset:0 0 auto 0;height:3px;background:linear-gradient(90deg,var(--accent),#39d6ff)}
.ib-card:hover{border-color:var(--line2);box-shadow:var(--shadow-md)}
.ib-card.ib-off{opacity:.58}
.ib-card.ib-off:before{background:var(--sub2)}
.ib-card.ib-off:hover{opacity:.85}
.ib-card.ib-selected{border-color:var(--accent);box-shadow:0 0 0 3px rgba(59,130,246,.14)}

.ib-card-head{display:flex;align-items:flex-start;gap:11px}
.ib-card-check{position:absolute;top:14px;left:14px;opacity:0;pointer-events:none;transition:opacity .15s ease}
.ib-card:hover .ib-card-check,.ib-card.ib-selected .ib-card-check{opacity:1;pointer-events:auto}
.ib-avatar{width:40px;height:40px;border-radius:12px;flex-shrink:0;display:grid;place-items:center;font-size:17px;background:rgba(59,130,246,.14);color:#b79bff;border:1px solid rgba(59,130,246,.22)}
.ib-card-id{flex:1;min-width:0;padding-left:20px}
.ib-card-id .ib-name-top{display:flex;align-items:center;gap:6px}
.ib-card-id b{font-size:13px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;display:block}
.ib-card-id .mono{font-size:9.5px;color:var(--sub2);margin-top:2px}
.ib-card-controls{display:flex;flex-direction:column;align-items:flex-end;gap:7px;flex-shrink:0}

.ib-tagrow{display:flex;flex-wrap:wrap;gap:5px}
.ib-tagrow span{padding:3px 8px;border-radius:7px;background:var(--panel2);border:1px solid var(--line);font-size:9.5px;font-weight:700;letter-spacing:.01em;color:var(--sub);white-space:nowrap;transition:border-color .12s ease}
.ib-card:hover .ib-tagrow span{border-color:var(--line2)}
.ib-live-tag{background:rgba(34,197,139,.14)!important;color:var(--good)!important;border-color:transparent!important;display:inline-flex!important;align-items:center;gap:4px}
.ib-live-tag i{width:5px;height:5px;border-radius:50%;background:var(--good);animation:ibLivePulse 1.6s ease-in-out infinite;flex-shrink:0}
@keyframes ibLivePulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.35);opacity:.6}}
.no-motion .ib-live-tag i{animation:none}
.ib-linkonly-tag{background:rgba(242,73,85,.12)!important;color:var(--bad)!important;border-color:transparent!important}

.ib-card-addr{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:8px 11px;border-radius:10px;background:var(--panel2);border:1px solid var(--line)}
.ib-card-addr span.mono{font-size:11px;color:var(--text)}
.ib-card-addr small{font-size:9px;color:var(--sub2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:110px}

.ib-card-traffic{display:flex;flex-direction:column;gap:6px}
.ib-card-traffic .ib-tf-top{display:flex;align-items:center;justify-content:space-between;font-size:9.5px;color:var(--sub2)}
.ib-card-traffic .ib-tf-top b{font-size:11.5px;color:var(--text);font-weight:800}
.ib-progress{height:6px;border-radius:99px;background:var(--line2);overflow:hidden;box-shadow:inset 0 0 0 1px var(--line)}
.ib-progress i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),#39d6ff);transition:width .3s ease}
.ib-progress i.warn{background:linear-gradient(90deg,#f5a524,#f59e0b)}
.ib-progress i.crit{background:linear-gradient(90deg,#f24955,#ef4444)}

.ib-card-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px}
.ib-card-stats>div{padding:8px 9px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);text-align:center}
.ib-card-stats small{display:block;color:var(--sub2);font-size:8.5px;margin-bottom:3px}
.ib-card-stats b{font-size:11px}
.ib-card-stats b.soon{color:var(--warn)}
.ib-card-stats b.expired{color:var(--bad)}

.ib-card-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:2px;border-top:1px dashed var(--line);padding-top:11px}
.ib-card-foot .ib-clientcell{display:flex;align-items:center;gap:7px;font-size:10.5px;color:var(--sub)}
.ib-card-foot .ib-clientcell .iconbtn{width:27px;height:27px;font-size:12px}
.ib-card-actions{display:flex;gap:5px}
.ib-card-actions .iconbtn{width:29px;height:29px;font-size:13px;border-radius:9px;transition:transform .12s ease,background-color .12s ease,color .12s ease}
.ib-card-actions .iconbtn:hover{transform:translateY(-1px);background:var(--panel2)}

.ib-switch{width:34px;height:19px;border-radius:99px;background:var(--line2);position:relative;cursor:pointer;border:0;flex-shrink:0;box-shadow:inset 0 0 0 1px var(--line)}
.ib-switch:after{content:'';position:absolute;width:13px;height:13px;top:3px;right:3px;border-radius:50%;background:#fff;transition:.16s}
.ib-switch.on{background:linear-gradient(90deg,var(--accent),#39d6ff);box-shadow:0 0 12px rgba(59,130,246,.35)}
.ib-switch.on:after{right:18px}
.ib-status-dot{width:8px;height:8px;border-radius:50%;background:#7688a9;flex-shrink:0}
.ib-status-dot.green{background:#22c58b;box-shadow:0 0 0 3px rgba(34,197,139,.18);animation:ibLivePulse 1.6s ease-in-out infinite}
.ib-status-dot.red{background:#f24955}
.no-motion .ib-status-dot{animation:none}
@media(max-width:560px){.ib-grid{grid-template-columns:1fr}}
.ov-quickstats>div{position:relative;overflow:hidden}
.ov-quickstats>div:nth-child(1) i{background:rgba(59,130,246,.14);color:#a997ff}
.ov-quickstats>div:nth-child(2) i{background:rgba(34,197,139,.14);color:#22c58b}
.ov-quickstats>div:nth-child(3) i{background:rgba(53,214,255,.14);color:#35d6ff}
.ov-quickstats>div:nth-child(4) i{background:rgba(245,165,36,.14);color:#f5a524}
.ov-toplinks{padding:14px 18px}
.ov-toplink-row{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--line)}
.ov-toplink-row:last-child{border-bottom:none}
.ov-toplink-row .otl-rank{width:20px;height:20px;border-radius:6px;background:var(--panel2);display:grid;place-items:center;font-size:10px;color:var(--sub2);flex-shrink:0}
.ov-toplink-row .otl-info{flex:1;min-width:0}
.ov-toplink-row .otl-info b{font-size:11.5px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ov-toplink-row .otl-bar{height:4px;border-radius:99px;background:var(--line2);margin-top:5px;overflow:hidden}
.ov-toplink-row .otl-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),#39d6ff);border-radius:99px}
.ov-toplink-row .otl-val{font-size:10px;color:var(--sub2);white-space:nowrap;flex-shrink:0}
.ov-empty{padding:20px;text-align:center;color:var(--sub2);font-size:11px}
@media(max-width:900px){.ib-quickstats{flex-direction:column}}

/* drawer */
.overlay{position:fixed;inset:0;background:rgba(4,6,10,.55);backdrop-filter:blur(2px);z-index:90;display:none}
.overlay.show{display:block}
.drawer{position:fixed;top:0;left:0;bottom:0;width:680px;max-width:92vw;background:var(--panel);border-left:1px solid var(--line);z-index:91;transform:translateX(-105%);transition:transform .22s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column}
.drawer.show{transform:translateX(0)}
.dr-head{padding:18px 20px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}
.dr-head h3{font-size:15px;font-weight:800}
.dr-body{flex:1;overflow:auto;padding:18px 20px}
.dr-foot{padding:16px 20px;border-top:1px solid var(--line);display:flex;gap:10px}
.grp{margin-bottom:16px}
.grp label{display:block;font-size:12px;font-weight:600;color:var(--sub);margin-bottom:6px}
.grp input,.grp select,.grp textarea{width:100%;padding:10px 12px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font-size:13px;outline:none}
.grp input:focus,.grp select:focus,.grp textarea:focus{border-color:var(--accent)}
.grp textarea{resize:vertical;min-height:64px;font-family:ui-monospace,monospace;direction:ltr;text-align:left}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.chk{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text)}
.hint{font-size:11px;color:var(--sub2);margin-top:5px;line-height:1.7}
.divider{height:1px;background:var(--line);margin:18px 0}
.inbound-builder{display:flex;flex-direction:column;gap:16px}
.ib-hero{padding:16px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(135deg,rgba(79,124,255,.10),rgba(59,130,246,.07));display:flex;align-items:center;justify-content:space-between;gap:12px}
.ib-hero .ib-title{display:flex;align-items:center;gap:12px}.ib-hero .ib-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:linear-gradient(135deg,var(--accent),#6d5dfc);color:#fff;font-size:20px;box-shadow:0 10px 24px rgba(79,124,255,.22)}
.ib-hero b{display:block;font-size:14px}.ib-hero small{display:block;color:var(--sub);font-size:11px;margin-top:3px}
.ib-section{border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.018);overflow:hidden}.ib-section-head{padding:12px 14px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between}.ib-section-head b{font-size:12.5px}.ib-section-head small{font-size:10.5px;color:var(--sub2)}
.ib-section-body{padding:14px}.ib-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.ib-grid.three{grid-template-columns:1fr 1fr 1fr}.ib-full{grid-column:1/-1}
.ib-choice{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
/* Professional inbound protocol/transport matrix — renamed to .ib-opt (was
   accidentally reusing the .ib-card class name used by the main inbound
   dashboard cards above; that collision was overriding the dashboard card
   layout with these small radio-tile rules). */
.ib-matrix{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px}
.ib-opt{position:relative;display:flex;align-items:center;gap:10px;padding:12px;border:1px solid var(--line);border-radius:12px;background:linear-gradient(145deg,rgba(255,255,255,.025),rgba(255,255,255,.01));cursor:pointer;transition:.16s;user-select:none}
.ib-opt:hover{border-color:rgba(59,130,246,.45);transform:translateY(-1px)}
.ib-opt.on{border-color:var(--accent);background:linear-gradient(145deg,rgba(124,58,237,.18),rgba(59,130,246,.08));box-shadow:0 8px 24px rgba(124,58,237,.12),inset 0 0 0 1px rgba(59,130,246,.18)}
.ib-opt.off{opacity:.42;cursor:not-allowed;filter:saturate(.5)}
.ib-opt input{position:absolute;opacity:0;pointer-events:none}
.ib-opt .ib-opt-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(255,255,255,.05);color:var(--accent);font-size:17px;flex:0 0 auto}
.ib-opt b{display:block;font-size:11.5px}.ib-opt small{display:block;color:var(--sub2);font-size:8.5px;margin-top:2px}
.ib-step{display:flex;align-items:center;gap:8px;margin-bottom:11px}.ib-step .num{width:24px;height:24px;border-radius:8px;display:grid;place-items:center;background:rgba(124,58,237,.16);color:#c9a8ff;font-size:10px;font-weight:900}.ib-step b{font-size:12px}.ib-step small{display:block;color:var(--sub2);font-size:9px;margin-top:2px}
.ib-divider{height:1px;background:var(--line);margin:15px 0}
.ib-mode-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.ib-mini{padding:9px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);font-size:10px;text-align:center;color:var(--sub)}
.ib-mini b{display:block;color:var(--text);font-size:11px;margin-bottom:2px}
.ib-mini.active{border-color:rgba(34,197,139,.35);background:rgba(34,197,139,.06)}
@media(max-width:700px){.ib-matrix{grid-template-columns:repeat(2,1fr)}.ib-mode-grid{grid-template-columns:repeat(2,1fr)}}
.ib-choice label{position:relative}.ib-choice input{position:absolute;opacity:0;pointer-events:none}.ib-choice span{display:flex;align-items:center;gap:8px;padding:10px 11px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);font-size:12px;cursor:pointer;transition:.15s}.ib-choice span i{font-size:15px;color:var(--sub)}.ib-choice input:checked+span{border-color:var(--accent);background:rgba(79,124,255,.12);box-shadow:inset 0 0 0 1px rgba(79,124,255,.25)}.ib-choice input:checked+span i{color:var(--accent)}
.ib-status{padding:10px 12px;border-radius:10px;border:1px solid var(--line);background:rgba(0,0,0,.12);font-size:11px;line-height:1.8}.ib-status.ok{border-color:rgba(34,197,139,.3);background:rgba(34,197,139,.07)}.ib-status.warn{border-color:rgba(245,165,36,.3);background:rgba(245,165,36,.07)}
.ib-summary{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.ib-summary .sum{padding:9px 10px;border:1px solid var(--line);border-radius:9px;background:var(--panel2)}.ib-summary small{display:block;color:var(--sub2);font-size:9.5px}.ib-summary b{display:block;margin-top:3px;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ib-advanced{display:none}.ib-advanced.open{display:block}.ib-advanced-toggle{width:100%;justify-content:space-between}.ib-help{font-size:10.5px;color:var(--sub2);line-height:1.8;margin-top:6px}.ib-danger{color:#ff9b9b}
@media(max-width:600px){.ib-grid,.ib-grid.three,.ib-choice,.ib-summary{grid-template-columns:1fr}.ib-full{grid-column:auto}}

.section-title{font-size:12px;font-weight:800;color:var(--sub);text-transform:uppercase;letter-spacing:.03em;margin-bottom:10px}

/* ===== Message Center ===== */
.message-center{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.message-stat{padding:15px;border:1px solid var(--line);border-radius:15px;background:linear-gradient(145deg,var(--panel),rgba(59,130,246,.04));position:relative;overflow:hidden}.message-stat:after{content:"";position:absolute;inset:auto -20px -30px auto;width:90px;height:90px;border-radius:50%;background:radial-gradient(circle,var(--accent),transparent 68%);opacity:.08}.message-stat .ms-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(59,130,246,.12);color:var(--accent);margin-bottom:10px}.message-stat b{font-size:22px;display:block}.message-stat small{display:block;color:var(--sub);font-size:9px;margin-top:4px}.message-stat.danger .ms-icon{color:#fb7185;background:rgba(244,63,94,.11)}.message-stat.warn .ms-icon{color:#fbbf24;background:rgba(245,158,11,.11)}.message-stat.good .ms-icon{color:#34d399;background:rgba(16,185,129,.11)}.message-toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.message-filter{display:flex;gap:6px;flex-wrap:wrap}.message-filter button{padding:7px 10px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--sub);font-size:10px;cursor:pointer}.message-filter button.on{border-color:var(--accent);color:var(--text);background:rgba(59,130,246,.12)}.message-list{display:flex;flex-direction:column;gap:8px;padding:12px}.message-row{display:grid;grid-template-columns:38px 1fr auto;gap:10px;align-items:start;padding:12px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.015)}.message-row:hover{border-color:color-mix(in srgb,var(--accent) 40%,var(--line));background:rgba(255,255,255,.025)}.message-row .mi{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;background:rgba(255,255,255,.04);color:var(--sub)}.message-row.err .mi{color:#fb7185;background:rgba(244,63,94,.09)}.message-row.warn .mi{color:#fbbf24;background:rgba(245,158,11,.09)}.message-row.ok .mi{color:#34d399;background:rgba(16,185,129,.09)}.message-row .mt{min-width:0}.message-row .mt b{font-size:11px;display:block;line-height:1.8}.message-row .mt p{font-size:9px;color:var(--sub);margin-top:3px;word-break:break-word;line-height:1.8}.message-row .meta{text-align:left;direction:ltr;color:var(--sub2);font-size:8px;white-space:nowrap}.message-row .meta strong{display:block;color:var(--sub);font-size:9px;margin-bottom:3px}.error-detail{margin-top:8px;padding:9px;border-radius:9px;background:rgba(0,0,0,.16);border:1px dashed var(--line);font-family:ui-monospace,Consolas,monospace;font-size:8px;line-height:1.8;direction:ltr;text-align:left;white-space:pre-wrap;word-break:break-word;color:#aeb9d2;max-height:120px;overflow:auto}.message-empty{padding:45px 20px;text-align:center;color:var(--sub);font-size:11px}.message-empty i{display:block;font-size:34px;color:var(--good);margin-bottom:10px}.message-auto{font-size:9px;color:var(--sub2);margin-right:auto}@media(max-width:900px){.message-center{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.message-center{grid-template-columns:1fr 1fr}.message-row{grid-template-columns:34px 1fr}.message-row .meta{grid-column:2;text-align:right;direction:rtl}.message-auto{display:none}}
/* toast */
#toastWrap{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:200;display:flex;flex-direction:column;gap:8px}
.toast{background:var(--panel2);border:1px solid var(--line2);padding:11px 18px;border-radius:10px;font-size:13px;display:flex;align-items:center;gap:9px;box-shadow:0 10px 30px rgba(0,0,0,.4);animation:up .18s ease}
.toast.ok{border-color:rgba(34,197,139,.4)}.toast.ok i{color:var(--good)}
.toast.err{border-color:rgba(242,73,85,.4)}.toast.err i{color:var(--bad)}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

.qr-box{background:#fff;padding:10px;border-radius:12px;width:150px;height:150px;margin:0 auto 12px}
.qr-box img{width:100%;height:100%}
.copy-row{display:flex;gap:8px}
.copy-row input{flex:1}

.two-col{display:grid;grid-template-columns:1.1fr .9fr;gap:18px}
@media(max-width:980px){.two-col{grid-template-columns:1fr}}
.status-dot{width:9px;height:9px;border-radius:50%;display:inline-block;margin-left:6px}
.status-dot.on{background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18)}
.status-dot.off{background:var(--sub2)}
.settings-card{padding:20px}
.link-cell{display:flex;flex-direction:column;gap:2px}
.link-cell b{font-size:13px}
.link-cell span{font-size:11px;color:var(--sub2)}
.loading{opacity:.5;pointer-events:none}

/* FaultPass 17 — original premium control-center skin */
body{background:radial-gradient(900px 500px at 75% -10%,rgba(59,130,246,.10),transparent 65%),var(--bg)}
/* رفع باگ اصلیِ «پوسته روشن»: پیش‌تر پس‌زمینه‌ی سایدبار و نوار بالا همیشه
   با رنگ ثابت تیره نوشته شده بود و data-theme را نادیده می‌گرفت؛ در نتیجه
   با فعال کردن پوسته‌ی روشن، فقط بدنه‌ی صفحه سفید می‌شد ولی سایدبار/تاپ‌بار
   تیره می‌ماند (ظاهر ناقص و دو رنگ). این‌جا هر دو حالت را صریحاً تعریف می‌کنیم. */
[data-theme="dark"] .sidebar,
:root:not([data-theme]) .sidebar{background:linear-gradient(180deg,#0d111b 0%,#0b0f17 100%);box-shadow:inset -1px 0 rgba(255,255,255,.04),20px 0 60px rgba(0,0,0,.16)}
[data-theme="light"] .sidebar{background:linear-gradient(180deg,#ffffff 0%,#f7f8fb 100%);box-shadow:inset -1px 0 rgba(0,0,0,.04),20px 0 50px rgba(30,34,60,.05)}
.sidebar{width:268px}
.sidebar-brand{padding:18px 20px 17px}.sidebar-brand img{width:38px;height:38px;border-radius:12px}.sidebar-brand div{font-size:15px}.sidebar-brand small{color:var(--sub2)}
.tab{padding:11px 14px;border-radius:11px;margin:2px 0}.tab-locked{opacity:.58}.tab-locked:hover{opacity:.85}.tab.on{background:linear-gradient(135deg,var(--accent),var(--accent-d));box-shadow:0 10px 25px -10px rgba(59,130,246,.55)}
[data-theme="dark"] .topbar,
:root:not([data-theme]) .topbar{height:68px;padding:0 26px;background:rgba(13,17,27,.88);backdrop-filter:none;box-shadow:0 1px 0 rgba(255,255,255,.025)}
[data-theme="light"] .topbar{height:68px;padding:0 26px;background:rgba(255,255,255,.88);backdrop-filter:none;box-shadow:0 1px 0 rgba(30,34,60,.04)}
.body-wrap{padding:24px 28px 70px}.page{max-width:1440px}
.pg-head{margin-bottom:18px}.pg-head h1{font-size:22px;letter-spacing:-.4px}.pg-head p{font-size:12px}
.eyebrow{font-size:10px;letter-spacing:.16em;color:#8d82c9;font-weight:800;margin-bottom:7px}.live-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#22c58b;box-shadow:0 0 0 4px rgba(34,197,139,.10);vertical-align:middle;margin-left:5px}
.stat-grid{gap:12px}.stat-card{border-radius:16px;padding:16px 18px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.018));box-shadow:var(--shadow-sm)}
.card{border-radius:16px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.018));box-shadow:var(--shadow-sm)}
.inbound-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:0 0 16px}.inbound-strip>div{display:flex;align-items:center;gap:11px;padding:13px 15px;border:1px solid var(--line);background:rgba(255,255,255,.018);border-radius:13px}.inbound-strip i{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;background:rgba(59,130,246,.12);color:#a997ff;font-size:17px}.inbound-strip b{display:block;font-size:12px}.inbound-strip small{display:block;color:var(--sub);font-size:10px;margin-top:2px}.btn-inbound{padding-left:20px;padding-right:20px;box-shadow:0 12px 30px -12px rgba(59,130,246,.75)}
.endpoint-input{display:flex;gap:7px;align-items:stretch}.endpoint-input input{flex:1;min-width:0}.endpoint-btn{white-space:nowrap;padding:9px 11px;font-size:11px}.endpoint-btn:disabled{opacity:.65}.ib-status.ok{border-color:rgba(34,197,139,.35)!important}.ib-status.warn{border-color:rgba(245,165,36,.35)!important}@media(max-width:800px){.inbound-strip{grid-template-columns:1fr}.body-wrap{padding:18px 14px 60px}}

.resource-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}.resource-card{min-height:126px;padding:13px 15px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.015));overflow:hidden}.rc-head{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--sub);font-weight:800;letter-spacing:.08em}.rc-head i{margin-left:5px;color:#7688a9}.rc-head b{font-size:21px;color:var(--text);letter-spacing:0}.rc-sub{font-size:9px;color:var(--sub2);margin-top:6px}.spark{display:block;width:100%;height:44px;margin-top:9px}.spark polyline{fill:none;stroke:#557bff;stroke-width:2;vector-effect:non-scaling-stroke}.spark path{fill:rgba(85,123,255,.08);stroke:none}.traffic-layout{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(290px,.55fr);gap:14px;margin-bottom:14px}.traffic-card,.connection-card{padding:0}.panel-head{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;border-bottom:1px solid var(--line)}.panel-head b{display:block;font-size:10px;letter-spacing:.09em}.panel-head small{display:block;color:var(--sub2);font-size:9px;margin-top:4px}.panel-head>i{color:var(--sub2)}.traffic-legend{display:flex;gap:14px;font-size:10px;color:var(--sub)}.traffic-legend b{color:var(--text)}.big-chart{height:250px;padding:10px 14px 0}.big-chart svg{width:100%;height:100%}.big-chart polyline{fill:none;stroke:#5b78d9;stroke-width:2;vector-effect:non-scaling-stroke}.big-chart .area{fill:rgba(91,120,217,.07);stroke:none}.traffic-foot{display:grid;grid-template-columns:1fr 1fr 1.5fr;padding:12px 16px;border-top:1px solid var(--line)}.traffic-foot small{display:block;color:var(--sub2);font-size:8px}.traffic-foot b{font-size:12px}.connection-number{font-size:28px;font-weight:900;padding:16px 18px 0}.connection-label{font-size:8px;color:var(--sub2);padding:2px 18px}.conn-chart{width:100%;height:120px;padding:0 12px}.conn-chart polyline{fill:none;stroke:#4f7cff;stroke-width:2;vector-effect:non-scaling-stroke}.conn-chart .area{fill:rgba(79,124,255,.08);stroke:none}.conn-foot{display:flex;justify-content:space-between;padding:10px 16px;border-top:1px solid var(--line);font-size:9px;color:var(--sub)}.conn-foot b{color:var(--text)}.bottom-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}.mini-panel{padding-bottom:10px}.health-row{display:flex;justify-content:space-between;padding:10px 16px;border-bottom:1px solid var(--line);font-size:11px}.health-row:last-child{border-bottom:0}.health-row span{color:var(--sub)}.health-row b{max-width:68%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.mono{direction:ltr;text-align:left}.mini-panel .panel-head .badge{font-size:8px}.inbound-head{align-items:center}@media(max-width:1050px){.resource-grid{grid-template-columns:repeat(2,1fr)}.traffic-layout{grid-template-columns:1fr}.bottom-grid{grid-template-columns:1fr}}@media(max-width:560px){.resource-grid{grid-template-columns:1fr}.traffic-foot{grid-template-columns:1fr;gap:10px}.big-chart{height:190px}}

.client-manager{display:flex;flex-direction:column;gap:12px}.client-hero{display:flex;justify-content:space-between;gap:12px;padding:14px;border:1px solid var(--line);border-radius:14px;background:linear-gradient(135deg,rgba(59,130,246,.12),rgba(57,214,255,.04))}.client-hero b{display:block;font-size:13px}.client-hero small{display:block;color:var(--sub);font-size:10px;line-height:1.8;margin-top:4px}.client-create{padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel2)}.client-list{display:flex;flex-direction:column;gap:8px}.client-row{display:flex;align-items:center;gap:10px;padding:11px;border:1px solid var(--line);border-radius:13px;background:rgba(255,255,255,.018)}.client-avatar{width:38px;height:38px;display:grid;place-items:center;border-radius:11px;background:rgba(59,130,246,.12);color:var(--accent);font-size:17px}.client-main{flex:1;min-width:0}.client-main b{display:block;font-size:11px}.client-main small{display:block;color:var(--sub2);font-size:8px;margin-top:3px;overflow:hidden;text-overflow:ellipsis}.client-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.client-tags span{font-size:8px;color:var(--sub);padding:4px 6px;border:1px solid var(--line);border-radius:7px}.client-actions{display:flex;gap:5px}.empty-client{padding:24px;text-align:center;color:var(--sub2);font-size:10px}.danger-note{border-color:rgba(239,68,68,.3)!important}
.pro-diagnostics{overflow:hidden}.diag-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:14px}.diag-item{border:1px solid var(--line);border-radius:13px;padding:12px;background:rgba(255,255,255,.018)}.diag-item small,.diag-item span{display:block;color:var(--sub2);font-size:9px}.diag-item b{display:block;font-size:18px;margin:5px 0}.diag-empty{grid-column:1/-1;padding:22px;text-align:center;color:var(--sub2)}@media(max-width:900px){.diag-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:520px){.diag-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<script>(function(){
  // نکته (رفع باگ): قبلاً این اسکریپت اولیه از کلید localStorage جداگانه‌ای
  // به‌نام «vw_theme» می‌خواند که هیچ‌جای برنامه هرگز در آن چیزی نمی‌نوشت
  // (تنظیمات واقعی همیشه زیر کلید «vw_appearance» ذخیره می‌شود)، پس همیشه
  // مقدار پیش‌فرض «dark» اعمال می‌شد و باعث یک فلاش کوتاهِ پوسته‌ی اشتباه
  // در بارگذاری اولیه‌ی صفحه می‌شد، تا وقتی اسکریپت اصلی اجرا شود.
  try{
    var raw = localStorage.getItem('vw_appearance');
    var pref = raw ? (JSON.parse(raw).theme || 'dark') : 'dark';
    var resolved = pref === 'system'
      ? (matchMedia('(prefers-color-scheme:light)').matches ? 'light' : 'dark')
      : pref;
    document.documentElement.setAttribute('data-theme', resolved);
  }catch(e){ document.documentElement.setAttribute('data-theme','dark'); }
})();</script>
<div id="app">
  <div class="sidebar-overlay" onclick="toggleSidebar()"></div>
  <div class="sidebar">
    <div class="sidebar-brand"><img src="data:image/png;base64,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"><div><span data-i18n="brand">FaultPass</span><small>Control Center</small></div></div>
    <div class="tabnav" id="tabnav">
      <div class="tab on" data-pg="overview"><i class="ti ti-layout-dashboard"></i><span data-i18n="nav_overview">داشبورد</span></div>
      <div class="tab" data-pg="links"><i class="ti ti-network"></i><span data-i18n="nav_links">اینباندها</span><span class="bd" id="nb-links">0</span></div>
      <div class="tab" data-pg="clientmgr"><i class="ti ti-user-plus"></i><span data-i18n="nav_clientmgr">ساخت کلاینت</span></div>
      <div class="tab" data-pg="categories"><i class="ti ti-category"></i><span data-i18n="nav_categories">دسته‌بندی‌ها</span></div>
      <div class="tab" data-pg="subgroups"><i class="ti ti-folders"></i><span data-i18n="nav_subgroups">گروه‌های ساب</span><span class="bd" id="nb-subs">0</span></div>
      <div class="tab" data-pg="nodes"><i class="ti ti-server-cog"></i><span data-i18n="nav_nodes">نودها (چند لوکیشن)</span></div>
      <div class="tab" data-pg="plans"><i class="ti ti-shopping-bag"></i><span data-i18n="nav_plans">پلن‌های فروش</span></div>
      <div class="tab" data-pg="reports"><i class="ti ti-chart-histogram"></i><span data-i18n="nav_reports">گزارش‌ها</span></div>
      <div class="tab" data-pg="admins"><i class="ti ti-users-group"></i><span data-i18n="nav_admins">ادمین‌ها</span></div>
      <div class="tab" data-pg="activity"><i class="ti ti-history"></i><span data-i18n="nav_activity">فعالیت‌ها</span></div>
      <div class="tab" data-pg="messages"><i class="ti ti-bell-ringing"></i><span data-i18n="nav_messages">پیام‌ها</span><span class="bd danger-bd" id="nb-errors">0</span></div>
      <div class="tab" data-pg="settings"><i class="ti ti-settings"></i><span data-i18n="nav_settings">تنظیمات</span></div>
    </div>
    <div class="sidebar-foot">
      <div class="lang-mini">
        <button id="dashLangFa" class="on" onclick="setDashLang('fa')">فا</button>
        <button id="dashLangEn" onclick="setDashLang('en')">EN</button>
      </div>
      <div class="user-chip" id="userChip"><div class="av">V</div><span id="userName">...</span></div>
    </div>
  </div>

  <div class="main-col">
  <div class="topbar">
    <button class="hamburger" onclick="toggleSidebar()"><i class="ti ti-menu-2"></i></button>
    <div class="page-title"><span id="pageTitleMain" data-i18n="nav_overview">داشبورد</span><span id="pageTitleSub" data-i18n="pt_overview">وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات فروش</span></div>
    <div class="top-right">
      <button class="nd-switch" id="nodeSwitchBtn" style="display:none" onclick="openNodeSwitcher()" title="انتخاب پنل/نود برای مدیریت"></button>
      <button class="icon-btn" id="themeToggle" onclick="toggleTheme()" title="تغییر پوسته"><i class="ti ti-moon"></i></button>
      <a class="icon-btn" href="/logout" title="خروج"><i class="ti ti-logout"></i></a>
    </div>
  </div>

  <div class="nd-banner" id="nodeBanner" style="display:none"></div>
  <div class="body-wrap">

    <!-- OVERVIEW -->
    <div class="page on" id="pg-overview">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> LIVE SYSTEM MONITOR</div><h1>مرکز کنترل FaultPass</h1><p>نمای لحظه‌ای منابع سرور، ترافیک، اتصال‌ها و سرویس فروش.</p></div>
        <div class="toolbar"><button class="btn" onclick="refreshOverview()"><i class="ti ti-refresh"></i>بروزرسانی</button><button class="btn primary" onclick="gotoPage('links')"><i class="ti ti-network"></i>اینباندها</button></div></div>
      <div class="ib-quickstats ov-quickstats" id="ovBizStats"></div>
      <div class="resource-grid" id="resourceGrid">
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-cpu"></i> CPU</span><b id="cpuVal">—</b></div><div class="rc-sub" id="cpuSub">در حال دریافت...</div><svg class="spark" id="cpuSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-device-ram"></i> RAM</span><b id="ramVal">—</b></div><div class="rc-sub" id="ramSub">—</div><svg class="spark" id="ramSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-bolt"></i> SWAP</span><b id="swapVal">—</b></div><div class="rc-sub" id="swapSub">—</div><svg class="spark" id="swapSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
        <div class="resource-card"><div class="rc-head"><span><i class="ti ti-database"></i> STORAGE</span><b id="storageVal">—</b></div><div class="rc-sub" id="storageSub">—</div><svg class="spark" id="storageSpark" viewBox="0 0 240 46" preserveAspectRatio="none"></svg></div>
      </div>
      <div class="traffic-layout">
        <div class="card traffic-card"><div class="panel-head"><div><b>OVERALL SPEED</b><small id="speedMeta">Network throughput</small></div><div class="traffic-legend"><span>↑ <b id="txRate">0 B/s</b></span><span>↓ <b id="rxRate">0 B/s</b></span></div></div><div class="big-chart"><svg id="trafficChart" viewBox="0 0 900 260" preserveAspectRatio="none"></svg></div><div class="traffic-foot"><div><small>SENT</small><b id="sentTotal">0 B</b></div><div><small>RECEIVED</small><b id="recvTotal">0 B</b></div><div><small>LIVE THROUGHPUT</small><b id="liveRate">↑ 0 B/s ↓ 0 B/s</b></div></div></div>
        <div class="card connection-card"><div class="panel-head"><div><b>CONNECTION STATS</b><small>Open sockets</small></div><i class="ti ti-plug-connected"></i></div><div class="connection-number" id="connVal">0</div><div class="connection-label">OPEN CONNECTIONS</div><svg class="conn-chart" id="connChart" viewBox="0 0 340 150" preserveAspectRatio="none"></svg><div class="conn-foot"><span>REQUESTS <b id="reqVal">0</b></span><span>ERRORS <b id="errVal">0</b></span></div></div>
      </div>
      <div class="bottom-grid">
        <div class="card mini-panel"><div class="panel-head"><div><b>SERVICE HEALTH</b><small>Runtime status</small></div><span class="badge green">ONLINE</span></div><div class="health-row"><span>Uptime</span><b id="uptimeVal">—</b></div><div class="health-row"><span>CPU Cores</span><b id="coresVal">—</b></div><div class="health-row"><span>Panel RAM</span><b id="procRamVal">—</b></div></div>
        <div class="card mini-panel"><div class="panel-head"><div><b>BOT SERVICES</b><small>Sales + management</small></div><span id="ovBotStatus" class="badge gray">CHECKING</span></div><div class="health-row"><span>Telegram Bot</span><b id="botStateText">—</b></div><div class="health-row"><span>Public URL</span><b class="mono" id="ovBaseUrl">—</b></div></div>
        <div class="card mini-panel"><div class="panel-head"><div><b>NETWORK</b><small>Host load</small></div><i class="ti ti-world"></i></div><div class="health-row"><span>Load</span><b id="loadVal">—</b></div><div class="health-row"><span>Traffic</span><b id="trafficTotalVal">0 B</b></div></div>
      </div>
      <div class="card mini-panel" style="margin-top:14px"><div class="panel-head"><div><b>TOP CONFIGS BY USAGE</b><small>پرمصرف‌ترین کانفیگ‌های ۷ روز اخیر</small></div><i class="ti ti-trending-up"></i></div><div id="ovTopLinks" class="ov-toplinks"></div></div>
    </div>

    <!-- LINKS -->
    <div class="page" id="pg-links">
      <div class="pg-head inbound-head"><div><div class="eyebrow"><span class="live-dot"></span> FAULTPASS CORE · <span id="ibLiveTag">LIVE</span></div><h1>اینباندها</h1><p>مرکز مدیریت اینباند، ساخت کلاینت و کنترل دسترسی؛ با پایش زنده هر ۵ ثانیه.</p></div>
        <div class="toolbar">
          <div class="search"><input id="linkSearch" placeholder="جستجوی اینباند / UUID..." oninput="renderLinks()"><i class="ti ti-search"></i></div>
          <select class="sel" id="linkFilterCat" onchange="renderLinks()"><option value="">همه دسته‌ها</option></select>
          <span id="ibUpdatedAt" style="font-size:9px;color:var(--sub2);align-self:center;white-space:nowrap">—</span>
          <button class="btn" id="ibRefreshBtn" onclick="refreshAllInbounds()"><i class="ti ti-refresh" id="ibRefreshIcon"></i>بروزرسانی همه</button>
          <button class="btn" onclick="openOutboundManager()" title="مدیریت پراکسی‌های خروجی (SOCKS5 / SOCKS4 / HTTP)"><i class="ti ti-route"></i>اوتباند</button>
          <button class="btn" onclick="openAutoLink()"><i class="ti ti-wand"></i>ساخت هوشمند</button>
          <button class="btn primary btn-inbound" onclick="openLinkDrawer()"><i class="ti ti-plus"></i>اینباند جدید</button>
        </div>
      </div>
      <div class="ib-quickstats" id="ibQuickStats"></div>
      <div class="ib-listbar">
        <label class="ib-selectall"><input type="checkbox" id="ibSelAll" onchange="toggleAllLinks(this.checked)"><span>انتخاب همه</span></label>
        <span class="ib-count" id="ibCountLabel">0 اینباند</span>
      </div>
      <div class="ib-bulkbar" id="ibBulkBar" style="display:none">
        <span><b id="ibSelCount">0</b> مورد انتخاب شده</span>
        <div class="ib-bulkactions">
          <button class="btn sm" onclick="bulkOutbound()"><i class="ti ti-route"></i>خروجی (Outbound)</button>
          <button class="btn sm" onclick="bulkToggleLinks(true)"><i class="ti ti-power"></i>فعال‌سازی</button>
          <button class="btn sm" onclick="bulkToggleLinks(false)"><i class="ti ti-power"></i>غیرفعال‌سازی</button>
          <button class="btn sm" style="color:var(--bad)" onclick="bulkDeleteLinks()"><i class="ti ti-trash"></i>حذف</button>
        </div>
      </div>
      <div class="ib-grid" id="ibGrid"></div>
      <div class="empty" id="linksEmpty" style="display:none"><i class="ti ti-inbox"></i>کانفیگی یافت نشد</div>
    </div>

    <!-- CLIENT MANAGER (بخش جدای ساخت کلاینت از روی اینباند) -->
    <div class="page" id="pg-clientmgr">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> FAULTPASS · CLIENT MANAGER</div><h1>ساخت کلاینت</h1><p>یک اینباند را انتخاب کن و از روی همان کلاینت‌های واقعی (زیرمجموعه) بساز؛ بدون نیاز به رفتن به صفحه اینباندها.</p></div>
        <div class="toolbar"><button class="btn" onclick="loadClientManager()"><i class="ti ti-refresh"></i>بروزرسانی</button></div>
      </div>
      <div class="card" style="padding:18px;margin-bottom:14px">
        <div class="grp"><label>انتخاب اینباند</label>
          <select class="sel" id="cmInboundSelect" style="width:100%" onchange="loadClientManagerClients(this.value)"><option value="">— انتخاب کنید —</option></select>
        </div>
        <div id="cmInboundInfo"></div>
      </div>
      <div id="cmBody"></div>
    </div>

    <!-- CATEGORIES -->
    <div class="page" id="pg-categories">
      <div class="pg-head"><div><h1>دسته‌بندی‌ها</h1><p>پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ</p></div>
        <div class="toolbar"><button class="btn primary" onclick="openCategoryDrawer()"><i class="ti ti-plus"></i>دسته جدید</button></div>
      </div>
      <div class="card"><table><thead><tr><th>نام</th><th>حجم پیش‌فرض</th><th>انقضا (روز)</th><th>محدودیت IP</th><th></th></tr></thead><tbody id="catsBody"></tbody></table></div>
    </div>

    <!-- SUBGROUPS -->
    <div class="page" id="pg-subgroups">
      <div class="pg-head"><div><h1>گروه‌های ساب</h1><p>ترکیب چند کانفیگ در یک لینک اشتراک واحد</p></div>
        <div class="toolbar"><button class="btn primary" onclick="openSubGroupDrawer()"><i class="ti ti-plus"></i>گروه جدید</button></div>
      </div>
      <div class="card"><table><thead><tr><th>نام گروه</th><th>تعداد کانفیگ (این پنل + نودها)</th><th>لینک عمومی</th><th></th></tr></thead><tbody id="subsBody"></tbody></table></div>
    </div>

    <!-- NODES -->
    <div class="page" id="pg-nodes">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> FAULTPASS · NODES</div><h1>نودها</h1><p>چند پنل FaultPass را به هم وصل کن (هر کدام در یک لوکیشن) و همه را از یک پنل مدیریت کن.</p></div>
        <div class="toolbar"><button class="btn" onclick="checkAllNodes()"><i class="ti ti-refresh"></i>بررسی همه</button><button class="btn primary" onclick="openNodeDrawer()"><i class="ti ti-plus"></i>افزودن نود</button></div>
      </div>
      <div class="card" style="margin-bottom:14px"><div class="panel-head"><div><b><i class="ti ti-key"></i> توکن این پنل (وقتی این پنل «نود» است)</b><small>توکن را کپی کن و در پنل اصلی، بخش نودها، بچسبان</small></div></div><div style="padding:0 18px 18px" id="nodeTokenBody"></div></div>
      <div class="card"><div class="panel-head"><div><b>نودهای متصل به این پنل</b><small>وضعیت هر ۳۰ ثانیه به‌روز می‌شود · «مدیریت» کل پنل را روی همان نود اجرا می‌کند</small></div></div><div style="padding:0 18px 18px" id="nodesList"></div></div>
    </div>

    <!-- PLANS -->
    <div class="page" id="pg-plans">
      <div class="pg-head"><div><h1>پلن‌های فروش</h1><p>پلن‌هایی که در ربات فروش تلگرام نمایش داده می‌شوند</p></div>
        <div class="toolbar"><button class="btn primary" onclick="openPlanDrawer()"><i class="ti ti-plus"></i>پلن جدید</button></div>
      </div>
      <div class="card"><table><thead><tr><th>نام</th><th>مدت</th><th>حجم</th><th>سرعت</th><th>قیمت (⭐)</th><th>ویژه</th><th></th></tr></thead><tbody id="plansBody"></tbody></table></div>
    </div>

    <!-- REPORTS -->
    <div class="page" id="pg-reports">
      <div class="pg-head"><div><h1>گزارش‌ها</h1><p>خلاصه‌ی عملکرد فروش و کانفیگ‌ها</p></div>
        <div class="toolbar">
          <select class="sel" id="repDays" onchange="loadReports()"><option value="7">۷ روز اخیر</option><option value="14" selected>۱۴ روز اخیر</option><option value="30">۳۰ روز اخیر</option></select>
          <a class="btn" href="/api/reports/export.csv"><i class="ti ti-download"></i>خروجی CSV</a>
        </div>
      </div>
      <div class="stat-grid" id="repStats"></div>
      <div class="card">
        <div style="padding:16px 18px;border-bottom:1px solid var(--line)"><b style="font-size:13px">پرمصرف‌ترین کانفیگ‌ها</b></div>
        <table><thead><tr><th>برچسب</th><th>پروتکل</th><th>مصرف</th></tr></thead><tbody id="repTopBody"></tbody></table>
      </div>
    </div>

    <!-- ADMINS -->
    <div class="page" id="pg-admins">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> FAULTPASS · مدیریت حساب</div><h1>مدیریت حساب‌ها</h1><p>اینجا همه حساب‌های مدیریتی پنل را مرتب و دقیق مدیریت می‌کنیم؛ از ساخت ادمین تا تعیین دسترسی و کنترل وضعیت حساب.</p></div>
        <div class="toolbar"><button class="btn" onclick="loadAdmins()"><i class="ti ti-refresh"></i>همگام‌سازی</button><button class="btn primary" onclick="openAdminDrawer()"><i class="ti ti-user-plus"></i>ایجاد حساب مدیریتی</button></div>
      </div>
      <div class="admins-hero">
        <div class="access-command-copy"><div class="command-badge"><i class="ti ti-shield-lock"></i> مدیریت حساب‌ها</div><h2>مدیریت کامل ادمین‌ها</h2><p>حساب اصلی پنل دسترسی کامل دارد و برای هر ادمین می‌توان دسترسی‌های موردنیاز را جداگانه تعیین کرد. وضعیت هر حساب و آخرین ورود نیز از همین بخش قابل بررسی است.</p><div class="command-points"><span><i class="ti ti-check"></i> تفکیک دسترسی</span><span><i class="ti ti-check"></i> ثبت آخرین ورود</span><span><i class="ti ti-check"></i> امنیت حساب‌ها</span></div></div>
        <div class="admins-summary" id="adminsSummary"><div class="sum"><b id="adminTotal">—</b><small>حساب مدیریتی</small></div><div class="sum"><b id="adminActive">—</b><small>حساب فعال</small></div><div class="sum"><b id="adminOwner">1</b><small>مالک پنل</small></div></div>
      </div>
      <div class="card admin-directory" id="adminReqCard" style="margin-bottom:14px;display:none"><div class="panel-head"><div><b>درخواست‌های ثبت‌نام ادمینی</b><small>افرادی که از صفحه ورود درخواست همکاری داده‌اند؛ بررسی کن و تصمیم بگیر.</small></div><span class="command-badge" id="adminReqBadge">۰ درخواست</span></div><div id="adminReqBody" style="padding:14px 18px"></div></div>
      <div class="card admin-directory"><div class="panel-head"><div><b>فهرست ادمین‌ها</b><small>وضعیت، دسترسی و فعالیت هر ادمین را از یکجا بررسی و مدیریت کن.</small></div><span class="directory-live"><i></i> کنترل فعال</span></div><div class="admin-grid" id="adminsBody"></div></div>
    </div>

    <!-- ACTIVITY -->
    <div class="page" id="pg-activity">
      <div class="pg-head"><div><h1>لاگ فعالیت‌ها</h1><p>۱۵۰ رویداد اخیر پنل</p></div>
        <div class="toolbar"><button class="btn" onclick="loadActivity()"><i class="ti ti-refresh"></i>بروزرسانی</button></div>
      </div>
      <div class="card"><table><thead><tr><th>زمان</th><th>نوع</th><th>پیام</th></tr></thead><tbody id="activityBody"></tbody></table></div>
    </div>

    <!-- MESSAGES -->
    <div class="page" id="pg-messages">
      <div class="pg-head"><div><div class="eyebrow"><span class="live-dot"></span> MESSAGE CENTER</div><h1>مرکز پیام و خطا</h1><p>تمام خطاهای سرور، خطاهای مرورگر و رویدادهای مهم اینجا جمع می‌شوند تا هیچ خطایی گم نشود.</p></div><div class="toolbar"><span class="message-auto" id="messageLastSync">همگام‌سازی خودکار</span><button class="btn" onclick="loadMessages()"><i class="ti ti-refresh"></i>بروزرسانی</button><button class="btn danger" onclick="clearErrors()"><i class="ti ti-trash"></i>پاک‌کردن خطاها</button></div></div>
      <div class="message-center" id="messageStats"></div>
      <div class="card">
        <div class="panel-head"><div><b>خطاهای ثبت‌شده</b><small>خطاهای Backend و Frontend با جزئیات مسیر و زمان</small></div><div class="message-filter"><button class="on" data-message-filter="all" onclick="setMessageFilter('all')">همه</button><button data-message-filter="err" onclick="setMessageFilter('err')">خطا</button><button data-message-filter="warn" onclick="setMessageFilter('warn')">هشدار</button><button data-message-filter="client" onclick="setMessageFilter('client')">مرورگر</button></div></div>
        <div class="message-list" id="messageList"></div>
      </div>
      <div class="card" style="margin-top:14px"><div class="panel-head"><div><b>رویدادهای مهم</b><small>آخرین فعالیت‌های پنل برای عیب‌یابی سریع</small></div></div><div class="message-list" id="messageActivityList"></div></div>
    </div>

    <!-- SETTINGS -->
    <div class="page" id="pg-settings">
      <div class="pg-head"><div><div class="eyebrow">CONTROL CENTER / PERSONALIZATION</div><h1>تنظیمات و استودیو ظاهر</h1><p>ظاهر، فونت، رنگ، تراکم، زبان و تنظیمات عملیاتی پنل را از یکجا کنترل کن.</p></div><div class="toolbar"><button class="btn" onclick="resetAppearance()"><i class="ti ti-refresh"></i>بازنشانی ظاهر</button></div></div>

      <div class="appearance-studio">
        <div class="appearance-card">
          <h3>Appearance Studio</h3><p>تنظیمات ظاهری فقط برای همین مرورگر ذخیره می‌شوند و بدون دست‌زدن به اطلاعات سرور قابل تغییرند.</p>
          <div class="appearance-grid">
            <div class="appearance-field"><label>فونت رابط کاربری</label><select id="appearanceFont" onchange="setFont(this.value)"><option value="Vazirmatn">Vazirmatn</option><option value="Estedad">Estedad</option><option value="IBM Plex Sans Arabic">IBM Plex Sans Arabic</option><option value="Shabnam">Shabnam</option><option value="Yekan Bakh">Yekan Bakh</option><option value="Inter">Inter</option></select></div>
            <div class="appearance-field"><label>اندازه متن</label><div class="theme-pills"><button class="theme-pill" data-font-size="small" onclick="setFontSize('small')">Small</button><button class="theme-pill" data-font-size="normal" onclick="setFontSize('normal')">Normal</button><button class="theme-pill" data-font-size="large" onclick="setFontSize('large')">Large</button></div></div>
            <div class="appearance-field"><label>تراکم پنل</label><div class="theme-pills"><button class="theme-pill" data-density="comfortable" onclick="setDensity('comfortable')">Comfort</button><button class="theme-pill" data-density="compact" onclick="setDensity('compact')">Compact</button></div></div>
            <div class="appearance-field"><label>گوشه‌ها</label><div class="theme-pills"><button class="theme-pill" data-radius="soft" onclick="setRadius('soft')">Soft</button><button class="theme-pill" data-radius="sharp" onclick="setRadius('sharp')">Sharp</button><button class="theme-pill" data-radius="pill" onclick="setRadius('pill')">Pill</button></div></div>
            <div class="appearance-field"><label>پوسته</label><div class="theme-pills"><button class="theme-pill" data-theme-choice="dark" onclick="setAppearanceTheme('dark')">Dark</button><button class="theme-pill" data-theme-choice="light" onclick="setAppearanceTheme('light')">Light</button><button class="theme-pill" data-theme-choice="system" onclick="setAppearanceTheme('system')">System</button></div></div>
            <div class="appearance-field"><label>رنگ اصلی</label><div class="accent-pills"><button class="accent-pill" data-accent="purple" onclick="setAccent('purple')"><span class="accent-dot" style="background:#3b82f6"></span>Purple</button><button class="accent-pill" data-accent="blue" onclick="setAccent('blue')"><span class="accent-dot" style="background:#3b82f6"></span>Blue</button><button class="accent-pill" data-accent="cyan" onclick="setAccent('cyan')"><span class="accent-dot" style="background:#06b6d4"></span>Cyan</button><button class="accent-pill" data-accent="green" onclick="setAccent('green')"><span class="accent-dot" style="background:#10b981"></span>Green</button><button class="accent-pill" data-accent="orange" onclick="setAccent('orange')"><span class="accent-dot" style="background:#f59e0b"></span>Orange</button><button class="accent-pill" data-accent="pink" onclick="setAccent('pink')"><span class="accent-dot" style="background:#ec4899"></span>Pink</button><button class="accent-pill" data-accent="red" onclick="setAccent('red')"><span class="accent-dot" style="background:#ef4444"></span>Red</button><button class="accent-pill" data-accent="indigo" onclick="setAccent('indigo')"><span class="accent-dot" style="background:#2563eb"></span>Indigo</button><button class="accent-pill" data-accent="teal" onclick="setAccent('teal')"><span class="accent-dot" style="background:#14b8a6"></span>Teal</button><button class="accent-pill" data-accent="gold" onclick="setAccent('gold')"><span class="accent-dot" style="background:#eab308"></span>Gold</button></div></div>
          </div>
          <div class="appearance-actions">
            <div class="appearance-toggle"><span>انیمیشن‌های پنل</span><button id="motionSwitch" class="switch" onclick="toggleMotion()"></button></div>
            <div class="appearance-toggle"><span>سایدبار باز در دسکتاپ</span><button id="wideSwitch" class="switch" onclick="toggleWideSidebar()"></button></div>
            <div class="appearance-toggle"><span>Glow / نورپردازی</span><button id="glowSwitch" class="switch" onclick="toggleGlow()"></button></div>
          </div>
        </div>
        <div class="appearance-card appearance-preview"><div class="preview-window"><div class="preview-top"><i class="ti ti-circle-filled"></i><i class="ti ti-circle-filled"></i><i class="ti ti-circle-filled"></i></div><div class="preview-main"><div class="preview-side"><div class="active"></div><div></div><div></div><div></div></div><div class="preview-content"><div class="pv-title">FaultPass Control Center</div><div class="pv-sub">Live system overview</div><div class="pv-cards"><span></span><span></span><span></span></div></div></div></div></div>
      </div>

      <div class="card pro-diagnostics" style="margin-top:14px">
        <div class="panel-head"><div><b>SYSTEM HEALTH / LIVE DIAGNOSTICS</b><small>Live server, resource, object and security telemetry</small></div><div class="toolbar"><span id="diagStatus" class="badge green">READY</span><button class="btn" onclick="loadDiagnostics()"><i class="ti ti-activity"></i>Refresh</button></div></div>
        <div class="diag-grid" id="diagGrid"><div class="diag-empty">Press Refresh to inspect the live system.</div></div>
      </div>

      <div class="two-col">
        <div class="card settings-card">
          <div class="section-title">آدرس عمومی پنل</div>
          <p class="hint" style="margin-bottom:12px">برای لینک‌های Subscription، دامنه واقعی پنل را ثابت کن. روی Railway بهتر است دامنه عمومی سرویس را اینجا قرار بدهی.</p>
          <div class="grp"><input id="setBaseUrl" placeholder="https://panel.example.com"></div>
          <button class="btn primary" onclick="saveBaseUrl()"><i class="ti ti-device-floppy"></i>ذخیره آدرس</button>
          <div class="divider"></div><div class="section-title">امنیت حساب</div>
          <div class="grp"><label>نام کاربری پنل</label><div class="row2"><input type="text" id="adminUsername" autocomplete="username" maxlength="40" placeholder="admin"><button class="btn primary" onclick="changeUsername()"><i class="ti ti-user-edit"></i>تغییر نام کاربری</button></div><div class="hint">نام کاربری جدید بدون فاصله و بین ۳ تا ۴۰ کاراکتر.</div></div>
          <div class="divider"></div>
          <div class="grp"><label>رمز فعلی</label><div style="position:relative"><input type="password" id="curPass" autocomplete="current-password"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('curPass',this)"><i class="ti ti-eye"></i></button></div></div><div class="row2"><div class="grp"><label>رمز جدید</label><div style="position:relative"><input type="password" id="newPass" autocomplete="new-password" oninput="passwordMeter()"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('newPass',this)"><i class="ti ti-eye"></i></button></div><div id="passMeter" style="height:4px;background:var(--line);border-radius:99px;margin-top:7px;overflow:hidden"><i id="passMeterBar" style="display:block;height:100%;width:0;background:var(--bad);transition:.2s"></i></div><div id="passHint" class="hint">حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.</div></div><div class="grp"><label>تکرار رمز جدید</label><div style="position:relative"><input type="password" id="repPass" autocomplete="new-password"><button type="button" class="iconbtn" style="position:absolute;left:7px;top:6px" onclick="toggleSettingsPass('repPass',this)"><i class="ti ti-eye"></i></button></div></div></div>
          <button class="btn primary" onclick="changePassword()"><i class="ti ti-key"></i>تغییر امن رمز</button><button class="btn" style="margin-right:7px" onclick="revokeOtherSessions()"><i class="ti ti-shield-lock"></i>لغو نشست‌های قبلی</button>
        </div>
        <div class="card settings-card">
          <div class="section-title">Railway Network Center</div>
          <p class="hint" style="margin-bottom:12px">دامنه و پورت TCP عمومی Railway را اینجا مدیریت کن. Railway دامنه و پورت TCP Proxy را خودش تولید می‌کند و باید همان مقدار استفاده شود.</p>
          <div class="row2"><div class="grp"><label>TCP Host</label><input id="setTcpHost" placeholder="roundhouse.proxy.rlwy.net" class="mono" style="direction:ltr;text-align:left"></div><div class="grp"><label>TCP Port</label><input id="setTcpPort" placeholder="11105" class="mono" style="direction:ltr;text-align:left"></div></div>
          <p class="hint" id="tcpListenHint">—</p><button class="btn primary" onclick="saveTcpSettings()"><i class="ti ti-device-floppy"></i>ذخیره شبکه</button>
          <div class="divider"></div><div class="section-title">Sales & Management Bot</div>
          <div class="grp"><label>Bot Token</label><input id="setBotToken" placeholder="123456:ABC-DEF..." class="mono" style="direction:ltr;text-align:left"></div><div class="grp"><label>Admin IDs</label><input id="setBotAdmins" placeholder="123456789,987654321"></div>
          <div style="display:flex;gap:10px;align-items:center;margin-top:8px"><span class="status-dot off" id="botDot"></span><span id="botStatusText" style="font-size:13px">وضعیت نامشخص</span></div><div style="display:flex;gap:10px;margin-top:14px"><button class="btn primary" onclick="saveBotSettings()"><i class="ti ti-device-floppy"></i>ذخیره</button><button class="btn" id="botStartBtn" onclick="botStart()"><i class="ti ti-player-play"></i>شروع</button><button class="btn danger" id="botStopBtn" onclick="botStop()"><i class="ti ti-player-stop"></i>توقف</button></div>
        </div>
      </div>
      <div class="card settings-card tpl-studio" style="margin-top:14px">
        <div class="tpl-studio-head"><div><div class="section-title">Subscription Template</div><p class="hint">همان یک لینک ساب که به کاربر می‌دهی؛ فقط تعیین کن نام کانفیگ داخل اپ او دقیقاً چه چیزهایی را نشان دهد.</p></div><div class="tpl-badge"><i class="ti ti-wand"></i>Template Studio</div></div>
        <div class="tpl-grid">
          <div class="tpl-fields">
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-tag"></i><div><b>نام کانفیگ</b><small>نام دلخواه یا برند شما</small></div></div><input type="checkbox" class="tpl-switch" id="subTplName"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-database"></i><div><b>حجم اختصاص‌یافته</b><small>مثلاً ۵۰ گیگابایت</small></div></div><input type="checkbox" class="tpl-switch" id="subTplVolume"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-fingerprint"></i><div><b>شناسه کانفیگ (ID)</b><small>شناسه کوتاه یکتا</small></div></div><input type="checkbox" class="tpl-switch" id="subTplId"></label>
            <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-router"></i><div><b>نام اینباند</b><small>نام اینباند مادر این کانفیگ</small></div></div><input type="checkbox" class="tpl-switch" id="subTplInbound"></label>
          </div>
          <div class="tpl-preview">
            <div class="tpl-preview-label"><i class="ti ti-device-mobile"></i>پیش‌نمایش داخل اپ کاربر</div>
            <div class="tpl-preview-row"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="subTplPreview">MyConfig</div><span class="tpl-preview-proto">VLESS</span></div>
            <p class="hint" style="margin-top:10px">ترتیب نمایش دقیقاً همین ترتیب بالاست؛ بین هر بخش یک خط جداکننده (|) قرار می‌گیرد.</p>
          </div>
        </div>
        <button class="btn primary" style="margin-top:14px" onclick="saveSubTemplate()"><i class="ti ti-device-floppy"></i>ذخیره الگوی ساب</button>
      </div>

      <div class="card settings-card" style="margin-top:14px">
        <div class="section-title">استایل نام کانفیگ‌ها</div>
        <p class="hint" style="margin-bottom:12px">با روشن بودن این گزینه، اسم ساده مثل FaultPass به‌صورت FaultPass | Aurora 🌠 (اسم و ایموجی خفن) ساخته می‌شود؛ هم در ساخت دستی و هم در «ساخت سریع/هوشمند». اسمی که خودت تزئین کرده باشی (با | یا ایموجی) دست‌نخورده می‌ماند.</p>
        <label class="tpl-row"><div class="tpl-row-main"><i class="ti ti-sparkles"></i><div><b>استایل خودکار نام کانفیگ‌ها</b><small>دستی و خودکار</small></div></div><input type="checkbox" class="tpl-switch" id="nameStyleEnabled" onchange="updateBrandPreview()"></label>
        <div class="tpl-preview" style="margin-top:10px"><div class="tpl-preview-label"><i class="ti ti-device-mobile"></i> پیش‌نمایش در اپ کاربر</div>
          <div class="tpl-preview-row"><span class="tpl-preview-dot"></span><div class="tpl-preview-text" id="brandNamePreview">FaultPass | Aurora 🌠</div><span class="tpl-preview-proto">VLESS</span></div></div>
        <button class="btn primary" style="margin-top:14px" onclick="saveNameStyle()"><i class="ti ti-device-floppy"></i>ذخیره استایل نام</button>
      </div>
      <div class="card settings-card" style="margin-top:14px"><div class="section-title">فروشگاه (پرداخت با ⭐️ استارز تلگرام)</div><p class="hint">وقتی روشنه، هر کاربری با زدن /start روی ربات، پلن‌های تعریف‌شده در «پلن‌های فروش» رو می‌بینه و می‌تونه بخره؛ فوراً هم اثر می‌کنه، نیازی به ری‌استارت نیست.</p><label class="chk"><input type="checkbox" id="setSalesEnabled" onchange="saveSalesToggle()"> فروشگاه فعال باشد</label></div>
      <div class="card settings-card" style="margin-top:14px"><div class="section-title">Bot Text Studio</div><p class="hint">تمام پیام‌های کلیدی ربات را از همین پنل ویرایش کن؛ تغییرات روی ربات در اجرای بعدی/ری‌استارت اعمال می‌شوند.</p><div class="bot-text-grid"><div class="grp"><label>پیام خوش‌آمد</label><textarea id="botTxtWelcome" rows="4"></textarea></div><div class="grp"><label>منوی مدیریت</label><textarea id="botTxtAdmin" rows="4"></textarea></div><div class="grp"><label>پیام ساخت کانفیگ</label><textarea id="botTxtCreated" rows="3"></textarea></div><div class="grp"><label>پیام فروشگاه</label><textarea id="botTxtStore" rows="3"></textarea></div><div class="grp"><label>پیام پرداخت موفق</label><textarea id="botTxtPayment" rows="3"></textarea></div></div><button class="btn primary" onclick="saveBotTexts()"><i class="ti ti-device-floppy"></i>ذخیره متن‌های ربات</button></div>

      <div class="card advanced-settings" style="margin-top:14px"><div class="panel-head"><div><b>CONTROL CENTER PRO</b><small>ابزارهای حرفه‌ای برای شخصی‌سازی و نگهداری پنل</small></div><span class="badge green">PRO</span></div><div class="advanced-grid"><button class="pro-action" onclick="refreshOverview();toast('داده‌های زنده بروزرسانی شد ✓')"><i class="ti ti-activity-heartbeat"></i><b>Live Refresh</b><small>مانیتورینگ فوری منابع</small></button><button class="pro-action" onclick="loadSettings();toast('تنظیمات دوباره بارگذاری شد ✓')"><i class="ti ti-refresh"></i><b>Reload Settings</b><small>دریافت تنظیمات واقعی سرور</small></button><button class="pro-action" onclick="location.reload()"><i class="ti ti-reload"></i><b>Hard Reload</b><small>بارگذاری کامل رابط</small></button><button class="pro-action" onclick="navigator.clipboard?.writeText(location.origin);toast('دامنه پنل کپی شد ✓')"><i class="ti ti-world-copy"></i><b>Copy Panel URL</b><small>دامنه فعلی پنل</small></button></div></div>
    </div>

  </div>
  </div>
</div>

<div class="overlay" id="overlay" onclick="closeDrawer()"></div>
<div class="drawer" id="drawer">
  <div class="dr-head"><h3 id="drTitle">—</h3><button class="iconbtn" onclick="closeDrawer()"><i class="ti ti-x"></i></button></div>
  <div class="dr-body" id="drBody"></div>
  <div class="dr-foot" id="drFoot"></div>
</div>

<div id="toastWrap"></div>

<script>
// ============================================================
// Core helpers
// ============================================================
const $ = (id) => document.getElementById(id);
function toast(msg, ok=true){
  const t = document.createElement('div');
  t.className = 'toast ' + (ok?'ok':'err');
  const safeMsg = dashTranslateValue(String(msg ?? ''), typeof getDashLang === 'function' ? getDashLang() : 'fa');
  t.innerHTML = `<i class="ti ti-${ok?'circle-check':'alert-circle'}"></i><span>${escapeHtml(safeMsg)}</span>`;
  $('toastWrap').appendChild(t);
  setTimeout(()=>t.remove(), 3800);
}
// وقتی یک «نود» برای مدیریت انتخاب شده، APIهای عملیاتی از طریق پنل اصلی روی نود اجرا می‌شن.
const ACTIVE_NODE = (()=>{ try{ return JSON.parse(sessionStorage.getItem('fp_active_node')||'null'); }catch(e){ return null; } })();
const NODE_FWD_PREFIXES = ['/api/links','/api/proxies','/api/subs','/api/categories','/api/protocols','/api/reality-keypair','/api/connections','/api/telemetry','/api/system','/api/network','/api/reports','/api/activity','/api/errors','/stats'];
function nodeRewrite(path){
  if(!ACTIVE_NODE) return path;
  const p = String(path).split('?')[0].replace(/\/+$/,'');
  return NODE_FWD_PREFIXES.some(x=>p===x || p.startsWith(x+'/')) ? `/api/nodes/${ACTIVE_NODE.id}/fwd${path}` : path;
}
async function api(path, opts={}){
  const res = await fetch(nodeRewrite(path), {credentials:'same-origin', headers:{'Content-Type':'application/json'}, ...opts});
  let data = {};
  try{ data = await res.json(); }catch(e){}
  if(!res.ok){
    const message = data.detail || data.error || data.message || ('خطا ' + res.status);
    throw new Error(message);
  }
  return data;
}

let MESSAGE_FILTER='all';
let messageTimer=null;
let reportingClientError=false;
async function reportClientError(message, source='browser', extra={}){
  if(reportingClientError) return;
  reportingClientError=true;
  try{
    await fetch('/api/errors/client',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},keepalive:true,body:JSON.stringify({message:String(message||'Unknown client error').slice(0,1200),source:String(source||'browser').slice(0,40),path:location.pathname,stack:String(extra.stack||'').slice(0,4000),details:String(extra.details||'').slice(0,1500)})});
  }catch(e){} finally{reportingClientError=false;}
}
window.addEventListener('error',e=>{ if(e?.message) reportClientError(e.message,'browser',{stack:e.error?.stack,details:`${e.filename||''}:${e.lineno||''}:${e.colno||''}`}); });
window.addEventListener('unhandledrejection',e=>{ const r=e?.reason; reportClientError(r?.message||String(r||'Unhandled promise rejection'),'promise',{stack:r?.stack}); });
function fmtBytes(n){
  n = Number(n||0);
  if(n<=0) return '0';
  const u=['B','KB','MB','GB','TB']; let i=0;
  while(n>=1024 && i<u.length-1){n/=1024;i++;}
  return n.toFixed(n<10&&i>0?1:0)+' '+u[i];
}
function escapeHtml(s){ return String(s??'').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

// ============================================================
// Nav
// ============================================================
document.querySelectorAll('.tab').forEach(t=>{
  t.addEventListener('click', ()=> gotoPage(t.dataset.pg));
});
function gotoPage(pg){
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on', t.dataset.pg===pg));
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('on', p.id==='pg-'+pg));
  CURRENT_PAGE = pg;
  updatePageTitle(pg);
  document.getElementById('app').classList.remove('sb-open');
  const loaders = {overview:refreshOverview, links:loadLinks, clientmgr:loadClientManager, categories:loadCategories, subgroups:loadSubGroups, nodes:loadNodesPage,
    plans:loadPlans, reports:loadReports, admins:()=>{loadAdmins();loadAdminRequests();}, activity:loadActivity, messages:loadMessages, settings:()=>{loadSettings();loadDiagnostics();}};
  if(loaders[pg]) loaders[pg]();
}

// ============================================================
// Drawer
// ============================================================
function openDrawer(title, bodyHtml, footHtml){
  $('drTitle').textContent = title;
  $('drBody').innerHTML = bodyHtml;
  $('drFoot').innerHTML = footHtml;
  $('overlay').classList.add('show');
  $('drawer').classList.add('show');
}
function closeDrawer(){
  $('overlay').classList.remove('show');
  $('drawer').classList.remove('show');
}

// ============================================================
// Appearance Studio
// ============================================================
const APPEARANCE_DEFAULTS={font:'Vazirmatn',theme:'dark',accent:'purple',density:'comfortable',motion:true,wide:false,radius:'soft',glow:true,fontSize:'normal'};
const ACCENTS={purple:['#7F56D9','#6941C6'],blue:['#3b82f6','#1d4ed8'],cyan:['#06b6d4','#0e7490'],green:['#10b981','#047857'],orange:['#f59e0b','#b45309'],pink:['#ec4899','#be185d'],red:['#ef4444','#b91c1c'],indigo:['#2563eb','#4338ca'],teal:['#14b8a6','#0f766e'],gold:['#eab308','#a16207']};
function getAppearance(){try{return {...APPEARANCE_DEFAULTS,...JSON.parse(localStorage.getItem('vw_appearance')||'{}')}}catch(e){return {...APPEARANCE_DEFAULTS}}}
function saveAppearance(a){try{localStorage.setItem('vw_appearance',JSON.stringify(a))}catch(e){} applyAppearance()}
function applyAppearance(){const a=getAppearance();const root=document.documentElement;root.style.setProperty('--font-ui',`'${a.font}',sans-serif`);const theme=a.theme==='system'?(matchMedia('(prefers-color-scheme:light)').matches?'light':'dark'):a.theme;root.setAttribute('data-theme',theme);const c=ACCENTS[a.accent]||ACCENTS.purple;root.style.setProperty('--accent',c[0]);root.style.setProperty('--accent-d',c[1]);root.style.setProperty('--ui-glow',a.glow?`0 14px 40px -18px ${c[0]}88`:'none');document.body.classList.toggle('density-compact',a.density==='compact');document.body.classList.toggle('no-motion',!a.motion);document.body.classList.toggle('wide-sidebar',!!a.wide);document.body.classList.toggle('radius-sharp',a.radius==='sharp');document.body.classList.toggle('radius-pill',a.radius==='pill');document.body.classList.toggle('font-small',a.fontSize==='small');document.body.classList.toggle('font-large',a.fontSize==='large');if($('appearanceFont'))$('appearanceFont').value=a.font;document.querySelectorAll('[data-theme-choice]').forEach(x=>x.classList.toggle('on',x.dataset.themeChoice===a.theme));document.querySelectorAll('[data-accent]').forEach(x=>x.classList.toggle('on',x.dataset.accent===a.accent));document.querySelectorAll('[data-density]').forEach(x=>x.classList.toggle('on',x.dataset.density===a.density));document.querySelectorAll('[data-radius]').forEach(x=>x.classList.toggle('on',x.dataset.radius===a.radius));document.querySelectorAll('[data-font-size]').forEach(x=>x.classList.toggle('on',x.dataset.fontSize===a.fontSize));if($('motionSwitch'))$('motionSwitch').classList.toggle('on',a.motion);if($('wideSwitch'))$('wideSwitch').classList.toggle('on',a.wide);if($('glowSwitch'))$('glowSwitch').classList.toggle('on',a.glow);updateThemeIcon()}
function setFont(v){const a=getAppearance();a.font=v;saveAppearance(a);toast('فونت پنل تغییر کرد ✓')}
function setAppearanceTheme(v){const a=getAppearance();a.theme=v;saveAppearance(a)}
function setAccent(v){const a=getAppearance();a.accent=v;saveAppearance(a)}
function setDensity(v){const a=getAppearance();a.density=v;saveAppearance(a)}
function setRadius(v){const a=getAppearance();a.radius=v;saveAppearance(a)}
function setFontSize(v){const a=getAppearance();a.fontSize=v;saveAppearance(a)}
function toggleMotion(){const a=getAppearance();a.motion=!a.motion;saveAppearance(a)}
function toggleWideSidebar(){const a=getAppearance();a.wide=!a.wide;saveAppearance(a)}
function toggleGlow(){const a=getAppearance();a.glow=!a.glow;saveAppearance(a)}
try{matchMedia('(prefers-color-scheme:light)').addEventListener('change',()=>{if(getAppearance().theme==='system')applyAppearance()})}catch(e){}
function resetAppearance(){try{localStorage.removeItem('vw_appearance');localStorage.removeItem('vw_theme')}catch(e){};applyAppearance();toast('ظاهر پنل به حالت پیش‌فرض برگشت ✓')}
applyAppearance();

// ============================================================
// Bootstrapping / current user
// ============================================================
let CATEGORIES = [];
let LINKS = [];
let PROTOCOLS = [];
let MANUAL_META = {};
let ADMIN_CACHE = [];

function toggleTheme(){
  const a=getAppearance(); a.theme=(a.theme==='light'?'dark':'light'); saveAppearance(a); toast(a.theme==='light'?'پوسته روشن و کاملاً سفید فعال شد ✓':'پوسته تیره فعال شد ✓');
}
function updateThemeIcon(){
  const btn = document.getElementById('themeToggle');
  if(!btn) return;
  const cur = document.documentElement.getAttribute('data-theme') || 'dark';
  btn.innerHTML = cur === 'light' ? '<i class="ti ti-sun"></i>' : '<i class="ti ti-moon"></i>';
}
updateThemeIcon();

function toggleSidebar(){
  document.getElementById('app').classList.toggle('sb-open');
}

var DASH_I18N = {
  fa: {
    dir:'rtl', brand:'FaultPass',
    nav_overview:'داشبورد', nav_links:'اینباندها', nav_clientmgr:'ساخت کلاینت', nav_categories:'دسته‌بندی‌ها', nav_subgroups:'گروه‌های ساب',
    nav_plans:'پلن‌های فروش', nav_reports:'گزارش‌ها', nav_admins:'ادمین‌ها', nav_activity:'فعالیت‌ها', nav_messages:'پیام‌ها', nav_settings:'تنظیمات', nav_nodes:'نودها', pt_nodes:'اتصال چند پنل FaultPass و مدیریت همه از یک پنل',
    pt_overview:'وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات فروش',
    pt_links:'مدیریت حرفه‌ای اینباندها، کلاینت‌ها و لینک‌های اشتراک',
    pt_clientmgr:'ساخت کلاینت واقعی از روی اینباند دلخواه، جدا از صفحه اینباندها',
    pt_categories:'پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ',
    pt_subgroups:'ترکیب چند کانفیگ در یک لینک اشتراک واحد',
    pt_plans:'پلن‌هایی که در ربات فروش تلگرام نمایش داده می‌شوند',
    pt_reports:'خلاصه‌ی عملکرد فروش و کانفیگ‌ها',
    pt_admins:'حساب‌های دسترسی جانبی به پنل (فقط مالک)',
    pt_activity:'۱۵۰ رویداد اخیر پنل',
    pt_messages:'مرکز خطاها، هشدارها و پیام‌های سیستم',
    pt_settings:'آدرس عمومی پنل، ربات فروش تلگرام و رمز عبور'
  },
  en: {
    dir:'ltr', brand:'FaultPass',
    nav_overview:'Overview', nav_links:'Inbounds', nav_clientmgr:'Create Client', nav_categories:'Categories', nav_subgroups:'Sub Groups',
    nav_plans:'Sale Plans', nav_reports:'Reports', nav_admins:'Admins', nav_activity:'Activity', nav_messages:'Messages', nav_settings:'Settings', nav_nodes:'Nodes', pt_nodes:'Connect several FaultPass panels and manage them from one',
    pt_overview:'Live status of the service, configs and sales bot',
    pt_links:'Manage inbounds, clients and subscription links',
    pt_clientmgr:'Create a real client from any inbound, separate from the inbounds page',
    pt_categories:'Default traffic, expiry and IP-limit presets for config groups',
    pt_subgroups:'Combine several configs into one subscription link',
    pt_plans:'Plans shown in the Telegram sales bot',
    pt_reports:'Summary of sales and config performance',
    pt_admins:'Secondary panel access accounts (owner only)',
    pt_activity:'Last 150 panel events',
    pt_messages:'Errors, warnings and system messages',
    pt_settings:'Panel public URL, Telegram sales bot and password'
  }
};
var CURRENT_PAGE = 'overview';
const DASH_EN_TERMS = {
  // Navigation / pages
  'داشبورد':'Dashboard','اینباندها':'Inbounds','اینباند':'Inbound','دسته‌بندی‌ها':'Categories','دسته‌بندی':'Category',
  'گروه‌های ساب':'Subscription Groups','گروه ساب':'Subscription Group','گروه جدید':'New Group','پلن‌های فروش':'Sales Plans','پلن فروش':'Sales Plan','پلن جدید':'New Plan',
  'گزارش‌ها':'Reports','ادمین‌ها':'Admins','ادمین':'Admin','ادمین جدید':'New Admin','مالک':'Owner','فعالیت‌ها':'Activity','فعالیت':'Activity','پیام‌ها':'Messages','تنظیمات':'Settings',
  'مرکز کنترل':'Control Center','مرکز پیام و خطا':'Message & Error Center','مدیریت حساب‌ها':'Admin Management','مدیریت حساب':'Admin Management',
  'تنظیمات و استودیو ظاهر':'Settings & Appearance Studio','استودیو ظاهر':'Appearance Studio',

  // Common actions / states
  'فعال':'Active','غیرفعال':'Inactive','فعال/غیرفعال':'Enable/Disable','خاموش':'Stopped','در حال اجرا':'Running','روشن':'Online','آنلاین':'Online','آفلاین':'Offline',
  'در دسترس نیست':'Unavailable','وضعیت نامشخص':'Unknown status','در حال دریافت...':'Loading...','بروزرسانی':'Refresh','بروزرسانی زنده':'Live Refresh',
  'ذخیره':'Save','ذخیره تغییرات':'Save Changes','ذخیره آدرس':'Save URL','ذخیره شبکه':'Save Network','ذخیره متن‌های ربات':'Save Bot Texts','حذف':'Delete','ویرایش':'Edit','ساخت':'Create','ساخت سریع':'Quick Create','لغو':'Cancel','تأیید':'Confirm','انصراف':'Cancel','بازگشت':'Back','نمایش':'View','کپی':'Copy','کپی لینک':'Copy Link','کپی لینک ساب':'Copy Subscription Link','دریافت فایل':'Download','خروجی CSV':'CSV Export','جستجو':'Search','فیلتر':'Filter','همه':'All','پاک‌کردن خطاها':'Clear Errors','لغو نشست‌های قبلی':'Revoke Previous Sessions',
  'شروع':'Start','توقف':'Stop','فعال‌سازی':'Enable','غیرفعال‌سازی':'Disable','عملیات':'Actions','کنترل':'Control','جزئیات':'Details','بستن':'Close','بارگذاری کامل رابط':'Hard Reload','بازنشانی ظاهر':'Reset Appearance','بارگذاری دوباره':'Reload',

  // Titles / descriptions
  'وضعیت لحظه‌ای سرویس، کانفیگ‌ها و ربات فروش':'Live service, configuration and sales-bot status',
  'مدیریت حرفه‌ای اینباندها، کلاینت‌ها و لینک‌های اشتراک':'Professional inbound, client and subscription management',
  'پیش‌فرض‌های حجم، انقضا و محدودیت برای گروه‌های کانفیگ':'Traffic, expiry and limit presets for config groups',
  'ترکیب چند کانفیگ در یک لینک اشتراک واحد':'Combine multiple configs into one subscription link',
  'پلن‌هایی که در ربات فروش تلگرام نمایش داده می‌شوند':'Plans shown in the Telegram sales bot',
  'خلاصه‌ی عملکرد فروش و کانفیگ‌ها':'Sales and configuration performance',
  'حساب‌های دسترسی جانبی به پنل (فقط مالک)':'Secondary panel access accounts (owner only)',
  '۱۵۰ رویداد اخیر پنل':'Latest 150 panel events',
  'مرکز خطاها، هشدارها و پیام‌های سیستم':'Errors, warnings and system messages',
  'آدرس عمومی پنل، ربات فروش تلگرام و رمز عبور':'Panel public URL, Telegram sales bot and account security',
  'نمای لحظه‌ای منابع سرور، ترافیک، اتصال‌ها و سرویس فروش.':'Live server resources, traffic, connections and sales service.',
  'مرکز مدیریت اینباند، ساخت کلاینت و کنترل دسترسی؛ با پایش زنده هر ۵ ثانیه.':'Inbound management, client creation and access control with live monitoring every 5 seconds.',
  'تمام خطاهای سرور، خطاهای مرورگر و رویدادهای مهم اینجا جمع می‌شوند تا هیچ خطایی گم نشود.':'All server errors, browser errors and important events are collected here.',
  'ظاهر، فونت، رنگ، تراکم، زبان و تنظیمات عملیاتی پنل را از یکجا کنترل کن.':'Control appearance, font, colors, density, language and operational settings from one place.',
  'برای لینک‌های Subscription، دامنه واقعی پنل را ثابت کن. روی Railway بهتر است دامنه عمومی سرویس را اینجا قرار بدهی.':'Set the real panel domain for subscription links. On Railway, use the service public domain here.',
  'دامنه و پورت TCP عمومی Railway را اینجا مدیریت کن. Railway دامنه و پورت TCP Proxy را خودش تولید می‌کند و باید همان مقدار استفاده شود.':'Manage the public Railway TCP domain and port here. Railway generates the TCP Proxy values.',
  'تمام پیام‌های کلیدی ربات را از همین پنل ویرایش کن؛ تغییرات روی ربات در اجرای بعدی/ری‌استارت اعمال می‌شوند.':'Edit the bot messages here; changes apply on the next bot start/restart.',
  'حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.':'At least 8 characters; a mix of letters, numbers and symbols is recommended.',
  'نام کاربری جدید بدون فاصله و بین ۳ تا ۴۰ کاراکتر.':'New username without spaces, between 3 and 40 characters.',
  'ابزارهای حرفه‌ای برای شخصی‌سازی و نگهداری پنل':'Professional tools for panel personalization and maintenance',

  // Dashboard metrics
  'کل اینباندها':'Total Inbounds','مشتریان فروشگاه':'Store Customers','فروش (Stars)':'Sales (Stars)','پرمصرف‌ترین کانفیگ‌های ۷ روز اخیر':'Top configs from the last 7 days',
  'پرمصرف‌ترین کانفیگ‌ها':'Top Configs by Usage','خطاهای ثبت‌شده':'Recorded Errors','خطاهای Backend و Frontend با جزئیات مسیر و زمان':'Backend and frontend errors with route and time details',
  'رویدادهای مهم':'Important Events','آخرین فعالیت‌های پنل برای عیب‌یابی سریع':'Recent panel activity for quick troubleshooting',
  'وضعیت سیستم':'System Status','سیستم سالم است.':'System is healthy.','خطای ثبت‌شده‌ای وجود ندارد. سیستم سالم است.':'No recorded errors. System is healthy.','رویدادی وجود ندارد.':'No events found.','لاگی وجود ندارد':'No activity logs.','داده‌ای موجود نیست':'No data available.','هنوز داده‌ی مصرفی ثبت نشده':'No usage data recorded yet.','کانفیگی یافت نشد':'No configs found.','گروهی وجود ندارد':'No groups found.','پلنی وجود ندارد':'No plans found.',
  'همگام‌سازی خودکار':'Auto Sync','آخرین بروزرسانی':'Last Updated','۳۰ روز اخیر':'Last 30 days','۱۴ روز اخیر':'Last 14 days','۷ روز اخیر':'Last 7 days',
  'در حال ذخیره...':'Saving...','تغییر امن رمز':'Change Password','تغییر نام کاربری':'Change Username','نام کاربری پنل':'Panel Username','نام کاربری جدید':'New Username','رمز عبور':'Password','رمز فعلی':'Current Password','رمز جدید':'New Password','تکرار رمز جدید':'Repeat New Password','تکرار رمز عبور':'Repeat Password','امنیت حساب':'Account Security',
  'پیام خوش‌آمد':'Welcome Message','منوی مدیریت':'Admin Menu','پیام ساخت کانفیگ':'Config Created Message','پیام فروشگاه':'Store Message','پیام پرداخت موفق':'Payment Success Message',
  'آدرس عمومی پنل':'Panel Public URL','دامنه فعلی پنل':'Current panel domain','ذخیره شد':'Saved','ذخیره شد ✓':'Saved ✓','ساخته شد':'Created','حذف شد':'Deleted','بروزرسانی شد':'Updated','کپی شد':'Copied','کپی شد ✓':'Copied ✓','تنظیمات دوباره بارگذاری شد ✓':'Settings reloaded ✓','داده‌های زنده بروزرسانی شد ✓':'Live data refreshed ✓','دامنه پنل کپی شد ✓':'Panel URL copied ✓','نام کاربری با موفقیت تغییر کرد ✓':'Username changed successfully ✓','رمز عبور با موفقیت تغییر کرد ✓':'Password changed successfully ✓',

  // Tables / forms
  'نام کاربری':'Username','نام':'Name','نام گروه':'Group Name','برچسب':'Label','نقش':'Role','وضعیت':'Status','زمان':'Time','نوع':'Type','پیام':'Message','تعداد':'Count','تعداد کانفیگ':'Config Count','لینک عمومی':'Public Link',
  'پروتکل':'Protocol','آدرس':'Address','آدرس / Domain':'Address / Domain','پورت':'Port','سرعت':'Speed','حجم':'Traffic','حجم مصرفی':'Usage','حجم پیش‌فرض (GB)':'Default Traffic (GB)','انقضا':'Expiry','انقضا (روز)':'Expiry (Days)','اعتبار (روز)':'Validity (Days)','زمان دقیق انقضا':'Exact Expiry','محدودیت IP':'IP Limit','Connection Limit':'Connection Limit','تعداد کاربر':'Client Limit','تعداد خروجی':'Output Count','توضیحات':'Description','یادداشت داخلی':'Internal Note',
  'مدت':'Duration','قیمت (⭐)':'Price (⭐)','ویژه':'Featured','آخرین ورود':'Last Login','کل':'Total','روز':'Days','ساعت':'Hours','دقیقه':'Minutes','نامحدود':'Unlimited','پیش‌فرض':'Default','اختیاری':'Optional','اجباری':'Required','مصرف':'Usage','اتصال':'Connection','اتصالات':'Connections','کلاینت‌ها':'Clients','کلاینت':'Client','مشتریان':'Customers','مشتری‌ها':'Customers',
  'کپی VLESS':'Copy VLESS','اشتراک':'Subscription','مدیریت کلاینت‌های واقعی':'Real Client Manager','ساخت کلاینت واقعی':'Create Client','کنترل پنل':'Panel Control','مدیریت ربات':'Bot Management','ربات':'Bot',

  // Inbound builder
  'ساخت اینباند':'Create Inbound','ویرایش اینباند':'Edit Inbound','ساخت کلاینت':'Create Client','ویرایش کلاینت':'Edit Client','انتخاب پروتکل':'Select Protocol','پروتکل پایه':'Base Protocol','انتقال':'Transport','لایه انتقال':'Transport Layer','امنیت':'Security','تنظیمات اتصال':'Connection Settings','تنظیمات پیشرفته':'Advanced Settings','خلاصه':'Summary','قبل از ذخیره ترکیب نهایی را بررسی کن':'Review the final combination before saving',
  'ترکیب نهایی':'Final Combination','شبکه':'Network','روش رمزنگاری':'Encryption Method','رمز / Secret':'Password / Secret','کلید عمومی':'Public Key','شناسه کوتاه':'Short ID','مسیر Spider':'Spider X','تولید کلید Reality':'Generate Reality Keypair','تست پینگ':'Ping Test','در حال تست':'Testing...','ابتدا آدرس یا دامنه را وارد کنید':'Enter an address or domain first','پورت نامعتبر است':'Invalid port','اتصال برقرار نشد':'Connection failed',
  'این ترکیب آماده استفاده است.':'This combination is ready to use.','این ترکیب برای ساخت لینک و مدیریت سرویس آماده شده است.':'This combination is prepared for link and service management.','Shadowsocks به‌صورت TCP-only در این Builder ارائه می‌شود.':'Shadowsocks is provided as TCP-only in this builder.','Transport فقط مسیر انتقال است و جدا از پروتکل پایه انتخاب می‌شود.':'Transport is only the transfer layer and is selected separately from the base protocol.',
  'VLESS':'VLESS','VMess':'VMess','Trojan':'Trojan','Shadowsocks':'Shadowsocks','TCP':'TCP','WebSocket':'WebSocket','WS':'WebSocket','gRPC':'gRPC','XHTTP':'XHTTP','TLS':'TLS','Reality':'Reality','None':'None','امنیت بدون رمزنگاری':'No encryption','بدون رمزنگاری':'No encryption',

  // Settings / appearance
  'فونت رابط کاربری':'Interface Font','اندازه متن':'Text Size','تراکم پنل':'Panel Density','گوشه‌ها':'Corners','پوسته':'Theme','رنگ اصلی':'Accent Color','انیمیشن‌های پنل':'Panel Animations','سایدبار باز در دسکتاپ':'Open sidebar on desktop','نورپردازی':'Glow','Appearance Studio':'Appearance Studio','ظاهر پنل به حالت پیش‌فرض برگشت ✓':'Appearance reset ✓','فونت پنل تغییر کرد ✓':'Panel font updated ✓',
  'پوسته تاریک':'Dark Theme','پوسته روشن':'Light Theme','سیستم':'System','فونت پیش‌فرض':'Default Font','کوچک':'Small','متوسط':'Medium','بزرگ':'Large','فشرده':'Compact','راحت':'Comfortable','گرد':'Rounded','تیز':'Sharp',

  // Messages / diagnostics
  'خطا':'Error','هشدار':'Warning','اطلاعات':'Info','مرورگر':'Browser','پاک‌کردن':'Clear','مرکز خطاها':'Error Center','مرکز پیام و خطا':'Message & Error Center','خطا در پردازش اطلاعات ورود.':'Login data could not be processed.',
  'آدرس TCP ذخیره شد':'TCP address saved','آدرس ذخیره شد':'Address saved','ربات روشن شد':'Bot started','ربات خاموش شد':'Bot stopped','ربات در حال اجراست':'Bot is running','ربات خاموش است':'Bot is stopped',
  'Caps Lock فعال است':'Caps Lock is on','قدرت رمز':'Password strength','حداقل ۸ کاراکتر، ترکیب حروف بزرگ/کوچک، عدد و نماد پیشنهاد می‌شود.':'At least 8 characters; uppercase/lowercase letters, numbers and symbols are recommended.',

  // Railway / service
  'دامنه عمومی Railway وارد شد؛ برای TCP خام باید TCP Proxy فعال باشد':'Railway public domain loaded; raw TCP requires TCP Proxy.','اطلاعات TCP Proxy ریل‌وی در این سرویس پیدا نشد':'Railway TCP Proxy information was not found for this service.',
  'همه دسته‌ها':'All categories','مورد انتخاب شده':'selected','اینباند جدید':'New Inbound','دسته جدید':'New Category','وضعیت':'Status','آدرس':'Address','ترافیک':'Traffic','کلاینت / اتصال':'Client / Connection','عملیات':'Actions','نام گروه':'Group Name','تعداد کانفیگ':'Config Count','لینک عمومی':'Public Link','حجم پیش‌فرض':'Default Traffic','قیمت (⭐)':'Price (⭐)','خروجی CSV':'CSV Export','برچسب':'Label','مدیریت حساب‌ها':'Admin Management','ادمین جدید':'New Admin','نقش':'Role','آخرین ورود':'Last Login','مرکز پیام و خطا':'Message & Error Center','پاک‌کردن خطاها':'Clear Errors','خطاهای ثبت‌شده':'Recorded Errors','خطاهای Backend و Frontend با جزئیات مسیر و زمان':'Backend and frontend errors with route and time details','همه':'All','هشدار':'Warning','مرورگر':'Browser','بازنشانی ظاهر':'Reset Appearance','اندازه متن':'Text Size','تراکم پنل':'Panel Density','گوشه‌ها':'Corners','پوسته':'Theme','رنگ اصلی':'Accent Color','انیمیشن‌های پنل':'Panel Animations','سایدبار باز در دسکتاپ':'Open sidebar on desktop','Glow / نورپردازی':'Glow / Lighting','امنیت حساب':'Account Security','رمز فعلی':'Current Password','رمز جدید':'New Password','تکرار رمز جدید':'Repeat New Password','تغییر امن رمز':'Change Password','لغو نشست‌های قبلی':'Revoke Previous Sessions','توقف':'Stop','منوی مدیریت':'Admin Menu','پیام ساخت کانفیگ':'Config Created Message','پیام فروشگاه':'Store Message','پیام پرداخت موفق':'Payment Success Message','مانیتورینگ فوری منابع':'Instant resource monitoring','دریافت تنظیمات واقعی سرور':'Load real server settings','بارگذاری کامل رابط':'Hard Reload','دامنه فعلی پنل':'Current panel domain','در حال دریافت...':'Loading...','بروزرسانی':'Refresh','ساخت سریع':'Quick Create','کانفیگی یافت نشد':'No configs found','دسته‌بندی‌ها':'Categories','پلن‌های فروش':'Sales Plans','گروه‌های ساب':'Subscription Groups','ادمین‌ها':'Admins','پیام‌ها':'Messages','تنظیمات':'Settings',

  // --- Added: fill remaining gaps found across dashboard toasts, confirm()
  // dialogs, inbound builder, client manager and admin permission matrix ---
  'اینباند حذف شود؟':'inbound(s) be deleted?','این کلاینت حذف شود؟':'Delete this client?','این کانفیگ حذف شود؟':'Delete this config?','این دسته حذف شود؟':'Delete this category?','این گروه حذف شود؟':'Delete this group?','این پلن حذف شود؟':'Delete this plan?','این ادمین حذف شود؟':'Delete this admin?','همه خطاهای ثبت‌شده پاک شوند؟':'Clear all recorded errors?','همه نشست‌های قبلی این حساب لغو شوند؟':'Revoke all previous sessions for this account?','دسته‌بندی‌ای وجود ندارد':'No categories found','بروزرسانی گروهی انجام شد':'Bulk update completed','حذف گروهی انجام شد':'Bulk delete completed','کانفیگ خودکار ساخته شد':'Auto config created','اینباند بروزرسانی شد':'Inbound updated','اینباند با موفقیت ساخته شد':'Inbound created successfully','خطا در ذخیره اینباند':'Error saving inbound','خطا در دریافت اطلاعات Railway':'Error fetching Railway information','کلاینت واقعی ساخته شد ✓':'Client created ✓','متن‌های ربات ذخیره شد ✓':'Bot texts saved ✓','خطاها پاک شدند ✓':'Errors cleared ✓','ذخیره شد و ربات با تنظیمات جدید ری‌استارت شد':'Saved — the bot restarted with the new settings','ذخیره شد — برای اعمال، ربات را روشن کنید':'Saved — turn the bot on to apply the changes','کلید Reality ساخته شد. Private Key را روی نود خودتان نگه دارید.':'Reality keypair generated. Keep the private key on your own node.','پورت باید بین 1 تا 65535 باشد':'Port must be between 1 and 65535','Shadowsocks فقط با TCP ساخته می‌شود':'Shadowsocks can only be created over TCP','رمز جدید باید حداقل ۸ کاراکتر باشد':'New password must be at least 8 characters','رمز جدید باید با رمز فعلی متفاوت باشد':'New password must be different from the current password','تکرار رمز یکسان نیست':'Password confirmation does not match','همه‌ی فیلدهای رمز عبور را پر کنید':'Please fill in all password fields','نام کاربری باید ۳ تا ۴۰ کاراکتر و بدون فاصله باشد':'Username must be 3–40 characters with no spaces','نام کاربری را وارد کنید':'Please enter a username','هر کلاینت UUID مستقل دارد و برای پروتکل‌های Live مستقیماً توسط Relay قابل احراز است.':'Each client has its own UUID and, for Live protocols, is authenticated directly by the relay.','این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.':'This inbound currently only generates links. For a real client, first choose a Live combination such as VLESS + WS/TCP/XHTTP.','مدیریت کلاینت‌ها':'Manage Clients','حجم (GB، خالی = والد)':'Traffic (GB, empty = parent)','انقضا (روز، 0 = والد)':'Expiry (days, 0 = parent)','بدون تغییر خالی بگذار':'Leave empty for no change','والد':'parent','ساخت اینباند حرفه‌ای':'Create Professional Inbound','پروتکل پایه، ترنسپورت و امنیت کاملاً تفکیک‌شده':'Base protocol, transport and security are fully separated','اول مشخص کن با چه پروتکلی کانفیگ ساخته شود':'First decide which protocol the config will use','حالا مسیر انتقال را جداگانه انتخاب کن':'Now choose the transport layer separately','TLS / Reality / None را مستقل از ترنسپورت انتخاب کن':'Choose TLS / Reality / None independently of the transport','فقط فیلدهای مرتبط با انتخاب بالا نمایش داده می‌شوند':'Only fields relevant to the selection above are shown','لینک اشتراک':'Subscription Link','اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.':'If this link doesn\'t open for the customer, first set the panel\'s public URL correctly under the “Settings” tab.','دسته':'Category','گروه ساب جدید':'New Subscription Group','پلن':'Plan','پیشنهاد ویژه':'Featured offer','در حال اتصال':'Connecting','غیرفعال/منقضی':'Disabled/Expired','فعال - بدون اتصال':'Active – No connection','منقضی شده':'Expired','روز مانده':'days left','بدون انقضا':'No expiry','اتصال زنده':'Live connections','کل کانفیگ‌ها':'Total Configs','تعداد سفارش':'Order Count','ساخت و مدیریت اینباند':'Create & manage inbounds','سابسکریپشن':'Subscription','پیام‌ها و خطاها':'Messages & Errors','اینباند و کلاینت':'Inbounds & Clients','هشدارهای اخیر':'Recent Warnings','خطاهای مرورگر':'Browser Errors','خطای نامشخص':'Unknown error','سرور TCP روی پورت داخلی':'TCP server on internal port','گوش می‌دهد — این را در Railway به همین پورت داخلی متصل کن، نه به':'is listening — in Railway, point this at the same internal port, not at the main HTTP','مثلاً':'e.g.','اصلی':'main','همه‌ی اینباندها بروزرسانی شدند ✓':'All inbounds refreshed ✓','بروزرسانی همه':'Refresh All','الگوی نام کانفیگ‌های ساب ذخیره شد ✓':'Subscription remark template saved ✓','نام کانفیگ':'Config Name','حجم اختصاص‌یافته':'Assigned Traffic','شناسه کانفیگ (ID)':'Config ID','نام اینباند':'Inbound Name','پیش‌نمایش: ':'Preview: ','همان یک لینک ساب که به کاربر می‌دهی؛ فقط تعیین کن نام کانفیگ داخل اپ او دقیقاً چه چیزهایی را نشان دهد.':'It\'s still the same single subscription link you hand out — just choose exactly what shows in the config name inside their app.','ذخیره الگوی ساب':'Save Template','Subscription Template':'Subscription Template'
};

// ============================================================
// Stable dashboard language engine
// ============================================================
// The dashboard contains both static DOM and HTML that is created later by
// drawers, tables, API responses and toast messages.  Translation therefore
// uses one stateful engine for the whole dashboard document (not only #app).
// Each text node/attribute remembers its Persian source and its last rendered
// value.  This prevents EN -> FA loss and also lets dynamically updated nodes
// refresh correctly while English mode is active.
const DASH_NODE_STATE = new WeakMap();
const DASH_ATTR_STATE = new WeakMap();
const DASH_TERM_LIST = Object.keys(DASH_EN_TERMS).sort((a,b)=>b.length-a.length);
const DASH_TRANSLATABLE_ATTRS = ['placeholder','title','aria-label'];
let DASH_TRANSLATING = false;

// Word-safe substring replace: a term is only replaced when the character
// right before/after it is NOT another Persian letter. Without this guard a
// short dictionary entry like 'کل' ("total") would also match *inside* an
// unrelated word such as 'کلید' ("key") -> 'Totalید', silently corrupting
// text that has nothing to do with the term. Persian suffixes attached with
// a ZWNJ (e.g. 'کلاینت‌ها') still match correctly because \u200c is not a
// Persian letter and is left outside this guard.
const DASH_FA_LETTER_RE = /[\u0600-\u06FF]/;
function dashReplaceTermSafely(out, term, replacement){
  if(!out.includes(term)) return out;
  let result = '';
  let i = 0;
  const len = term.length;
  while(i < out.length){
    if(out.startsWith(term, i)){
      const before = i > 0 ? out[i - 1] : '';
      const after = out[i + len] || '';
      if(!DASH_FA_LETTER_RE.test(before) && !DASH_FA_LETTER_RE.test(after)){
        result += replacement;
        i += len;
        continue;
      }
    }
    result += out[i];
    i++;
  }
  return result;
}

function dashTranslateValue(value, lang){
  if(lang !== 'en' || !value) return value || '';
  let out = String(value);
  for(const term of DASH_TERM_LIST){
    out = dashReplaceTermSafely(out, term, DASH_EN_TERMS[term]);
  }
  return out;
}

// Shorthand for one-off strings that never live in the DOM long enough for
// the tree-walker/observer to reach them — native confirm()/prompt() dialogs
// in particular. Translates against the current dashboard language.
function t(fa){
  return dashTranslateValue(fa, typeof getDashLang === 'function' ? getDashLang() : 'fa');
}

function dashShouldTranslateElement(el){
  if(!el) return false;
  if(/^(SCRIPT|STYLE|NOSCRIPT)$/i.test(el.tagName)) return false;
  if(el.closest('[data-no-translate],.mono,[data-i18n]')) return false;
  return true;
}

function dashRenderTextNode(textNode, lang){
  if(!textNode || !textNode.parentElement || !dashShouldTranslateElement(textNode.parentElement)) return;
  const current = textNode.nodeValue || '';
  let state = DASH_NODE_STATE.get(textNode);
  if(!state){
    state = {fa: current, last: current};
    DASH_NODE_STATE.set(textNode, state);
  }else if(current !== state.last){
    // The node was changed by application code. Treat the new value as the
    // canonical Persian source rather than translating an old snapshot.
    state.fa = current;
  }
  const next = lang === 'en' ? dashTranslateValue(state.fa,'en') : state.fa;
  state.last = next;
  if(current !== next) textNode.nodeValue = next;
}

function dashRenderAttr(el, attr, lang){
  if(!el || el.matches('[data-no-translate],.mono,[data-i18n]')) return;
  if(!el.hasAttribute(attr)) return;
  const current = el.getAttribute(attr) || '';
  let attrs = DASH_ATTR_STATE.get(el);
  if(!attrs){ attrs = {}; DASH_ATTR_STATE.set(el, attrs); }
  let state = attrs[attr];
  if(!state){
    state = {fa: current, last: current};
    attrs[attr] = state;
  }else if(current !== state.last){
    state.fa = current;
  }
  const next = lang === 'en' ? dashTranslateValue(state.fa,'en') : state.fa;
  state.last = next;
  if(current !== next) el.setAttribute(attr,next);
}

function translateDashTree(lang){
  const root=document.body;
  if(!root || DASH_TRANSLATING) return;
  DASH_TRANSLATING = true;
  try{
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    const nodes=[];
    let node;
    while((node=walker.nextNode())) nodes.push(node);
    for(const textNode of nodes) dashRenderTextNode(textNode,lang);

    root.querySelectorAll('input,textarea,button,[aria-label],select').forEach(el=>{
      for(const attr of DASH_TRANSLATABLE_ATTRS) dashRenderAttr(el,attr,lang);
    });

    root.querySelectorAll('option').forEach(option=>dashRenderTextNode(option.firstChild || option,lang));
  }finally{
    DASH_TRANSLATING = false;
  }
}

function setDashI18nElement(el, key, lang){
  if(!el || !key) return;
  const fa = DASH_I18N.fa?.[key];
  const en = DASH_I18N.en?.[key];
  if(fa === undefined && en === undefined) return;
  if(fa !== undefined) el.dataset.vwFa = String(fa);
  if(en !== undefined) el.dataset.vwEn = String(en);
  const next = lang === 'en' ? (en ?? fa ?? '') : (fa ?? '');
  el.textContent = String(next);
}

function updatePageTitle(pg){
  const mainEl = document.getElementById('pageTitleMain');
  const subEl = document.getElementById('pageTitleSub');
  const lang = getDashLang();
  if(mainEl) setDashI18nElement(mainEl, 'nav_'+pg, lang);
  if(subEl) setDashI18nElement(subEl, 'pt_'+pg, lang);
}

function applyDashLang(lang){
  lang = lang === 'en' ? 'en' : 'fa';
  const dictionary = DASH_I18N[lang] || DASH_I18N.fa;
  document.documentElement.setAttribute('dir', dictionary.dir || (lang==='fa'?'rtl':'ltr'));
  document.documentElement.setAttribute('lang', lang);
  document.body.classList.toggle('dash-en', lang==='en');
  document.getElementById('dashLangFa')?.classList.toggle('on', lang==='fa');
  document.getElementById('dashLangEn')?.classList.toggle('on', lang==='en');

  document.querySelectorAll('#app [data-i18n]').forEach(el=>{
    setDashI18nElement(el, el.getAttribute('data-i18n'), lang);
  });
  updatePageTitle(CURRENT_PAGE);
  translateDashTree(lang);
  try{ localStorage.setItem('vw_dash_lang',lang); }catch(e){}
}

function getDashLang(){
  try{ return localStorage.getItem('vw_dash_lang') === 'en' ? 'en' : 'fa'; }
  catch(e){ return 'fa'; }
}

function setDashLang(lang){
  applyDashLang(lang);
}

let dashTranslateObserver=null;
let dashTranslateQueued=false;
function enableDashTranslation(){
  if(dashTranslateObserver) dashTranslateObserver.disconnect();
  const root=document.getElementById('app') || document.body;
  if(!root) return;
  dashTranslateObserver=new MutationObserver(mutations=>{
    if(getDashLang()!=='en' || DASH_TRANSLATING || dashTranslateQueued) return;
    let hasAdded=false;
    for(const m of mutations){
      if(m.type==='childList' && m.addedNodes && m.addedNodes.length){ hasAdded=true; break; }
    }
    if(!hasAdded) return;
    dashTranslateQueued=true;
    const run=()=>{ dashTranslateQueued=false; if(getDashLang()==='en' && !DASH_TRANSLATING) translateDashTree('en'); };
    if(window.requestIdleCallback) requestIdleCallback(run,{timeout:120});
    else requestAnimationFrame(run);
  });
  dashTranslateObserver.observe(root,{subtree:true,childList:true});
}

// Apply the saved language only after the dashboard DOM exists.
applyDashLang(getDashLang());
enableDashTranslation();


// ══════════════════════════════ نودها + پراکسی خروجی (منتقل‌شده از vodiwalker) ══════════════════════════════

// ══════════════════════════════ نودها (اتصال چند پنل) ══════════════════════════════
// این پنل هم می‌تواند «نود» باشد (توکن می‌سازد و کپی می‌کنی) و هم «اصلی» (آدرس + توکن نودها را می‌گیرد).
let NODES_LIST = [];
let NODE_TOKEN = {enabled:false, token:null, created_at:null};
let NODE_TOKEN_SHOWN = false;
let NODES_TIMER = null;

function nodeStyle(){
  if(document.getElementById('ndStyle')) return;
  const st = document.createElement('style'); st.id = 'ndStyle';
  st.textContent = `
  .nd-banner{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 18px;background:linear-gradient(90deg,rgba(245,165,36,.18),rgba(245,165,36,.06));border-bottom:1px solid rgba(245,165,36,.4);font-size:13px}
  .nd-banner b{color:var(--warn)}
  .nd-banner .btn{margin-inline-start:auto}
  .nd-switch{display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border:1px solid var(--line2);border-radius:11px;background:var(--panel2);color:var(--text);cursor:pointer;font-size:12.5px;font-weight:700;font-family:inherit}
  .nd-switch.remote{border-color:rgba(245,165,36,.6);color:var(--warn)}
  .nd-dot{width:9px;height:9px;border-radius:50%;background:var(--sub2);display:inline-block;flex:none}
  .nd-dot.on{background:var(--good);box-shadow:0 0 0 3px rgba(34,197,139,.18)}
  .nd-dot.off{background:var(--bad);box-shadow:0 0 0 3px rgba(242,73,85,.16)}
  .nd-tokenbox{display:flex;gap:8px;align-items:stretch;flex-wrap:wrap}
  .nd-tokenbox input{flex:1;min-width:220px;direction:ltr;text-align:left;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:12.5px}
  .nd-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:14px}
  .nd-step{padding:11px 13px;border:1px dashed var(--line2);border-radius:12px;font-size:12px;color:var(--sub);line-height:1.8}
  .nd-step b{color:var(--text);display:block;margin-bottom:2px}
  .nd-row{display:flex;gap:14px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:14px;background:var(--panel2);margin-bottom:10px;flex-wrap:wrap}
  .nd-main{flex:1;min-width:220px;display:flex;flex-direction:column;gap:5px}
  .nd-main b{font-size:14px;display:flex;align-items:center;gap:8px}
  .nd-main small{font-size:11.5px;color:var(--sub)}
  .nd-metrics{display:flex;gap:8px;flex-wrap:wrap}
  .nd-m{padding:6px 10px;border-radius:10px;background:var(--panel);border:1px solid var(--line);font-size:11px;color:var(--sub);display:flex;flex-direction:column;gap:1px;min-width:74px}
  .nd-m b{font-size:13px;color:var(--text)}
  .nd-acts{display:flex;gap:6px;flex-wrap:wrap}
  .nd-err{color:var(--bad)!important}
  `;
  document.head.appendChild(st);
}
nodeStyle();

const fmtUptime = s => { s = Number(s)||0; const d=Math.floor(s/86400), h=Math.floor(s%86400/3600), m=Math.floor(s%3600/60); return d?`${d}d ${h}h`:(h?`${h}h ${m}m`:`${m}m`); };
function nodeCopy(text, okMsg){
  const done = ()=>toast(okMsg || 'کپی شد ✓');
  if(navigator.clipboard && window.isSecureContext){ navigator.clipboard.writeText(text).then(done, ()=>nodeFallbackCopy(text, done)); }
  else nodeFallbackCopy(text, done);
}
function nodeFallbackCopy(text, done){
  const t = document.createElement('textarea'); t.value = text; t.style.position='fixed'; t.style.opacity='0'; document.body.appendChild(t); t.select();
  try{ document.execCommand('copy'); done(); }catch(e){ toast('کپی نشد؛ دستی انتخاب و کپی کن', false); }
  t.remove();
}

// ───────────── توکن این پنل (وقتی این پنل نود است) ─────────────
async function loadNodeToken(){
  try{ NODE_TOKEN = await api('/api/node/token'); }catch(e){ NODE_TOKEN = {enabled:false, token:null}; }
  renderNodeToken();
}
function renderNodeToken(){
  const box = document.getElementById('nodeTokenBody'); if(!box) return;
  const origin = location.origin;
  if(!NODE_TOKEN.enabled){
    box.innerHTML = `<p class="muted" style="margin-bottom:12px">این پنل فعلاً به‌عنوان «نود» قابل‌اتصال نیست. برای اینکه پنل اصلی بتواند این پنل را مدیریت کند، یک توکن بساز.</p>
      <button class="btn primary" onclick="createNodeToken()"><i class="ti ti-key"></i> ساخت توکن نود</button>`;
    return;
  }
  const tok = NODE_TOKEN.token || '';
  box.innerHTML = `
    <div class="grp"><label>آدرس این پنل</label><div class="nd-tokenbox"><input readonly id="ndOrigin" value="${escapeHtml(origin)}"><button class="btn" onclick="nodeCopy(document.getElementById('ndOrigin').value,'آدرس کپی شد ✓')"><i class="ti ti-copy"></i> کپی</button></div></div>
    <div class="grp" style="margin-top:10px"><label>توکن API نود</label><div class="nd-tokenbox">
      <input readonly id="ndToken" type="${NODE_TOKEN_SHOWN?'text':'password'}" value="${escapeHtml(tok)}">
      <button class="btn" onclick="toggleNodeToken()"><i class="ti ${NODE_TOKEN_SHOWN?'ti-eye-off':'ti-eye'}"></i></button>
      <button class="btn primary" onclick="nodeCopy(NODE_TOKEN.token,'توکن کپی شد ✓')"><i class="ti ti-copy"></i> کپی توکن</button>
    </div></div>
    <div class="nd-steps">
      <div class="nd-step"><b>۱) کپی</b>آدرس و توکن بالا را کپی کن.</div>
      <div class="nd-step"><b>۲) پنل اصلی</b>در پنل اصلی برو به «نودها» ← «افزودن نود».</div>
      <div class="nd-step"><b>۳) پیست</b>آدرس و توکن را بچسبان و «تست اتصال» را بزن.</div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px">
      <button class="btn sm" onclick="createNodeToken(true)"><i class="ti ti-refresh"></i> ساخت مجدد (توکن قبلی باطل می‌شود)</button>
      <button class="btn sm danger" onclick="disableNodeToken()"><i class="ti ti-lock"></i> غیرفعال‌سازی</button>
    </div>
    <p class="hint" style="margin-top:10px">این توکن فقط به بخش‌های عملیاتی (اینباند، پراکسی، ساب، آمار) دسترسی می‌دهد؛ رمز، ادمین‌ها و تنظیمات را باز نمی‌کند. مثل رمز نگهش دار.${NODE_TOKEN.created_at?` · ساخته‌شده: ${escapeHtml(String(NODE_TOKEN.created_at).slice(0,16).replace('T',' '))}`:''}</p>`;
}
function toggleNodeToken(){ NODE_TOKEN_SHOWN = !NODE_TOKEN_SHOWN; renderNodeToken(); }
async function createNodeToken(regen){
  if(regen && !confirm('توکن قبلی همین الان باطل می‌شود و پنل‌های اصلی که با آن وصل‌اند قطع می‌شوند. ادامه بدهم؟')) return;
  try{ NODE_TOKEN = await api('/api/node/token', {method:'POST'}); NODE_TOKEN_SHOWN = true; renderNodeToken(); toast(regen ? 'توکن جدید ساخته شد ✓' : 'توکن ساخته شد ✓'); }
  catch(e){ toast(e.message, false); }
}
async function disableNodeToken(){
  if(!confirm('با غیرفعال‌سازی، هیچ پنل اصلی‌ای دیگر به این پنل دسترسی ندارد. ادامه بدهم؟')) return;
  try{ NODE_TOKEN = await api('/api/node/token', {method:'DELETE'}); NODE_TOKEN_SHOWN = false; renderNodeToken(); toast('توکن نود غیرفعال شد'); }
  catch(e){ toast(e.message, false); }
}

// ───────────── لیست نودها (وقتی این پنل اصلی است) ─────────────
async function loadNodesPage(){
  loadNodeToken();
  await loadNodes();
  clearInterval(NODES_TIMER);
  NODES_TIMER = setInterval(()=>{ if(CURRENT_PAGE==='nodes') loadNodes(); else clearInterval(NODES_TIMER); }, 30000);
}
async function loadNodes(){
  try{ const r = await api('/api/nodes'); NODES_LIST = r.nodes || []; }
  catch(e){ NODES_LIST = []; const el = document.getElementById('nodesList'); if(el) el.innerHTML = `<div class="notice danger-note">${escapeHtml(e.message)}</div>`; return; }
  renderNodes(); updateNodeSwitchBtn();
}
function nodeMetricsHtml(s){
  if(!s || !s.online) return '';
  const m = (label, val)=>`<div class="nd-m"><small>${label}</small><b>${val}</b></div>`;
  return `<div class="nd-metrics">
    ${m('پینگ', Math.round(s.latency_ms||0)+'ms')}
    ${m('اینباند', s.inbounds ?? 0)}
    ${m('کلاینت', s.clients ?? 0)}
    ${m('اتصال فعال', s.connections ?? 0)}
    ${m('ترافیک', fmtBytes(s.total_bytes||0))}
    ${s.cpu!=null?m('CPU', Math.round(s.cpu)+'%'):''}
    ${s.mem!=null?m('RAM', Math.round(s.mem)+'%'):''}
    ${m('آپتایم', fmtUptime(s.uptime_seconds))}
  </div>`;
}
function renderNodes(){
  const el = document.getElementById('nodesList'); if(!el) return;
  if(!NODES_LIST.length){ el.innerHTML = '<div class="muted" style="padding:14px">هنوز نودی اضافه نشده. روی «افزودن نود» بزن و آدرس + توکن پنل دیگر را بچسبان.</div>'; return; }
  el.innerHTML = NODES_LIST.map(n=>{
    const s = n.status || null;
    const state = !n.enabled ? '' : (s ? (s.online ? 'on' : 'off') : '');
    const label = !n.enabled ? 'غیرفعال' : (s ? (s.online ? 'آنلاین' : 'آفلاین') : 'در حال بررسی');
    const active = ACTIVE_NODE && ACTIVE_NODE.id === n.id;
    return `<div class="nd-row">
      <div class="nd-main">
        <b><span class="nd-dot ${state}"></span>${escapeHtml(n.name)} <span class="badge ${s&&s.online&&n.enabled?'green':(n.enabled&&s?'red':'gray')}">${label}</span>${active?' <span class="badge gray">در حال مدیریت</span>':''}</b>
        <small class="mono" style="direction:ltr;text-align:left">${escapeHtml(n.url)} · توکن ${escapeHtml(n.token_hint||'')}${s&&s.version?` · v${escapeHtml(s.version)}`:''}</small>
        ${s && !s.online && s.error ? `<small class="nd-err">${escapeHtml(s.error)}</small>`:''}
        ${nodeMetricsHtml(s)}
      </div>
      <div class="nd-acts">
        <button class="btn primary sm" onclick="manageNode('${n.id}')" ${(!n.enabled||!(s&&s.online))?'disabled':''}><i class="ti ti-server-cog"></i> مدیریت</button>
        <button class="btn sm" onclick="checkNodeNow('${n.id}')"><i class="ti ti-activity"></i> بررسی</button>
        <button class="btn sm" onclick="openNodeDrawer('${n.id}')"><i class="ti ti-pencil"></i></button>
        <button class="btn sm" onclick="toggleNodeEnabled('${n.id}')" title="${n.enabled?'غیرفعال‌سازی':'فعال‌سازی'}"><i class="ti ${n.enabled?'ti-player-pause':'ti-player-play'}"></i></button>
        <button class="btn sm danger" onclick="deleteNode('${n.id}')"><i class="ti ti-trash"></i></button>
      </div>
    </div>`;
  }).join('');
}
async function checkAllNodes(){
  try{ const r = await api('/api/nodes/check-all', {method:'POST'}); NODES_LIST = r.nodes||[]; renderNodes(); updateNodeSwitchBtn(); toast('وضعیت نودها به‌روز شد ✓'); }
  catch(e){ toast(e.message, false); }
}
async function checkNodeNow(id){
  try{ const r = await api(`/api/nodes/${id}/check`, {method:'POST'}); NODES_LIST = NODES_LIST.map(n=>n.id===id?r.node:n); renderNodes(); updateNodeSwitchBtn(); }
  catch(e){ toast(e.message, false); }
}
async function toggleNodeEnabled(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  try{ await api('/api/nodes', {method:'POST', body: JSON.stringify({id, name:n.name, url:n.url, enabled:!n.enabled})}); await loadNodes(); }
  catch(e){ toast(e.message, false); }
}
async function deleteNode(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  if(!confirm(`نود «${n.name}» از این پنل حذف شود؟ (خودِ سرور نود و کانفیگ‌هایش دست‌نخورده می‌مانند.)`)) return;
  try{
    await api(`/api/nodes/${id}`, {method:'DELETE'});
    if(ACTIVE_NODE && ACTIVE_NODE.id===id){ exitNodeMode(); return; }
    await loadNodes(); toast('نود حذف شد');
  }catch(e){ toast(e.message, false); }
}

// ───────────── افزودن / ویرایش نود ─────────────
function openNodeDrawer(id){
  const n = id ? NODES_LIST.find(x=>x.id===id) : null;
  openDrawer(n ? 'ویرایش نود' : 'افزودن نود', `
    <div class="grp"><label>نام نود</label><input id="ndName" value="${escapeHtml(n?n.name:'')}" placeholder="مثلاً: آلمان-۱"></div>
    <div class="grp"><label>آدرس پنل نود</label><input id="ndUrl" class="mono" style="direction:ltr;text-align:left" value="${escapeHtml(n?n.url:'')}" placeholder="https://your-node.up.railway.app" oninput="ndUrlWarn()"><div class="hint" id="ndUrlHint"></div></div>
    <div class="grp"><label>توکن API نود</label><input id="ndTok" type="password" class="mono" style="direction:ltr;text-align:left" placeholder="${n?'خالی = بدون تغییر ('+escapeHtml(n.token_hint||'')+')':'fpn_...'}" autocomplete="off"><div class="hint">از پنل نود: تب «نودها» ← «ساخت توکن نود» ← کپی.</div></div>
    <div id="ndTestResult"></div>
  `, `<button class="btn" onclick="testNodeForm('${id||''}')"><i class="ti ti-plug-connected"></i> تست اتصال</button>
      <button class="btn primary" style="flex:1" id="ndSave" onclick="saveNode('${id||''}')"><i class="ti ti-device-floppy"></i> ذخیره</button>`);
  ndUrlWarn();
}
function ndUrlWarn(){
  const v = (document.getElementById('ndUrl')?.value||'').trim().toLowerCase(); const h = document.getElementById('ndUrlHint'); if(!h) return;
  h.innerHTML = v.startsWith('http://') ? '<span class="nd-err">⚠️ با http توکن بدون رمزنگاری می‌رود؛ اگر نود روی اینترنت است حتماً https بگذار.</span>' : '';
}
function ndFormBody(id){
  return {id: id||undefined, name: (document.getElementById('ndName')?.value||'').trim(), url: (document.getElementById('ndUrl')?.value||'').trim(), token: (document.getElementById('ndTok')?.value||'').trim()};
}
async function testNodeForm(id){
  const box = document.getElementById('ndTestResult'); if(box) box.innerHTML = '<div class="ob-note">در حال تست اتصال...</div>';
  try{
    const r = (await api('/api/nodes/test', {method:'POST', body: JSON.stringify(ndFormBody(id))})).status;
    box.innerHTML = r.online
      ? `<div class="ob-note ok"><i class="ti ti-circle-check"></i> اتصال موفق · پینگ ${Math.round(r.latency_ms)}ms · نسخه ${escapeHtml(r.version||'?')} · ${r.inbounds??0} اینباند</div>`
      : `<div class="ob-note"><i class="ti ti-alert-triangle"></i> <span class="nd-err">${escapeHtml(r.error||'اتصال ناموفق')}</span></div>`;
  }catch(e){ box.innerHTML = `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`; }
}
async function saveNode(id){
  const btn = document.getElementById('ndSave'); if(btn) btn.disabled = true;
  try{
    const r = await api('/api/nodes', {method:'POST', body: JSON.stringify(ndFormBody(id))});
    closeDrawer(); await loadNodes();
    const s = r.node.status;
    toast(s && s.online ? 'نود اضافه شد و آنلاین است ✓' : 'نود ذخیره شد ولی آنلاین نیست: ' + ((s&&s.error)||''), !!(s&&s.online));
  }catch(e){ toast(e.message, false); if(btn) btn.disabled = false; }
}

// ───────────── مدیریت نود: کل پنل روی نود اجرا می‌شود ─────────────
function manageNode(id){
  const n = NODES_LIST.find(x=>x.id===id); if(!n) return;
  sessionStorage.setItem('fp_active_node', JSON.stringify({id:n.id, name:n.name, url:n.url}));
  location.reload();
}
function exitNodeMode(){
  sessionStorage.removeItem('fp_active_node');
  location.reload();
}
function initNodeMode(){
  if(!ACTIVE_NODE) return;
  ['admins','settings','nodes'].forEach(pg=>{ const t = document.querySelector(`.tab[data-pg="${pg}"]`); if(t) t.style.display='none'; });
  const b = document.getElementById('nodeBanner');
  if(b){
    b.style.display = 'flex';
    b.innerHTML = `<i class="ti ti-server-cog"></i><span>در حال مدیریت نود <b>${escapeHtml(ACTIVE_NODE.name)}</b> <span class="mono" style="direction:ltr;display:inline-block">${escapeHtml(ACTIVE_NODE.url)}</span> — همه‌ی تغییرات روی سرور آن نود اعمال می‌شود.</span><button class="btn sm" onclick="exitNodeMode()"><i class="ti ti-arrow-back-up"></i> بازگشت به این پنل</button>`;
  }
}
function updateNodeSwitchBtn(){
  const btn = document.getElementById('nodeSwitchBtn'); if(!btn) return;
  if(!ACTIVE_NODE && !NODES_LIST.length){ btn.style.display = 'none'; return; }
  btn.style.display = '';
  btn.classList.toggle('remote', !!ACTIVE_NODE);
  btn.innerHTML = `<i class="ti ${ACTIVE_NODE?'ti-server-cog':'ti-home'}"></i> ${ACTIVE_NODE?escapeHtml(ACTIVE_NODE.name):'این پنل'} <i class="ti ti-chevron-down"></i>`;
}
async function initNodeUi(){
  nodeStyle(); initNodeMode();
  try{ const r = await api('/api/nodes'); NODES_LIST = r.nodes||[]; }catch(e){ NODES_LIST = []; }
  updateNodeSwitchBtn();
}
function openNodeSwitcher(){
  ensureObStyle();
  const cur = ACTIVE_NODE ? ACTIVE_NODE.id : '';
  const rows = [`<label class="ob-row ${cur===''?'on':''}"><input type="radio" name="ndSw" value="" ${cur===''?'checked':''}><span class="ob-emoji">🏠</span><span class="ob-txt"><b>این پنل</b><small>پنل محلی (سرور فعلی)</small></span></label>`]
    .concat(NODES_LIST.map(n=>{
      const s = n.status, ok = n.enabled && s && s.online;
      return `<label class="ob-row ${cur===n.id?'on':''}" style="${ok?'':'opacity:.55'}"><input type="radio" name="ndSw" value="${n.id}" ${cur===n.id?'checked':''} ${ok?'':'disabled'}><span class="nd-dot ${ok?'on':(n.enabled?'off':'')}"></span><span class="ob-txt"><b>${escapeHtml(n.name)}</b><small>${ok?Math.round(s.latency_ms||0)+'ms · '+(s.inbounds??0)+' اینباند':(n.enabled?'آفلاین':'غیرفعال')}</small></span></label>`;
    })).join('');
  const ov = document.createElement('div'); ov.className = 'ob-ov';
  ov.innerHTML = `<div class="ob-box"><h3>انتخاب پنل برای مدیریت</h3><p>با انتخاب یک نود، تمام صفحات (اینباند، ساب، پراکسی، آمار) روی همان نود کار می‌کنند.</p><div class="ob-list ob-picker">${rows}</div>
    <div class="ob-foot"><button class="btn" data-a="cancel">انصراف</button><button class="btn" data-a="nodes"><i class="ti ti-server-cog"></i> صفحه‌ی نودها</button><button class="btn primary" data-a="ok"><i class="ti ti-check"></i> برو</button></div></div>`;
  const close = ()=>{ document.removeEventListener('keydown', onKey); ov.remove(); };
  const onKey = e=>{ if(e.key==='Escape') close(); };
  document.addEventListener('keydown', onKey);
  ov.addEventListener('click', e=>{
    if(e.target===ov) return close();
    const a = e.target.closest('[data-a]'); if(!a) return;
    if(a.dataset.a==='cancel') return close();
    if(a.dataset.a==='nodes'){ close(); if(ACTIVE_NODE){ sessionStorage.removeItem('fp_active_node'); location.reload(); } else gotoPage('nodes'); return; }
    const v = (ov.querySelector('input[name=ndSw]:checked')||{}).value || '';
    close();
    if(v==='') { if(ACTIVE_NODE) exitNodeMode(); } else manageNode(v);
  });
  document.body.appendChild(ov);
}


// ══════════════════════ پراکسی IP (SOCKS) — مسیر خروجی ══════════════════════
let PROXIES_CACHE = [];
let PROXIES_ERR = '';
async function loadProxies(){
  try{ const r = await api('/api/proxies'); PROXIES_CACHE = r.proxies||[]; PROXIES_ERR = ''; }
  catch(e){ PROXIES_ERR = e.message || 'خطا در دریافت لیست'; }
  renderProxiesSettings(); renderOutboundProxySelects(); refreshOutboundPickers();
}
function ensureObStyle(){
  if(document.getElementById('obStyle')) return;
  const st = document.createElement('style'); st.id = 'obStyle';
  st.textContent = `
  .ob-ov{position:fixed;inset:0;background:rgba(4,6,10,.62);backdrop-filter:blur(3px);z-index:150;display:flex;align-items:center;justify-content:center;padding:16px}
  .ob-box{width:min(460px,100%);max-height:88vh;display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line2);border-radius:18px;box-shadow:var(--shadow-md);overflow:hidden}
  .ob-box h3{font-size:15px;padding:16px 18px 4px}
  .ob-box>p{font-size:12px;color:var(--sub);padding:0 18px 12px}
  .ob-list{overflow:auto;padding:0 14px 6px;display:flex;flex-direction:column;gap:8px}
  .ob-row{display:flex;align-items:center;gap:11px;padding:11px 12px;border:1px solid var(--line);border-radius:13px;cursor:pointer;background:var(--panel2);transition:.15s}
  .ob-row:hover{border-color:var(--line2)}
  .ob-row.on{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 14%,transparent)}
  .ob-row input{accent-color:var(--accent)}
  .ob-row .ob-txt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
  .ob-row .ob-txt b{font-size:13px}
  .ob-row .ob-txt small,.ob-pmain small,.ob-item small{font-size:11px;color:var(--sub)}
  .ob-foot{display:flex;gap:8px;padding:14px 16px;border-top:1px solid var(--line);margin-top:8px}
  .ob-foot .btn{flex:1;justify-content:center}
  .ob-flagimg{width:26px;height:19px;border-radius:3px;object-fit:cover;box-shadow:0 0 0 1px rgba(255,255,255,.12);vertical-align:middle}
  .ob-emoji{font-size:20px;line-height:1}
  .ob-badge{display:inline-block;padding:3px 9px;border-radius:999px;font-size:11px;font-weight:700;background:rgba(135,146,168,.14);color:var(--sub);white-space:nowrap}
  .ob-badge.good{background:rgba(34,197,139,.14);color:var(--good)}
  .ob-badge.warn{background:rgba(245,165,36,.14);color:var(--warn)}
  .ob-badge.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .ob-prow{display:flex;align-items:center;gap:12px;padding:12px;border:1px solid var(--line);border-radius:13px;margin-bottom:9px;background:var(--panel2);flex-wrap:wrap}
  .ob-pflag{width:30px;text-align:center}
  .ob-pmain{flex:1;min-width:180px;display:flex;flex-direction:column;gap:3px}
  .ob-pmain b{font-size:13px}
  .ob-pping{display:flex;flex-direction:column;align-items:center;gap:3px;min-width:78px}
  .ob-pping small{font-size:10px;color:var(--sub2)}
  .ob-ok{color:var(--good)!important}.ob-bad{color:var(--bad)!important}
  .ib-ob-tag{display:inline-flex;align-items:center;gap:5px}
  .ib-ob-tag .ob-flagimg{width:16px;height:12px}
  .ob-note{padding:10px 12px;border-radius:11px;background:var(--panel2);border:1px solid var(--line);font-size:12px;margin:10px 0;display:flex;align-items:center;gap:8px}
  .ob-note.ok{border-color:rgba(34,197,139,.35)}
  .ob-items{display:flex;flex-direction:column;gap:6px;margin:8px 0}
  .ob-item{padding:9px 12px;border:1px solid var(--line);border-radius:10px;display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12px}
  .ob-box.wide{width:min(640px,100%)}
  .ob-mgr-body{overflow:auto;padding:0 18px 4px}
  .ob-hint{margin:8px 16px 0;padding:9px 12px;border-radius:10px;background:var(--panel2);border:1px solid var(--line);font-size:11.5px;color:var(--sub);display:flex;gap:6px;align-items:flex-start}
  .ob-picker{display:flex;flex-direction:column;gap:8px;margin:8px 0}
  .ob-seg{display:flex;gap:6px;padding:4px;border:1px solid var(--line);border-radius:13px;background:var(--panel2);margin-bottom:14px}
  .ob-seg button{flex:1;padding:9px 10px;border:0;border-radius:10px;background:transparent;color:var(--sub);font-size:12.5px;font-weight:700;cursor:pointer;display:flex;gap:6px;align-items:center;justify-content:center;font-family:inherit}
  .ob-seg button.on{background:var(--accent);color:#fff}
  `;
  document.head.appendChild(st);
}
ensureObStyle();
function flagHtml(p){
  p = p || {};
  const cc = String(p.country_code||'').toLowerCase();
  const emoji = p.flag || '🏳️';
  if(!/^[a-z]{2}$/.test(cc)) return `<span class="ob-emoji">${emoji}</span>`;
  // ویندوز پرچم ایموجی رو نشون نمی‌ده، پس از تصویر پرچم استفاده می‌کنیم و اگه لود نشد ایموجی جایگزین می‌شه
  return `<img class="ob-flagimg" src="https://flagcdn.com/w40/${cc}.png" alt="${cc.toUpperCase()}" loading="lazy" onerror="this.outerHTML='<span class=&quot;ob-emoji&quot;>${emoji}</span>'">`;
}
function pingText(p){
  if(!p.tested_at) return 'تست‌نشده';
  if(!p.test_ok || p.ping_ms==null) return 'قطع';
  return `${Math.round(p.ping_ms)}ms`;
}
function pingClass(p){
  if(!p.tested_at) return '';
  if(!p.test_ok || p.ping_ms==null) return 'bad';
  return p.ping_ms < 300 ? 'good' : (p.ping_ms < 800 ? 'warn' : 'bad');
}
function proxyLabel(p){
  const flag = p.flag || '🏳️';
  return `${flag} ${p.name} — ${p.country||'?'} · ${pingText(p)}`;
}
function renderOutboundProxySelects(){
  document.querySelectorAll('[data-outbound-proxy-select]').forEach(sel=>{
    const cur = sel.value;
    sel.innerHTML = '<option value="">🚀 مستقیم (خود Railway)</option>' + PROXIES_CACHE.map(p=>`<option value="${escapeHtml(p.id)}">${escapeHtml(proxyLabel(p))}</option>`).join('');
    if([...sel.options].some(o=>o.value===cur)) sel.value = cur;
  });
}
function renderProxiesSettings(){
  const html = proxiesListHtml();
  ['proxiesListWrap','dProxiesListWrap'].forEach(id=>{ const w=document.getElementById(id); if(w) w.innerHTML = html; });
}
function proxiesListHtml(){
  if(PROXIES_ERR && !PROXIES_CACHE.length){ return `<div class="notice danger-note">لیست پراکسی‌ها از سرور گرفته نشد: ${escapeHtml(PROXIES_ERR)} — مطمئن شو outbound_proxy.py و python-socks روی سرور نصب/دیپلوی شده‌اند.</div>`; }
  if(!PROXIES_CACHE.length){ return '<div class="muted" style="padding:12px">هنوز پراکسی‌ای اضافه نشده. با فرم بالا یک SOCKS5 اضافه کن.</div>'; }
  const quick = localStorage.getItem('fp_quick_outbound_proxy') || '';
  return PROXIES_CACHE.map(p=>`
    <div class="ob-prow">
      <div class="ob-pflag">${flagHtml(p)}</div>
      <div class="ob-pmain">
        <b>${escapeHtml(p.name)}</b>
        <small class="mono" style="direction:ltr;text-align:left">${escapeHtml(String(p.scheme||'socks5').toUpperCase())} · ${escapeHtml(p.host)}:${p.port}${p.has_auth?' · 🔑':''}</small>
        <small>${p.country?escapeHtml(p.country):'کشور نامشخص'}${p.city?' · '+escapeHtml(p.city):''}${p.isp?' · '+escapeHtml(p.isp):''}${p.exit_ip?` · IP خروجی: <span class="mono">${escapeHtml(p.exit_ip)}</span>`:''}${p.tls_state==='intercepted'?' · <span class="ob-bad">TLS رهگیری‌شده ⚠</span>':''}${p.breaker_open?' · <span class="ob-bad">موقتاً قطع‌شده (circuit)</span>':''}</small>
        ${p.test_message?`<small class="${p.test_ok?'ob-ok':'ob-bad'}">${escapeHtml(p.test_message)}</small>`:''}
        ${p.in_use?`<small>${p.in_use} کانفیگ از این پراکسی استفاده می‌کنند</small>`:''}
      </div>
      <div class="ob-pping"><span class="ob-badge ${pingClass(p)}">${pingText(p)}</span><small>پینگ واقعی</small>${p.tcp_ms!=null?`<small>TCP ${Math.round(p.tcp_ms)}ms</small>`:''}${p.score!=null&&p.test_ok?`<span class="ob-badge ${scGradeClass(p.grade)}" title="امتیاز کیفیت">${p.score} · ${escapeHtml(p.grade||'')}</span>`:''}</div>
      <button class="btn sm" onclick="testProxyRow('${p.id}')"><i class="ti ti-activity"></i> تست</button>
      <button class="btn sm" onclick="setQuickProxy('${p.id}')" title="انتخاب پیش‌فرض در پنجره‌ی «ساخت سریع»" style="${quick===p.id?'border-color:var(--accent);color:var(--accent)':''}"><i class="ti ti-star"></i></button>
      <button class="btn sm danger" onclick="deleteProxyRow('${p.id}')"><i class="ti ti-trash"></i></button>
    </div>`).join('');
}
async function testProxyRow(id, silent){
  try{
    if(!silent) toast('در حال تست تونل SOCKS5 و کشور خروجی...');
    const r = await api(`/api/proxies/${id}/test`, {method:'POST'});
    await loadProxies();
    if(!silent){ const p=r.proxy||{}; toast(p.test_ok ? `${p.country||'?'} · ${Math.round(p.ping_ms)}ms ✓` : (p.test_message||'تست ناموفق'), !!p.test_ok); }
  }
  catch(e){ toast(e.message, false); }
}
async function testAllProxies(){
  if(!PROXIES_CACHE.length){ toast('پراکسی‌ای برای تست نیست', false); return; }
  toast('در حال تست همه‌ی پراکسی‌ها...');
  try{
    const r = await api('/api/proxies/scan/saved', {method:'POST', body: JSON.stringify({samples:2})});
    let j;
    do{ await scSleep(800); j = await api(`/api/proxies/scan/${r.job_id}?since=999999`); }while(j.state==='running');
    await loadProxies();
    toast(`${j.working} از ${j.total} پراکسی سالم است`, j.working>0);
  }catch(e){ toast(e.message, false); }
}
async function deleteAllProxies(){
  if(!PROXIES_CACHE.length){ toast('پراکسی‌ای برای حذف وجود ندارد', false); return; }
  const inUse = PROXIES_CACHE.filter(x=>x.in_use).length;
  const warn = inUse ? `\n\n${inUse} پراکسی در حال استفاده‌اند و همه‌ی کانفیگ‌هایشان به حالت «مستقیم» برمی‌گردند.` : '';
  if(!confirm(`همه‌ی ${PROXIES_CACHE.length} پراکسی حذف شوند؟ این کار برگشت‌پذیر نیست.` + warn)) return;
  try{
    const r = await api('/api/proxies/delete-all', {method:'POST'});
    localStorage.removeItem('fp_quick_outbound_proxy');
    await loadProxies();
    if(typeof loadLinks==='function') loadLinks();
    toast(`${r.removed} پراکسی حذف شد${r.detached?` · ${r.detached} کانفیگ به مستقیم برگشت`:''} ✓`);
  }catch(e){ toast(e.message, false); }
}
async function deleteProxyRow(id){
  const p = PROXIES_CACHE.find(x=>x.id===id);
  const warn = p && p.in_use ? `\n\n${p.in_use} کانفیگ از این پراکسی استفاده می‌کنند و به حالت «مستقیم» برمی‌گردند.` : '';
  if(!confirm('این پراکسی حذف شود؟' + warn)) return;
  try{ await api(`/api/proxies/${id}`, {method:'DELETE'}); if(localStorage.getItem('fp_quick_outbound_proxy')===id) localStorage.removeItem('fp_quick_outbound_proxy'); await loadProxies(); toast('حذف شد'); }
  catch(e){ toast(e.message, false); }
}
function setQuickProxy(id){
  localStorage.setItem('fp_quick_outbound_proxy', id);
  renderProxiesSettings();
  toast('این پراکسی در پنجره‌ی «ساخت سریع» از قبل انتخاب می‌شود ✓');
}
async function addProxyForm(prefix){
  prefix = prefix || 'px';
  const el = k => document.getElementById(prefix + k);
  const name = el('Name')?.value.trim();
  const host = el('Host')?.value.trim();
  const port = Number(el('Port')?.value || 1080);
  const username = el('User')?.value.trim();
  const password = el('Pass')?.value.trim();
  if(!host){ toast('آدرس پراکسی را وارد کنید', false); return; }
  try{
    const r = await api('/api/proxies', {method:'POST', body: JSON.stringify({name,host,port,username,password})});
    ['Name','Host','User','Pass'].forEach(k=>{ if(el(k)) el(k).value=''; }); if(el('Port')) el('Port').value='1080';
    await loadProxies();
    toast('پراکسی اضافه شد — در حال تست...');
    if(r.proxy?.id) testProxyRow(r.proxy.id);
  }catch(e){ toast(e.message, false); }
}

// پنجره‌ی انتخاب مسیر خروجی (Promise):
//   multi=false → '' (مستقیم) | id ;  multi=true → آرایه‌ای از '' / idها ;  انصراف → null
//   requireProxies=true → اگه هیچ پراکسی‌ای نیست، به‌جای پرسیدن مدیریت اوتباند رو باز می‌کنه.
async function askOutboundChoice(opts){
  opts = opts || {};
  await loadProxies();
  if(!PROXIES_CACHE.length){
    if(opts.requireProxies){ toast('هنوز پراکسی‌ای اضافه نشده؛ اول یک SOCKS5 اضافه کن', false); openOutboundManager(); return null; }
    return opts.multi ? [''] : '';
  }
  ensureObStyle();
  const cur = (Array.isArray(opts.current) ? opts.current : [opts.current || '']).filter(id=>id==='' || PROXIES_CACHE.some(p=>p.id===id));
  return new Promise(resolve=>{
    const ov = document.createElement('div'); ov.className = 'ob-ov';
    ov.innerHTML = `<div class="ob-box" role="dialog"><h3>${escapeHtml(opts.title||'مسیر خروجی')}</h3><p>${escapeHtml(opts.sub||'ترافیک از کجا خارج شود؟')}</p>
      <div class="ob-list ob-picker">${outboundPickerHtml('obChoice', !!opts.multi, cur.length ? cur : [''])}</div>
      ${opts.note?`<div class="ob-hint"><i class="ti ti-info-circle"></i> ${escapeHtml(opts.note)}</div>`:''}
      <div class="ob-foot"><button class="btn" data-a="cancel">انصراف</button><button class="btn primary" data-a="ok"><i class="ti ti-check"></i>ادامه</button></div></div>`;
    const done = v => { document.removeEventListener('keydown', onKey); ov.remove(); resolve(v); };
    const onKey = e => { if(e.key==='Escape') done(null); };
    document.addEventListener('keydown', onKey);
    ov.addEventListener('click', e=>{
      if(e.target===ov) return done(null);
      const a = e.target.closest('[data-a]'); if(!a) return;
      if(a.dataset.a==='cancel') return done(null);
      const vals = readOutboundPicker(ov, 'obChoice');
      if(!vals.length){ toast('حداقل یک گزینه را انتخاب کن', false); return; }
      done(opts.multi ? vals : vals[0]);
    });
    document.body.appendChild(ov);
  });
}

// انتخابگر خروجی (رادیو یا چندانتخابی) — هم داخل پنجره و هم داخل drawer استفاده می‌شود
function outboundPickerHtml(name, multi, selected){
  const sel = new Set(selected && selected.length ? selected : ['']);
  const type = multi ? 'checkbox' : 'radio';
  const items = [{id:'', direct:true}, ...PROXIES_CACHE];
  return items.map(x=>{
    const on = sel.has(x.id);
    const input = `<input type="${type}" name="${name}" value="${escapeHtml(x.id)}" ${on?'checked':''}>`;
    if(x.direct) return `<label class="ob-row ${on?'on':''}">${input}<span class="ob-emoji">🚀</span><span class="ob-txt"><b>مستقیم (خود Railway)</b><small>ترافیک از IP سرور Railway خارج می‌شود</small></span></label>`;
    return `<label class="ob-row ${on?'on':''}">${input}${flagHtml(x)}<span class="ob-txt"><b>${escapeHtml(x.name)}</b><small>${x.country?escapeHtml(x.country):'کشور نامشخص'}${x.exit_ip?' · '+escapeHtml(x.exit_ip):''}</small></span><span class="ob-badge ${pingClass(x)}">${pingText(x)}</span></label>`;
  }).join('');
}
function readOutboundPicker(root, name){
  return [...(root||document).querySelectorAll(`input[name="${name}"]:checked`)].map(i=>i.value);
}
function refreshOutboundPickers(){
  document.querySelectorAll('[data-ob-picker]').forEach(box=>{
    const name = box.dataset.obPicker;
    const cur = readOutboundPicker(box, name);
    box.innerHTML = outboundPickerHtml(name, box.dataset.multi==='1', cur);
  });
  if(typeof updateComboSummary==='function') updateComboSummary();
}
if(!window.__obPickerBound){
  window.__obPickerBound = true;
  document.addEventListener('change', e=>{
    const inp = e.target;
    if(!(inp && inp.matches && inp.matches('.ob-row input'))) return;
    const grp = inp.closest('.ob-picker');
    if(grp) grp.querySelectorAll('.ob-row').forEach(r=>r.classList.toggle('on', r.querySelector('input').checked));
    if(typeof updateComboSummary==='function') updateComboSummary();
  });
}

// ─────────────── مدیریت اوتباند (پنجره‌ی مستقل، از هر جا قابل‌باز شدن) ───────────────
function openOutboundManager(){
  ensureObStyle();
  if(document.getElementById('obMgr')) return;
  const ov = document.createElement('div'); ov.className = 'ob-ov'; ov.id = 'obMgr';
  ov.innerHTML = `<div class="ob-box wide" role="dialog">
    <h3><i class="ti ti-route"></i> اوتباند — پراکسی‌ها (SOCKS5 · SOCKS4 · HTTP)</h3>
    <p>هر پراکسی که اینجا اضافه کنی تست واقعی می‌شود (پینگ از داخل تونل، کشور/پرچم/ISP خروجی، امتیاز کیفیت). بعد می‌توانی هر اینباند/کلاینت را روی آن بگذاری. برای افزودن تکیِ HTTP یا SOCKS4 آدرس کامل را بنویس، مثلاً http://user:pass@1.2.3.4:8080</p>
    <div class="ob-mgr-body">
      <div class="ob-seg" style="margin-bottom:12px">
        <button type="button" id="obAddSingleBtn" class="on" onclick="setObAddMode('single')"><i class="ti ti-plus"></i> افزودن تکی</button>
        <button type="button" id="obAddScanBtn" onclick="setObAddMode('scan')"><i class="ti ti-radar-2"></i> اسکن و افزودن گروهی</button>
      </div>
      <div id="obAddSingle">
        <div class="row2"><div class="grp"><label>نام دلخواه</label><input id="dpxName" placeholder="مثلاً آلمان-۱"></div><div class="grp"><label>Host / آدرس کامل</label><input id="dpxHost" class="mono" style="direction:ltr;text-align:left" placeholder="1.2.3.4  یا  socks5://user:pass@host:1080"></div></div>
        <div class="row2"><div class="grp"><label>Port</label><input id="dpxPort" class="mono" style="direction:ltr;text-align:left" value="1080"></div><div class="grp"><label>Username (اختیاری)</label><input id="dpxUser" class="mono" style="direction:ltr;text-align:left"></div></div>
        <div class="row2"><div class="grp"><label>Password (اختیاری)</label><input id="dpxPass" type="password" class="mono" style="direction:ltr;text-align:left"></div><div class="grp" style="display:flex;align-items:flex-end"><button class="btn primary" style="width:100%" onclick="addProxyForm('dpx')"><i class="ti ti-plus"></i> افزودن و تست</button></div></div>
      </div>
      <div id="obAddScan" style="display:none">
        <p class="hint" style="margin-top:0">لیست پراکسی‌های خودت را (پیست یا لینک لیست سرویس‌دهنده‌ات) بده؛ همه موازی و زنده با تونل واقعی تست می‌شوند: پروتکل، پینگ و پایداری، کشور/شهر/ISP خروجی، رهگیری TLS و امتیاز کیفیت. پراکسی رایگان عمومی از اینترنت جمع‌آوری نمی‌کنیم و آدرس‌های داخلی/لوکال رد می‌شوند.</p>
        <div class="ob-seg" style="margin-bottom:8px">
          <button type="button" id="scanSrcTextBtn" class="on" onclick="setScanSource('text')"><i class="ti ti-clipboard-text"></i> پیست لیست</button>
          <button type="button" id="scanSrcUrlBtn" onclick="setScanSource('url')"><i class="ti ti-link"></i> از یک URL</button>
        </div>
        <div id="scanTextWrap"><textarea id="scanText" rows="4" class="mono" style="direction:ltr;text-align:left;width:100%;resize:vertical" placeholder="هر خط یک پروکسی — فرمت‌ها:&#10;1.2.3.4:1080&#10;1.2.3.4:1080:user:pass&#10;user:pass@1.2.3.4:1080&#10;socks5://user:pass@1.2.3.4:1080&#10;http://1.2.3.4:8080&#10;socks4://1.2.3.4:1080"></textarea></div>
        <div id="scanUrlWrap" style="display:none"><input id="scanUrl" class="mono" style="direction:ltr;text-align:left" placeholder="https://provider.com/my-proxy-list.txt"></div>
        <div class="sc-opts">
          <label class="sc-opt">پروتکل<select id="scanProto"><option value="socks5">SOCKS5</option><option value="auto">تشخیص خودکار</option><option value="http">HTTP (CONNECT)</option><option value="socks4">SOCKS4</option></select></label>
          <label class="sc-opt">دقت تست<select id="scanSamples"><option value="1">سریع (۱ نمونه)</option><option value="3" selected>متعادل (۳ نمونه)</option><option value="5">دقیق (۵ نمونه)</option></select></label>
          <label class="sc-opt">هم‌زمانی<select id="scanConc"><option value="20">کم (۲۰)</option><option value="40" selected>متوسط (۴۰)</option><option value="80">زیاد (۸۰)</option></select></label>
          <label class="sc-opt sc-chk"><input type="checkbox" id="scanTls" checked> بررسی رهگیری TLS</label>
          <label class="sc-opt sc-chk"><input type="checkbox" id="scanSpeed"> تست سرعت دانلود</label>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px">
          <button class="btn primary sm" id="scanBtn" onclick="runProxyScan()"><i class="ti ti-radar-2"></i> شروع اسکن</button>
          <button class="btn sm danger" id="scanCancelBtn" style="display:none" onclick="cancelProxyScan()"><i class="ti ti-player-stop"></i> لغو اسکن</button>
        </div>
        <div id="scanResultsWrap" style="margin-top:12px"></div>
      </div>
      <div class="divider"></div>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px"><b style="font-size:13px">پراکسی‌های ذخیره‌شده</b><div style="display:flex;gap:6px"><button class="btn sm" onclick="testAllProxies()"><i class="ti ti-activity"></i> تست همه</button><button class="btn sm danger" onclick="deleteAllProxies()"><i class="ti ti-trash"></i> حذف همه</button></div></div>
      <div id="dProxiesListWrap"></div>
    </div>
    <div class="ob-foot"><button class="btn" data-a="close">بستن</button></div></div>`;
  const close = () => { document.removeEventListener('keydown', onKey); ov.remove(); };
  const onKey = e => { if(e.key==='Escape') close(); };
  document.addEventListener('keydown', onKey);
  ov.addEventListener('click', e=>{ if(e.target===ov || e.target.closest('[data-a="close"]')) close(); });
  document.body.appendChild(ov);
  loadProxies();
}
function setObAddMode(mode){
  document.getElementById('obAddSingleBtn').classList.toggle('on', mode==='single');
  document.getElementById('obAddScanBtn').classList.toggle('on', mode==='scan');
  document.getElementById('obAddSingle').style.display = mode==='single' ? '' : 'none';
  document.getElementById('obAddScan').style.display = mode==='scan' ? '' : 'none';
}
function setScanSource(src){
  document.getElementById('scanSrcTextBtn').classList.toggle('on', src==='text');
  document.getElementById('scanSrcUrlBtn').classList.toggle('on', src==='url');
  document.getElementById('scanTextWrap').style.display = src==='text' ? '' : 'none';
  document.getElementById('scanUrlWrap').style.display = src==='url' ? '' : 'none';
}
/* ===== Pro proxy scanner UI (live progress via polling) ===== */
let SCAN_RESULTS = [];
let SCAN_JOB = null;
let SCAN_VIEW = [];
let SCAN_SHOWN = 0;
const SCAN_PAGE = 120;
function ensureScanStyle(){
  if(document.getElementById('scanStyle')) return;
  const st = document.createElement('style'); st.id = 'scanStyle';
  st.textContent = `
  .sc-opts{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin:8px 0}
  .sc-opt{display:flex;flex-direction:column;gap:5px;font-size:11px;color:var(--sub2);font-weight:700}
  .sc-opt select{padding:8px 10px;border-radius:10px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font:inherit;font-size:12px}
  .sc-chk{flex-direction:row;align-items:center;gap:8px;padding:8px 10px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);cursor:pointer;color:var(--text)}
  .sc-chk input{accent-color:var(--accent)}
  .sc-live{border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--panel2)}
  .sc-head{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;margin-bottom:8px}
  .sc-head span{color:var(--sub2);font-size:11px;direction:ltr}
  .sc-bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden}
  .sc-bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,#6366f1,#22d3ee);transition:width .35s}
  .sc-bar.done i{background:linear-gradient(90deg,#22c58b,#34d399)}
  .sc-stats{display:flex;gap:14px;flex-wrap:wrap;margin-top:10px;font-size:11.5px;color:var(--sub2)}
  .sc-stats b{font-variant-numeric:tabular-nums;color:var(--text)}
  .sc-stats .good b{color:var(--good)}.sc-stats .bad b{color:var(--bad)}.sc-stats .warn b{color:var(--warn)}
  .sc-ticker{margin-top:10px;display:flex;flex-direction:column;gap:4px;max-height:132px;overflow:hidden}
  .sc-tick{display:flex;align-items:center;gap:8px;font-size:11.5px;padding:5px 8px;border-radius:9px;background:rgba(52,211,153,.07)}
  .sc-tick .mono{direction:ltr;unicode-bidi:isolate}
  .sc-tick em{margin-inline-start:auto;font-style:normal;color:var(--good);font-weight:800}
  .sc-tools{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 8px;align-items:center}
  .sc-tools select{padding:6px 9px;border-radius:9px;border:1px solid var(--line);background:var(--panel2);color:var(--text);font:inherit;font-size:11.5px}
  .sc-row{align-items:flex-start!important}
  .sc-tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:3px}
  .sc-tags em{font-style:normal;font-size:9.5px;font-weight:800;padding:1px 7px;border-radius:99px;background:rgba(135,146,168,.14);color:var(--sub);direction:ltr;unicode-bidi:isolate}
  .sc-tags em.good{background:rgba(34,197,139,.14);color:var(--good)}.sc-tags em.warn{background:rgba(245,165,36,.14);color:var(--warn)}.sc-tags em.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .sc-score{flex:none;min-width:44px;height:44px;border-radius:13px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900;font-size:15px;line-height:1;background:rgba(135,146,168,.14);color:var(--sub)}
  .sc-score small{font-size:9px;margin-top:3px;font-weight:800}
  .sc-score.good{background:rgba(34,197,139,.16);color:var(--good)}.sc-score.warn{background:rgba(245,165,36,.16);color:var(--warn)}.sc-score.bad{background:rgba(242,73,85,.14);color:var(--bad)}
  .ob-sc{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:800;margin-inline-start:6px}
  `;
  document.head.appendChild(st);
}
ensureScanStyle();
function scEl(id){ return document.getElementById(id); }
function scGradeClass(g){ return (g==='A'||g==='B') ? 'good' : (g==='C' ? 'warn' : 'bad'); }
function scFmtTime(s){ s = Math.round(s||0); return s>=60 ? `${Math.floor(s/60)}m ${s%60}s` : `${s}s`; }
function scSleep(ms){ return new Promise(r=>setTimeout(r,ms)); }
function scReset(){
  const btn = scEl('scanBtn'), cbtn = scEl('scanCancelBtn');
  if(btn){ btn.disabled = false; btn.innerHTML = '<i class="ti ti-radar-2"></i> شروع اسکن'; }
  if(cbtn) cbtn.style.display = 'none';
}
async function runProxyScan(){
  const isUrl = scEl('scanSrcUrlBtn').classList.contains('on');
  const body = isUrl ? {source:'url', url:(scEl('scanUrl').value||'').trim()} : {source:'text', text: scEl('scanText').value||''};
  if(isUrl && !body.url){ toast('آدرس لیست را وارد کن', false); return; }
  if(!isUrl && !body.text.trim()){ toast('لیست پروکسی را پیست کن', false); return; }
  body.protocol = scEl('scanProto').value;
  body.samples = Number(scEl('scanSamples').value) || 3;
  body.tls = scEl('scanTls').checked;
  body.speed = scEl('scanSpeed').checked;
  body.concurrency = Number(scEl('scanConc').value) || 40;
  const wrap = scEl('scanResultsWrap');
  SCAN_RESULTS = []; SCAN_VIEW = []; SCAN_SHOWN = 0;
  if(SCAN_JOB) SCAN_JOB.running = false;
  const btn = scEl('scanBtn');
  btn.disabled = true; btn.innerHTML = '<i class="ti ti-hourglass"></i> در حال شروع...';
  wrap.innerHTML = '';
  try{
    const r = await api('/api/proxies/scan/start', {method:'POST', body: JSON.stringify(body)});
    SCAN_JOB = {id:r.job_id, total:r.total, since:0, running:true, blocked:r.blocked||0, truncated:!!r.truncated};
    btn.innerHTML = '<i class="ti ti-loader-2"></i> در حال اسکن...';
    scEl('scanCancelBtn').style.display = '';
    wrap.innerHTML = `
      <div class="sc-live">
        <div class="sc-head"><b id="scTitle">در حال اسکن ${r.total} پراکسی…</b><span id="scElapsed">0s</span></div>
        <div class="sc-bar" id="scBarWrap"><i id="scBar"></i></div>
        <div class="sc-stats"><span>بررسی‌شده <b id="scDone">0</b>/<b>${r.total}</b></span><span class="good">سالم <b id="scOk">0</b></span><span class="bad">ناموفق <b id="scBad">0</b></span><span class="warn">پرریسک <b id="scRisky">0</b></span></div>
        ${r.blocked?`<div class="hint" style="margin:8px 0 0">${r.blocked} آدرس داخلی/لوکال به‌دلیل امنیت رد شد.</div>`:''}
        ${r.truncated?`<div class="hint" style="margin:8px 0 0">لیست بلندتر از سقف مجاز بود؛ فقط بخش اول بررسی می‌شود.</div>`:''}
        <div class="sc-ticker" id="scTicker"></div>
      </div>
      <div id="scFinal"></div>`;
    pollScan(SCAN_JOB);
  }catch(e){
    wrap.innerHTML = `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`;
    scReset();
  }
}
async function pollScan(job){
  try{
    while(job.running){
      if(!scEl('scanResultsWrap')) return;
      const j = await api(`/api/proxies/scan/${job.id}?since=${job.since}`);
      if(!job.running) return;
      job.since = j.next;
      const fresh = [];
      for(const x of j.results){ SCAN_RESULTS[x.i] = x; if(x.ok) fresh.push(x); }
      updateScanLive(j, fresh);
      if(j.state !== 'running'){ job.running = false; finishScan(j); return; }
      await scSleep(document.hidden ? 2500 : 700);
    }
  }catch(e){
    job.running = false;
    const w = scEl('scanResultsWrap');
    if(w) w.insertAdjacentHTML('beforeend', `<div class="ob-note"><span class="nd-err">${escapeHtml(e.message)}</span></div>`);
    scReset();
  }
}
function updateScanLive(j, fresh){
  const pct = j.total ? Math.round(j.done / j.total * 100) : 0;
  const set = (id, v)=>{ const el = scEl(id); if(el) el.textContent = v; };
  const bar = scEl('scBar'); if(bar) bar.style.width = pct + '%';
  set('scDone', j.done); set('scOk', j.working); set('scBad', j.done - j.working); set('scRisky', j.risky);
  set('scElapsed', scFmtTime(j.elapsed));
  const tk = scEl('scTicker');
  if(tk && fresh.length){
    const html = fresh.slice(-5).reverse().map(x=>`<div class="sc-tick">${flagHtml(x)}<span class="mono">${escapeHtml(x.host)}:${x.port}</span><small>${escapeHtml(x.scheme.toUpperCase())}</small><em>${Math.round(x.ping_ms)}ms · ${x.score}</em></div>`).join('');
    tk.innerHTML = html + tk.innerHTML;
    while(tk.children.length > 6) tk.lastElementChild.remove();
  }
}
async function cancelProxyScan(){
  if(!SCAN_JOB) return;
  try{ await api(`/api/proxies/scan/${SCAN_JOB.id}/cancel`, {method:'POST'}); }catch(e){ toast(e.message, false); }
}
function finishScan(j){
  scReset();
  const title = scEl('scTitle'), bw = scEl('scBarWrap'), tk = scEl('scTicker');
  if(title) title.textContent = j.state === 'cancelled' ? `اسکن لغو شد — ${j.working} سالم از ${j.done} بررسی‌شده` : `اسکن تمام شد — ${j.working} سالم از ${j.total}`;
  if(bw) bw.classList.add('done');
  const bar = scEl('scBar'); if(bar && j.state !== 'cancelled') bar.style.width = '100%';
  if(tk) tk.remove();
  renderScanFinal();
}
function scFilteredView(){
  const mode = (scEl('scFilter')||{}).value || 'ok';
  const all = SCAN_RESULTS.filter(Boolean);
  let list = all;
  if(mode === 'ok') list = all.filter(x=>x.ok);
  else if(mode === 'ab') list = all.filter(x=>x.ok && (x.grade==='A'||x.grade==='B'));
  return list.sort((a,b)=> (b.ok - a.ok) || (b.score - a.score) || ((a.ping_ms??1e9) - (b.ping_ms??1e9)));
}
function scanRowHtml(x){
  const tags = [];
  if(x.ok){
    tags.push(`<em>${escapeHtml(x.scheme.toUpperCase())}</em>`);
    if(x.ping_ms != null) tags.push(`<em>${Math.round(x.ping_ms)}ms</em>`);
    if(x.jitter) tags.push(`<em>±${Math.round(x.jitter)}</em>`);
    if(x.loss) tags.push(`<em class="bad">loss ${x.loss}%</em>`);
    if(x.tls_state === 'clean') tags.push('<em class="good">TLS ✓</em>');
    else if(x.tls_state === 'intercepted') tags.push('<em class="bad">TLS رهگیری‌شده ⚠</em>');
    else if(x.tls_state === 'blocked') tags.push('<em class="warn">443 ✗</em>');
    if(x.hosting === true) tags.push('<em>Datacenter</em>');
    if(x.speed_mbps != null) tags.push(`<em>${x.speed_mbps} Mbps</em>`);
  }
  const sub = x.ok ? [x.country, x.city, x.isp].filter(Boolean).map(escapeHtml).join(' · ') || 'کشور نامشخص' : escapeHtml(x.message || 'ناموفق');
  const preset = x.ok && x.status === 'ok' && x.score >= 70;
  return `<label class="ob-row sc-row${preset?' on':''}" style="${x.ok?'':'opacity:.55'}">
      <input type="checkbox" name="scanPick" value="${x.i}" ${preset?'checked':''} ${x.ok?'':'disabled'} onchange="this.closest('.ob-row').classList.toggle('on',this.checked)">
      ${flagHtml(x)}
      <span class="ob-txt"><b class="mono" style="direction:ltr;text-align:left">${escapeHtml(x.host)}:${x.port}${x.has_auth?' 🔑':''}</b><small>${sub}</small><span class="sc-tags">${tags.join('')}</span></span>
      <span class="sc-score ${x.ok?scGradeClass(x.grade):'bad'}" title="امتیاز کیفیت">${x.ok?x.score:'—'}<small>${x.ok?escapeHtml(x.grade):''}</small></span>
    </label>`;
}
function renderScanFinal(){
  const box = scEl('scFinal'); if(!box) return;
  const all = SCAN_RESULTS.filter(Boolean);
  if(!all.length){ box.innerHTML = '<div class="sg-empty">نتیجه‌ای نیست</div>'; return; }
  const good = all.filter(x=>x.ok && (x.grade==='A'||x.grade==='B')).length;
  const keepMode = (scEl('scFilter')||{}).value || 'ok';
  box.innerHTML = `
    <div class="sc-tools">
      <select id="scFilter" onchange="renderScanList()">
        <option value="ok" ${keepMode==='ok'?'selected':''}>فقط سالم‌ها</option>
        <option value="ab" ${keepMode==='ab'?'selected':''}>فقط کیفیت A و B</option>
        <option value="all" ${keepMode==='all'?'selected':''}>همه‌ی نتیجه‌ها</option>
      </select>
      <button class="btn sm" onclick="selectGoodScan()"><i class="ti ti-sparkles"></i> انتخاب A/B</button>
      <button class="btn sm" onclick="toggleAllScanPicks()"><i class="ti ti-checks"></i> همه/هیچ</button>
      <button class="btn sm" onclick="copyScanList()"><i class="ti ti-copy"></i> کپی لیست سالم‌ها</button>
    </div>
    <div class="ob-list sg-picklist" id="scList"></div>
    <div id="scMore" style="margin-top:8px"></div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
      <button class="btn primary" style="flex:1;min-width:190px" onclick="addScannedProxies()"><i class="ti ti-plus"></i> افزودن انتخاب‌شده‌ها</button>
      <button class="btn" style="flex:1;min-width:190px" onclick="addScannedProxies(true)" ${good?'':'disabled'}><i class="ti ti-rocket"></i> افزودن همه‌ی کیفیت A/B (${good})</button>
    </div>`;
  SCAN_SHOWN = 0;
  renderScanList();
}
function renderScanList(append){
  const list = scEl('scList'); if(!list) return;
  if(!append){ SCAN_VIEW = scFilteredView(); SCAN_SHOWN = 0; list.innerHTML = ''; }
  const next = SCAN_VIEW.slice(SCAN_SHOWN, SCAN_SHOWN + SCAN_PAGE);
  if(next.length) list.insertAdjacentHTML('beforeend', next.map(scanRowHtml).join(''));
  SCAN_SHOWN += next.length;
  if(!SCAN_VIEW.length) list.innerHTML = '<div class="sg-empty">موردی با این فیلتر نیست</div>';
  const left = SCAN_VIEW.length - SCAN_SHOWN;
  const more = scEl('scMore');
  if(more) more.innerHTML = left > 0 ? `<button class="btn sm" style="width:100%" onclick="renderScanList(true)">نمایش ${Math.min(SCAN_PAGE, left)} مورد بعدی (${left} باقی‌مانده)</button>` : '';
}
function toggleAllScanPicks(){
  const boxes = [...document.querySelectorAll('input[name=scanPick]:not(:disabled)')];
  const allChecked = boxes.length > 0 && boxes.every(b=>b.checked);
  boxes.forEach(b=>{ b.checked = !allChecked; b.closest('.ob-row').classList.toggle('on', b.checked); });
}
function selectGoodScan(){
  document.querySelectorAll('input[name=scanPick]:not(:disabled)').forEach(b=>{
    const x = SCAN_RESULTS[Number(b.value)];
    b.checked = !!x && (x.grade==='A' || x.grade==='B') && x.status==='ok';
    b.closest('.ob-row').classList.toggle('on', b.checked);
  });
}
async function addScannedProxies(allGood){
  if(!SCAN_JOB) return;
  let body;
  if(allGood){ body = {min_score:70, limit:200}; }
  else{
    const idxs = [...document.querySelectorAll('input[name=scanPick]:checked')].map(i=>Number(i.value));
    if(!idxs.length){ toast('حداقل یک پراکسی سالم را انتخاب کن', false); return; }
    body = {indexes: idxs};
  }
  try{
    const r = await api(`/api/proxies/scan/${SCAN_JOB.id}/import`, {method:'POST', body: JSON.stringify(body)});
    toast(`${r.added} پراکسی اضافه شد${r.skipped?` (${r.skipped} مورد تکراری رد شد)`:''} ✓`, r.added>0);
    await loadProxies();
  }catch(e){ toast(e.message, false); }
}
async function copyScanList(){
  if(!SCAN_JOB) return;
  try{
    const r = await api(`/api/proxies/scan/${SCAN_JOB.id}/export`, {method:'POST', body: JSON.stringify({min_score:0})});
    const text = (r.lines||[]).join('\n');
    if(!text){ toast('پراکسی سالمی برای کپی نیست', false); return; }
    try{ await navigator.clipboard.writeText(text); }
    catch(_){ const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); document.execCommand('copy'); t.remove(); }
    toast(`${r.count} پراکسی کپی شد ✓`);
  }catch(e){ toast(e.message, false); }
}


// ─────────────── تغییر خروجی: تکی (دکمه‌ی روی کارت) یا گروهی (نوار انتخاب) ───────────────
async function changeOutbound(uuids){
  uuids = (uuids||[]).filter(Boolean);
  if(!uuids.length) return;
  const one = uuids.length===1 ? (LINKS.find(x=>x.uuid===uuids[0])||{}) : {};
  const cur = uuids.length===1 ? (one.outbound_proxy_ids && one.outbound_proxy_ids.length ? one.outbound_proxy_ids : [one.outbound_proxy_id || '']) : [''];
  const ids = await askOutboundChoice({
    title: uuids.length===1 ? 'خروجی‌های این اینباند' : `خروجی‌های ${uuids.length} اینباند`,
    sub: 'هر تعداد لوکیشن که بخواهی تیک بزن؛ هر کدام در لینک ساب یک کانفیگ جدا می‌شود.', current: cur, multi: true, requireProxies: true,
    note: 'مثلاً فرانسه + آلمان + هلند → کاربر در ساب برای هر لوکیشن کانفیگ جدا می‌گیرد. حجم و انقضا مشترک است. کلاینت‌های زیرمجموعه هم همین خروجی‌ها را می‌گیرند.'
  });
  if(ids===null) return;
  try{
    const r = await api('/api/links/outbound', {method:'POST', body: JSON.stringify({uuids, outbound_proxy_ids: ids})});
    toast(`${ids.length} خروجی روی ${r.updated} اینباند${r.clients?` و ${r.clients} کلاینت`:''} تنظیم شد ✓`);
    loadLinks();
  }catch(e){ toast(e.message, false); }
}
function bulkOutbound(){ changeOutbound(selectedLinkUuids()); }

// ══════════════════════ استایل‌های کمکی (muted / notice / اعضای ساب) ══════════════════════
(function(){
  if(document.getElementById('fpExtraStyle')) return;
  const st = document.createElement('style'); st.id = 'fpExtraStyle';
  st.textContent = `
  .muted{color:var(--sub)}
  .notice{padding:10px 12px;border-radius:11px;border:1px solid var(--line);background:var(--panel2);font-size:12px}
  .sg-sec{margin-bottom:14px;padding:12px;border:1px solid var(--line);border-radius:14px;background:var(--panel2)}
  .sg-sec-head{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:10px;font-size:13px}
  .sg-row{display:flex;align-items:center;gap:10px;padding:9px 10px;border:1px solid var(--line);border-radius:11px;margin-bottom:7px;background:var(--panel)}
  .sg-row .sg-txt{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}
  .sg-row .sg-txt b{font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .sg-row .sg-txt small{font-size:11px;color:var(--sub)}
  .sg-empty{padding:12px;text-align:center;color:var(--sub);font-size:12px}
  .sg-picklist{max-height:300px;overflow:auto;display:flex;flex-direction:column;gap:7px;margin:8px 0}
  .ib-ob-tag{display:inline-flex;align-items:center;gap:5px}
  `;
  document.head.appendChild(st);
})();

// ══════════════════════ اعضای گروه ساب: اینباند این پنل + اینباند نودهای دیگر ══════════════════════
let SUBS_CACHE = [];
async function openSubMembersDrawer(subId){
  ensureObStyle();
  if(!LINKS.length){ try{ await loadLinks(true); }catch(e){} }
  let sub = SUBS_CACHE.find(s=>s.sub_id===subId);
  if(!sub){ await loadSubGroups(); sub = SUBS_CACHE.find(s=>s.sub_id===subId); }
  if(!sub){ toast('گروه پیدا نشد', false); return; }
  openDrawer(`اعضای «${escapeHtml(sub.name||'')}»`, subMembersBodyHtml(sub),
    `<button class="btn" style="flex:1" onclick="copyText('${escapeHtml(sub.sub_url||'')}')"><i class="ti ti-copy"></i>کپی لینک اشتراک</button>`);
}
function subMembersBodyHtml(sub){
  const localIds = sub.link_ids || [];
  const localRows = localIds.map(uid=>{
    const l = LINKS.find(x=>x.uuid===uid);
    const ob = l && l.outbound ? `<span style="flex:none">${flagHtml(l.outbound)}</span>` : '';
    return `<div class="sg-row">${ob}<div class="sg-txt"><b>${escapeHtml(l?l.label:uid)}</b><small>${l?escapeHtml(protoLabel(l))+' · این پنل':'این پنل'}</small></div>
      <button class="btn sm danger" onclick="removeLocalSubMember('${sub.sub_id}','${uid}')"><i class="ti ti-x"></i></button></div>`;
  }).join('') || '<div class="sg-empty">هنوز اینباندی از این پنل اضافه نشده</div>';
  const remoteRows = (sub.remote_links||[]).map(e=>`
    <div class="sg-row"><span class="nd-dot ${e.node_missing?'':(e.active?'on':'off')}"></span><div class="sg-txt">
      <b>${escapeHtml(e.label||e.uuid)}</b><small>${escapeHtml(e.protocol_display||'')} · نود «${escapeHtml(e.node_name||'')}»${e.last_error?` · <span class="nd-err">${escapeHtml(e.last_error)}</span>`:''}</small></div>
      <button class="btn sm danger" onclick="removeRemoteSubMember('${sub.sub_id}','${escapeHtml(e.id)}')"><i class="ti ti-x"></i></button></div>`).join('')
    || '<div class="sg-empty">هنوز اینباندی از نود دیگر وصل نشده</div>';
  return `
    <div class="sg-sec"><div class="sg-sec-head"><b>اینباندهای این پنل (${localIds.length})</b><button class="btn sm" onclick="openAddLocalMember('${sub.sub_id}')"><i class="ti ti-plus"></i> افزودن</button></div>${localRows}</div>
    <div class="sg-sec"><div class="sg-sec-head"><b>اینباندهای روی نودهای دیگر (${(sub.remote_links||[]).length})</b><div style="display:flex;gap:6px">
      <button class="btn sm" onclick="refreshRemoteSubMembers('${sub.sub_id}')" title="بروزرسانی از نود"><i class="ti ti-refresh"></i></button>
      <button class="btn sm" onclick="openAddRemoteMember('${sub.sub_id}')"><i class="ti ti-plus"></i> افزودن از نود</button>
    </div></div>${remoteRows}</div>
    <p class="hint">یک اینباند روی این پنل + یک اینباند روی پنل دیگر (لوکیشن دیگر)، هر دو در یک لینک اشتراک.</p>`;
}
async function reopenSubMembers(subId){ await loadSubGroups(); openSubMembersDrawer(subId); }
async function removeLocalSubMember(subId, uid){
  try{ await api(`/api/subs/${subId}/links`, {method:'POST', body: JSON.stringify({link_id: uid, action:'remove'})}); toast('حذف شد'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}
async function removeRemoteSubMember(subId, refId){
  try{ await api(`/api/subs/${subId}/remote-links/${encodeURIComponent(refId)}`, {method:'DELETE'}); toast('حذف شد'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}
async function refreshRemoteSubMembers(subId){
  try{ await api(`/api/subs/${subId}/remote-links/refresh`, {method:'POST'}); toast('وضعیت نودها به‌روز شد ✓'); reopenSubMembers(subId); }
  catch(e){ toast(e.message, false); }
}
function openAddLocalMember(subId){
  const sub = SUBS_CACHE.find(s=>s.sub_id===subId); const already = new Set(sub?.link_ids||[]);
  const options = LINKS.filter(l=>!l.is_client && !already.has(l.uuid));
  const rows = options.map(l=>`<label class="ob-row"><input type="checkbox" name="addLocal" value="${escapeHtml(l.uuid)}"><span class="ob-txt"><b>${escapeHtml(l.label)}</b><small>${escapeHtml(protoLabel(l))} · پورت ${l.port||443}</small></span></label>`).join('')
    || '<div class="sg-empty">اینباند دیگری در این پنل نیست</div>';
  openDrawer('افزودن از این پنل', `<div class="ob-list ob-picker sg-picklist">${rows}</div>`,
    `<button class="btn primary" style="flex:1" onclick="submitAddLocalMembers('${subId}')" ${options.length?'':'disabled'}><i class="ti ti-plus"></i>افزودن</button>`);
}
async function submitAddLocalMembers(subId){
  const uids = [...document.querySelectorAll('input[name=addLocal]:checked')].map(i=>i.value);
  if(!uids.length){ toast('حداقل یک اینباند انتخاب کن', false); return; }
  try{
    for(const uid of uids){ await api(`/api/subs/${subId}/links`, {method:'POST', body: JSON.stringify({link_id: uid, action:'add'})}); }
    toast(`${uids.length} اینباند اضافه شد ✓`); reopenSubMembers(subId);
  }catch(e){ toast(e.message, false); }
}
async function openAddRemoteMember(subId){
  await loadNodes();
  const usable = NODES_LIST.filter(n=>n.enabled && n.status && n.status.online);
  if(!usable.length){ toast('نودی آنلاین برای انتخاب نیست؛ اول از تب «نودها» یک نود وصل کن', false); closeDrawer(); gotoPage('nodes'); return; }
  openDrawer('افزودن از نود — انتخاب نود', usable.map(n=>`<label class="ob-row"><input type="radio" name="pickNode" value="${n.id}"><span class="nd-dot on"></span><span class="ob-txt"><b>${escapeHtml(n.name)}</b><small>${escapeHtml(n.url)}</small></span></label>`).join(''),
    `<button class="btn primary" style="flex:1" onclick="loadNodeInboundsForAdd('${subId}')"><i class="ti ti-arrow-left"></i>بعدی: انتخاب اینباند</button>`);
}
async function loadNodeInboundsForAdd(subId){
  const nodeId = (document.querySelector('input[name=pickNode]:checked')||{}).value;
  if(!nodeId){ toast('یک نود انتخاب کن', false); return; }
  try{
    const r = await api(`/api/nodes/${nodeId}/inbounds`);
    const sub = SUBS_CACHE.find(s=>s.sub_id===subId);
    const already = new Set((sub?.remote_links||[]).filter(e=>e.node_id===nodeId).map(e=>e.uuid));
    const items = (r.inbounds||[]).filter(i=>!already.has(i.uuid));
    const rows = items.map(i=>`<label class="ob-row"><input type="checkbox" name="addRemote" value="${escapeHtml(i.uuid)}"><span class="ob-txt"><b>${escapeHtml(i.label)}</b><small>${escapeHtml(i.protocol_display||'')} · پورت ${i.port||443}${i.outbound?` · ${flagHtml(i.outbound)} ${escapeHtml(i.outbound.country||i.outbound.name||'')}`:''}</small></span></label>`).join('')
      || '<div class="sg-empty">این نود اینباند دیگری برای افزودن ندارد</div>';
    openDrawer(`افزودن از نود «${escapeHtml(r.node.name)}»`, `<div class="ob-list ob-picker sg-picklist">${rows}</div>`,
      `<button class="btn primary" style="flex:1" onclick="submitAddRemoteMembers('${subId}','${nodeId}')" ${items.length?'':'disabled'}><i class="ti ti-plus"></i>افزودن</button>`);
  }catch(e){ toast(e.message, false); }
}
async function submitAddRemoteMembers(subId, nodeId){
  const uuids = [...document.querySelectorAll('input[name=addRemote]:checked')].map(i=>i.value);
  if(!uuids.length){ toast('حداقل یک اینباند انتخاب کن', false); return; }
  try{
    const r = await api(`/api/subs/${subId}/remote-links`, {method:'POST', body: JSON.stringify({node_id: nodeId, uuids})});
    if(r.failed && r.failed.length) toast(`${r.added} اضافه شد، ${r.failed.length} مورد ناموفق: ${r.failed[0].error}`, r.added>0);
    else toast(`${r.added} اینباند از نود اضافه شد ✓`);
    reopenSubMembers(subId);
  }catch(e){ toast(e.message, false); }
}


// ══════════════════════ اسم‌های تزئینی (Name Studio) ══════════════════════
(function(){
  if(document.getElementById('fpNameStyle')) return;
  const st = document.createElement('style'); st.id = 'fpNameStyle';
  st.textContent = `
  .name-studio{margin-top:8px;padding:10px;border-radius:14px;border:1px dashed var(--line2);background:color-mix(in srgb,var(--accent) 7%,transparent)}
  .ns-head{display:flex;align-items:center;justify-content:space-between;gap:8px;font-size:11px;color:var(--sub);margin-bottom:8px}
  .ns-head i{color:var(--accent)}
  .ns-more{border:1px solid var(--line);background:var(--panel2);color:inherit;border-radius:10px;padding:5px 10px;font-size:11px;cursor:pointer;font-family:inherit}
  .ns-chips{display:flex;flex-wrap:wrap;gap:6px}
  .ns-chip{border:1px solid color-mix(in srgb,var(--accent) 38%,transparent);background:color-mix(in srgb,var(--accent) 12%,transparent);color:inherit;border-radius:999px;padding:6px 11px;font-size:12px;cursor:pointer;direction:ltr;font-family:inherit;transition:transform .12s,background .12s}
  .ns-chip:hover{background:color-mix(in srgb,var(--accent) 28%,transparent)}.ns-chip:active{transform:scale(.96)}
  `;
  document.head.appendChild(st);
})();
function updateBrandPreview(){
  const el = $('brandNamePreview');
  if(el) el.textContent = $('nameStyleEnabled')?.checked ? 'FaultPass | Aurora 🌠' : 'FaultPass';
}
async function saveNameStyle(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({name_style_enabled: !!$('nameStyleEnabled')?.checked})});
    toast('استایل نام‌ها ذخیره شد ✓'); loadSettings();
  }catch(e){ toast(e.message, false); }
}
const NAME_STUDIO_INPUTS = ['fLabel','clientName','cmClientName'];
document.addEventListener('focusin', e=>{ const el = e.target; if(el && NAME_STUDIO_INPUTS.includes(el.id)) attachNameStudio(el); });
function attachNameStudio(input){
  if(input.dataset.nsAttached) return; input.dataset.nsAttached = '1';
  const box = document.createElement('div'); box.className = 'name-studio';
  box.innerHTML = '<div class="ns-head"><span><i class="ti ti-sparkles"></i> اسم‌های خفن (کلیک کن)</span><button type="button" class="ns-more"><i class="ti ti-dice-5"></i> پیشنهاد جدید</button></div><div class="ns-chips"></div>';
  input.insertAdjacentElement('afterend', box);
  const chips = box.querySelector('.ns-chips');
  async function load(){
    chips.innerHTML = '<span class="muted">…</span>';
    try{
      const base = (input.value||'').split('|')[0].replace(/[^\p{L}\p{N} _-]/gu,'').trim() || 'FaultPass';
      const r = await api('/api/name-suggestions?base='+encodeURIComponent(base)+'&n=8');
      chips.innerHTML = '';
      (r.suggestions||[]).forEach(n=>{
        const b = document.createElement('button'); b.type = 'button'; b.className = 'ns-chip'; b.textContent = n;
        b.onclick = ()=>{ input.value = n; input.dispatchEvent(new Event('input',{bubbles:true})); toast('اسم انتخاب شد ✓'); };
        chips.appendChild(b);
      });
    }catch(err){ chips.innerHTML = ''; }
  }
  box.querySelector('.ns-more').onclick = load; load();
}

// ══════════════════════ ساخت هوشمند: انتخاب پروفایل آماده ══════════════════════
const AUTO_PROFILES = [
  {id:'balanced', icon:'⚖️', name:'متعادل (پیشنهادی)', desc:'۲ آی‌پی هم‌زمان · ۴ اتصال · فرگمنت امن'},
  {id:'normal',   icon:'🌐', name:'ساده',               desc:'بدون هیچ محدودیتی'},
  {id:'gaming',   icon:'🎮', name:'گیمینگ',             desc:'۱ آی‌پی · ۲ اتصال · کم‌تاخیر'},
  {id:'maximum',  icon:'🛡️', name:'حداکثر امنیت',       desc:'فینگرپرینت تصادفی · فرگمنت امن'},
];
function askAutoProfile(){
  ensureObStyle();
  return new Promise(resolve=>{
    const last = localStorage.getItem('fp_auto_profile') || 'balanced';
    const rows = AUTO_PROFILES.map(x=>`<label class="ob-row ${x.id===last?'on':''}"><input type="radio" name="autoProf" value="${x.id}" ${x.id===last?'checked':''}><span class="ob-emoji">${x.icon}</span><span class="ob-txt"><b>${x.name}</b><small>${x.desc}</small></span></label>`).join('');
    const ov = document.createElement('div'); ov.className = 'ob-ov';
    ov.innerHTML = `<div class="ob-box" role="dialog"><h3><i class="ti ti-wand"></i> ساخت هوشمند</h3><p>یک پروفایل آماده انتخاب کن؛ اسم کانفیگ هم خودکار و تزئینی ساخته می‌شود.</p>
      <div class="ob-list ob-picker">${rows}</div>
      <div class="ob-foot"><button class="btn" data-a="cancel">انصراف</button><button class="btn primary" data-a="ok"><i class="ti ti-check"></i>ادامه</button></div></div>`;
    const done = v => { document.removeEventListener('keydown', onKey); ov.remove(); resolve(v); };
    const onKey = e => { if(e.key==='Escape') done(null); };
    document.addEventListener('keydown', onKey);
    ov.addEventListener('click', e=>{
      if(e.target===ov) return done(null);
      const a = e.target.closest('[data-a]'); if(!a) return;
      if(a.dataset.a==='cancel') return done(null);
      const v = (ov.querySelector('input[name=autoProf]:checked')||{}).value || 'balanced';
      localStorage.setItem('fp_auto_profile', v); done(v);
    });
    document.body.appendChild(ov);
  });
}

async function boot(){
  try{
    const me = await api('/api/me');
    if(!me.authenticated){ location.href='/login'; return; }
    $('userName').textContent = me.admin.username;
    $('userChip').querySelector('.av').textContent = (me.admin.username||'?').slice(0,1).toUpperCase();
    if(me.admin.role !== 'owner'){
      const _nt = document.querySelector('.tab[data-pg="nodes"]'); if(_nt) _nt.style.display='none';
      document.querySelector('.tab[data-pg="admins"]').style.display='none';
      document.querySelector('.tab[data-pg="settings"]').style.display='none';
      if(!(me.admin.permissions||[]).includes('clients')){
        document.querySelector('.tab[data-pg="clientmgr"]').style.display='none';
      }
    } else {
      loadAdminRequests();
      initNodeUi();
    }
  }catch(e){ location.href='/login'; return; }
  try{ const p = await api('/api/protocols'); PROTOCOLS = p.protocols||[]; MANUAL_META = p.manual||{}; }catch(e){}
  loadProxies();
  refreshOverview();
}
boot();

// ============================================================
// OVERVIEW
// ============================================================
async function refreshOverview(){
  try{
    const [stats, linksRes] = await Promise.all([api('/stats'), api('/api/links')]);
    LINKS = linksRes.links || [];
    $('nb-links').textContent = LINKS.filter(x=>!x.is_client).length;
    $('trafficTotalVal').textContent = fmtBytes(stats.total_traffic_bytes || 0);
  }catch(e){ toast(e.message, false); }
  try{
    const s = await api('/api/settings');
    $('ovBaseUrl').textContent = s.public_base_url || s.effective_host || '—';
    const running = !!s.bot_running;
    $('ovBotStatus').className = 'badge ' + (running?'green':'red');
    $('ovBotStatus').textContent = running?'ONLINE':'OFFLINE';
    $('botStateText').textContent = running?'در حال اجرا':'خاموش';
  }catch(e){}
  try{
    const rep = await api('/api/reports/summary?days=7');
    const t = rep.totals || {};
    $('ovBizStats').innerHTML = `
      <div><i class="ti ti-network"></i><span><b>${t.links||0}</b><small>کل اینباندها</small></span></div>
      <div><i class="ti ti-circle-check"></i><span><b>${t.active_links||0}</b><small>فعال</small></span></div>
      <div><i class="ti ti-users"></i><span><b>${t.customers||0}</b><small>مشتریان فروشگاه</small></span></div>`;
    const top = (rep.top_links||[]).slice(0,6);
    if(!top.length){
      $('ovTopLinks').innerHTML = '<div class="ov-empty">هنوز داده‌ی مصرفی ثبت نشده</div>';
    }else{
      const maxUsed = Math.max(1, ...top.map(l=>l.used_bytes||0));
      $('ovTopLinks').innerHTML = top.map((l,i)=>{
        const pct = Math.round((l.used_bytes||0)/maxUsed*100);
        return `<div class="ov-toplink-row"><div class="otl-rank">${i+1}</div><div class="otl-info"><b>${escapeHtml(l.label||'—')}</b><div class="otl-bar"><i style="width:${pct}%"></i></div></div><div class="otl-val">${fmtBytes(l.used_bytes||0)}</div></div>`;
      }).join('');
    }
  }catch(e){}
  await refreshTelemetry();
}
let TEL={cpu:[],ram:[],swap:[],storage:[],traffic:[],conn:[]};
function pushSeries(arr,v,max=36){arr.push(Number(v)||0);while(arr.length>max)arr.shift();}
function drawSpark(id,arr){const el=$(id);if(!el||!arr.length)return;const max=Math.max(100, ...arr), min=Math.min(0,...arr);const pts=arr.map((v,i)=>{const x=(i/Math.max(1,arr.length-1))*240;const y=44-((v-min)/(max-min||1))*38;return `${x.toFixed(1)},${y.toFixed(1)}`}).join(' ');el.innerHTML=`<polyline points="${pts}"/>`; }
function drawChart(id,arr,maxY){const el=$(id);if(!el||!arr.length)return;const w=id==='trafficChart'?900:340,h=id==='trafficChart'?260:150;const max=maxY||Math.max(1,...arr);const pts=arr.map((v,i)=>{const x=(i/Math.max(1,arr.length-1))*w;const y=h-8-(Math.min(max,v)/max)*(h-20);return `${x.toFixed(1)},${y.toFixed(1)}`}).join(' ');const area=`0,${h} ${pts} ${w},${h}`;el.innerHTML=`<polygon class="area" points="${area}"/><polyline points="${pts}"/>`; }
async function refreshTelemetry(){
  try{const t=await api('/api/telemetry');
    $('cpuVal').textContent=t.cpu+'%'; $('cpuSub').textContent=(t.cpu_cores||1)+' logical cores';
    $('ramVal').textContent=t.ram.percent+'%'; $('ramSub').textContent=fmtBytes(t.ram.used)+' / '+fmtBytes(t.ram.total);
    $('swapVal').textContent=t.swap.percent+'%'; $('swapSub').textContent=fmtBytes(t.swap.used)+' / '+fmtBytes(t.swap.total);
    $('storageVal').textContent=t.storage.percent+'%'; $('storageSub').textContent=fmtBytes(t.storage.used)+' / '+fmtBytes(t.storage.total);
    $('txRate').textContent=fmtBytes(t.network.tx_bps)+'/s'; $('rxRate').textContent=fmtBytes(t.network.rx_bps)+'/s'; $('liveRate').textContent='↑ '+fmtBytes(t.network.tx_bps)+'/s ↓ '+fmtBytes(t.network.rx_bps)+'/s';
    $('connVal').textContent=t.connections; $('reqVal').textContent=t.requests; $('errVal').textContent=t.errors; $('uptimeVal').textContent=t.uptime; $('coresVal').textContent=t.cpu_cores; $('procRamVal').textContent=fmtBytes(t.process.rss); $('loadVal').textContent=(t.load||[]).join('  '); $('sentTotal').textContent=fmtBytes(t.network.bytes_sent); $('recvTotal').textContent=fmtBytes(t.network.bytes_recv);
    const hist=Array.isArray(t.history)?t.history:[];
    if(hist.length){
      TEL.cpu=hist.map(x=>Number(x.cpu)||0); TEL.ram=hist.map(x=>Number(x.ram)||0); TEL.swap=hist.map(x=>Number(x.swap)||0); TEL.storage=hist.map(x=>Number(x.storage)||0);
      TEL.traffic=hist.map(x=>(Number(x.tx_bps)||0)+(Number(x.rx_bps)||0)); TEL.conn=hist.map(x=>Number(x.connections)||0);
    }else{
      pushSeries(TEL.cpu,t.cpu);pushSeries(TEL.ram,t.ram.percent);pushSeries(TEL.swap,t.swap.percent);pushSeries(TEL.storage,t.storage.percent);pushSeries(TEL.traffic,(t.network.tx_bps+t.network.rx_bps));pushSeries(TEL.conn,t.connections);
    }
    drawSpark('cpuSpark',TEL.cpu);drawSpark('ramSpark',TEL.ram);drawSpark('swapSpark',TEL.swap);drawSpark('storageSpark',TEL.storage);drawChart('trafficChart',TEL.traffic);drawChart('connChart',TEL.conn);
  }catch(e){}
}
let telemetryTimer=null;
function startTelemetryLoop(){ if(telemetryTimer) clearInterval(telemetryTimer); telemetryTimer=setInterval(()=>{ if(!document.hidden) refreshTelemetry(); },8000); }
startTelemetryLoop();

function statCard(icon,color,val,label){
  return `<div class="stat-card"><div class="sc-top"><div class="sc-icon" style="background:${color}22;color:${color}"><i class="ti ${icon}"></i></div></div>
    <div class="sc-val">${val ?? 0}</div><div class="sc-label">${label}</div></div>`;
}
function protoLabel(l){
  if(l && typeof l === 'object'){
    if(l.protocol_display) return l.protocol_display;
    const found = PROTOCOLS.find(x=>x.id===l.protocol);
    return found ? found.label : (l.protocol||'—');
  }
  const found = PROTOCOLS.find(x=>x.id===l);
  return found ? found.label : (l||'—');
}
function statusBadge(l){
  if(l.expired || !l.active) return `<span class="badge red">غیرفعال/منقضی</span>`;
  if(l.status_color==='green') return `<span class="badge green">متصل</span>`;
  return `<span class="badge gray">فعال</span>`;
}

// ============================================================
// LINKS
// ============================================================
async function loadLinks(silent){
  try{
    const [linksRes, catsRes] = await Promise.all([api('/api/links'), api('/api/categories')]);
    const selectedBefore = silent ? selectedLinkUuids() : [];
    LINKS = linksRes.links || [];
    CATEGORIES = catsRes.categories || [];
    const sel = $('linkFilterCat');
    const prevCatVal = sel.value;
    sel.innerHTML = '<option value="">همه دسته‌ها</option>' + CATEGORIES.map(c=>`<option value="${c.id}">${escapeHtml(c.name)}</option>`).join('');
    sel.value = prevCatVal;
    $('nb-links').textContent = LINKS.filter(x=>!x.is_client).length;
    renderLinks();
    if(silent && selectedBefore.length){
      selectedBefore.forEach(uid=>{const c=document.querySelector(`.ib-row-check[data-uid="${uid}"]`); if(c) c.checked=true;});
      updateLinksBulkBar();
    }
    if($('ibUpdatedAt')) $('ibUpdatedAt').textContent = 'بروزرسانی ' + new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  }catch(e){ if(!silent) toast(e.message, false); }
}
let linksTimer=setInterval(()=>{if(!document.hidden && CURRENT_PAGE==='links') loadLinks(true)},12000);
async function refreshAllInbounds(){
  const btn=$('ibRefreshBtn'), icon=$('ibRefreshIcon');
  if(btn) btn.disabled=true;
  if(icon) icon.classList.add('spin');
  try{
    await loadLinks();
    await refreshOverview();
    toast('همه‌ی اینباندها بروزرسانی شدند ✓');
  }catch(e){ toast(e.message, false); }
  finally{ if(btn) btn.disabled=false; if(icon) icon.classList.remove('spin'); }
}
function renderQuickStats(list){
  const total=list.length, active=list.filter(l=>l.active && !l.expired).length, live=list.filter(l=>l.live_status==='live').length, clients=list.reduce((s,l)=>s+Number(l.client_count||0),0);
  $('ibQuickStats').innerHTML = `
    <div><i class="ti ti-network"></i><span><b>${total}</b><small>کل اینباندها</small></span></div>
    <div><i class="ti ti-circle-check"></i><span><b>${active}</b><small>فعال</small></span></div>
    <div><i class="ti ti-bolt"></i><span><b>${live}</b><small>LIVE</small></span></div>
    <div><i class="ti ti-users"></i><span><b>${clients}</b><small>کل کلاینت‌ها</small></span></div>`;
}
function ibCardHtml(l){
  const pct=l.limit_bytes>0?Math.min(100,Math.round((l.used_bytes/l.limit_bytes)*100)):0; const port=l.port||443;
  const pctClass = pct>=90?'crit':(pct>=70?'warn':'');
  const isLive = l.live_status==='live';
  const daysLeft = l.expires_at ? Math.ceil((new Date(l.expires_at).getTime()-Date.now())/86400000) : null;
  const expClass = l.expired ? 'expired' : (daysLeft!==null && daysLeft<=3 ? 'soon' : '');
  const expSub = l.expires_at ? (l.expired ? 'منقضی شده' : (daysLeft!==null ? daysLeft+' روز مانده' : '')) : 'بدون انقضا';
  return `<article class="ib-card ${l.active?'':'ib-off'}" data-uid="${l.uuid}">
    <label class="ib-card-check"><input type="checkbox" class="ib-check ib-row-check" data-uid="${l.uuid}" onchange="updateLinksBulkBar()"></label>
    <div class="ib-card-head">
      <div class="ib-avatar"><i class="ti ti-router"></i></div>
      <div class="ib-card-id">
        <div class="ib-name-top"><b title="${escapeHtml(l.label||'Unnamed Inbound')}">${escapeHtml(l.label||'Unnamed Inbound')}</b>${l.expired?'<span class="badge red">منقضی</span>':''}</div>
        <div class="mono">${escapeHtml((l.uuid||'').slice(0,18))}…</div>
      </div>
      <div class="ib-card-controls">
        <button class="ib-switch ${l.active?'on':''}" title="فعال/غیرفعال" onclick="toggleLink('${l.uuid}', ${!l.active})"></button>
        <span class="ib-status-dot ${l.status_color||'gray'}" title="${l.status_color==='green'?'در حال اتصال':(l.status_color==='red'?'غیرفعال/منقضی':'فعال - بدون اتصال')}"></span>
      </div>
    </div>
    <div class="ib-tagrow"><span>${protoLabel(l)}</span><span>${l.network||'tcp'}/${l.security||'none'}</span>${isLive?'<span class="ib-live-tag"><i></i>LIVE</span>':'<span class="ib-linkonly-tag">LINK-ONLY</span>'}<span>${escapeHtml(l.category_name||'بدون دسته')}</span>${(l.outbounds&&l.outbounds.length>1)?l.outbounds.map(o=>`<span class="ib-ob-tag" title="خروجی">${o.id?flagHtml(o):'🚀'} ${escapeHtml(o.country||o.name||'')}</span>`).join(''):(l.outbound?`<span class="ib-ob-tag" title="خروجی از طریق پراکسی">${flagHtml(l.outbound)} ${escapeHtml(l.outbound.country||l.outbound.name||'')}</span>`:'')}</div>
    <div class="ib-card-addr"><span class="mono">${escapeHtml(l.address||'0.0.0.0')}:${port}</span><small>${expSub}</small></div>
    <div class="ib-card-traffic">
      <div class="ib-tf-top"><span>مصرف</span><b>${fmtBytes(l.used_bytes||0)}${l.limit_bytes>0?' / '+fmtBytes(l.limit_bytes):' / ∞'}</b></div>
      <div class="ib-progress"><i class="${pctClass}" style="width:${pct}%"></i></div>
    </div>
    <div class="ib-card-stats">
      <div><small>کلاینت</small><b>${Number(l.client_count||0)}</b></div>
      <div><small>اتصال</small><b>${Number(l.connected_ips||0)}/${Number(l.connection_limit||0)||'∞'}</b></div>
      <div><small>انقضا</small><b class="${expClass}">${l.expires_at?escapeHtml(l.expires_at.slice(0,10)):'∞'}</b></div>
    </div>
    <div class="ib-card-foot">
      <div class="ib-clientcell"><button class="iconbtn" title="مدیریت کلاینت‌ها" onclick="openClients('${l.uuid}')"><i class="ti ti-users"></i></button><span>مدیریت کلاینت</span></div>
      <div class="ib-card-actions">
        <button class="iconbtn" title="خروجی (Outbound)" onclick="changeOutbound(['${l.uuid}'])"><i class="ti ti-route"></i></button>
        <button class="iconbtn" title="اشتراک" onclick="showSubLink('${l.uuid}')"><i class="ti ti-qrcode"></i></button>
        <button class="iconbtn" title="ویرایش" onclick="openLinkDrawer('${l.uuid}')"><i class="ti ti-pencil"></i></button>
        <button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateLink('${l.uuid}')"><i class="ti ti-replace"></i></button>
        <button class="iconbtn" title="ریست حجم مصرفی" onclick="resetLinkUsage('${l.uuid}')"><i class="ti ti-refresh"></i></button>
        <button class="iconbtn" title="حذف" onclick="deleteLink('${l.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>
      </div>
    </div>
  </article>`;
}
function renderLinks(){
  const q = ($('linkSearch').value||'').toLowerCase(); const cat = $('linkFilterCat').value;
  const all = LINKS.filter(l=>!l.is_client);
  renderQuickStats(all);
  const filtered = all.filter(l=>{ if(cat && String(l.category_id)!==String(cat)) return false; if(q && !(`${l.label||''} ${l.uuid||''} ${l.protocol||''}`).toLowerCase().includes(q)) return false; return true; });
  $('linksEmpty').style.display = filtered.length ? 'none' : 'block';
  $('ibGrid').innerHTML = filtered.map(ibCardHtml).join('');
  if($('ibCountLabel')) $('ibCountLabel').textContent = `${filtered.length} اینباند`;
  updateLinksBulkBar();
}
function toggleAllLinks(checked){
  document.querySelectorAll('.ib-row-check').forEach(c=>c.checked=checked);
  updateLinksBulkBar();
}
function selectedLinkUuids(){
  return Array.from(document.querySelectorAll('.ib-row-check:checked')).map(c=>c.dataset.uid);
}
function updateLinksBulkBar(){
  const sel = selectedLinkUuids();
  $('ibBulkBar').style.display = sel.length ? 'flex' : 'none';
  if($('ibSelCount')) $('ibSelCount').textContent = sel.length;
  const all = document.querySelectorAll('.ib-row-check');
  if($('ibSelAll')) $('ibSelAll').checked = all.length>0 && sel.length===all.length;
  document.querySelectorAll('.ib-card').forEach(card=>{
    const cb = card.querySelector('.ib-row-check');
    card.classList.toggle('ib-selected', !!(cb && cb.checked));
  });
}
async function bulkToggleLinks(active){
  const sel = selectedLinkUuids(); if(!sel.length) return;
  try{ await Promise.all(sel.map(uid=>api(`/api/links/${uid}`, {method:'PATCH', body: JSON.stringify({active})}))); toast('بروزرسانی گروهی انجام شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function bulkDeleteLinks(){
  const sel = selectedLinkUuids(); if(!sel.length) return;
  if(!confirm(`${sel.length} ${t('اینباند حذف شود؟')}`)) return;
  try{ await Promise.all(sel.map(uid=>api(`/api/links/${uid}`, {method:'DELETE'}))); toast('حذف گروهی انجام شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function openClients(uid){
  const inbound=LINKS.find(x=>x.uuid===uid); if(!inbound) return;
  try{
    const d=await api(`/api/links/${uid}/clients`);
    const clients=d.clients||[];
    openDrawer(`Client Manager · ${escapeHtml(inbound.label||'Inbound')}`, `
      <div class="client-manager">
        <div class="client-hero"><div><b>مدیریت کلاینت‌های واقعی</b><small>هر کلاینت UUID مستقل دارد و برای پروتکل‌های Live مستقیماً توسط Relay قابل احراز است.</small></div><span class="badge ${inbound.live_status==='live'?'green':'red'}">${inbound.live_status==='live'?'LIVE':'LINK-ONLY'}</span></div>
        ${inbound.live_status!=='live'?`<div class="notice danger-note">این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.</div>`:''}
        <div class="client-create"><div class="grp"><label>نام کلاینت</label><input id="clientName" placeholder="مثلاً iPhone · User 01"></div><div class="row2"><div class="grp"><label>حجم (GB، خالی = والد)</label><input id="clientLimit" type="number" min="0" placeholder="0"></div><div class="grp"><label>انقضا (روز، 0 = والد)</label><input id="clientDays" type="number" min="0" placeholder="0"></div></div><button class="btn primary" style="width:100%" onclick="createClient('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت واقعی</button></div>
        <div class="client-list">${clients.length?clients.map(c=>`<article class="client-row"><div class="client-avatar"><i class="ti ti-device-laptop"></i></div><div class="client-main"><b>${escapeHtml(c.label||'Client')}</b><small class="mono">${escapeHtml(c.uuid)}</small><div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span><span>${fmtBytes(c.used_bytes||0)}${c.limit_bytes?' / '+fmtBytes(c.limit_bytes):''}</span><span>${c.expires_at?escapeHtml(c.expires_at.slice(0,10)):'∞'}</span></div></div><div class="client-actions"><button class="iconbtn" title="لینک اشتراک" onclick="showClientSubLink(${escapeHtml(JSON.stringify(c.sub||''))})"><i class="ti ti-qrcode"></i></button><button class="iconbtn" title="کپی VLESS" onclick="copyText(${escapeHtml(JSON.stringify(c.vless_full||''))})"><i class="ti ti-copy"></i></button><button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateClient('${uid}','${c.uuid}')"><i class="ti ti-replace"></i></button><button class="iconbtn" title="ریست حجم مصرفی" onclick="resetClientUsage('${uid}','${c.uuid}')"><i class="ti ti-refresh"></i></button><button class="iconbtn" title="حذف" onclick="deleteClient('${uid}','${c.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button></div></article>`).join(''):'<div class="empty-client">هنوز کلاینتی برای این اینباند ساخته نشده.</div>'}</div>
      </div>
  `, `<button class="btn" style="width:100%" onclick="loadLinks();openClients('${uid}')"><i class="ti ti-refresh"></i>بروزرسانی</button>`);
  }catch(e){toast(e.message,false)}
}
async function createClient(uid){
  const label=$('clientName')?.value||''; const limit=Number($('clientLimit')?.value||0); const days=Number($('clientDays')?.value||0);
  try{await api(`/api/links/${uid}/clients`,{method:'POST',body:JSON.stringify({label,limit_bytes:limit?limit*1024*1024*1024:0,expires_days:days})});toast('کلاینت واقعی ساخته شد ✓');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}
async function deleteClient(uid,cid){
  if(!confirm(t('این کلاینت حذف شود؟'))) return;
  try{await api(`/api/links/${uid}/clients/${cid}`,{method:'DELETE'});toast('کلاینت حذف شد');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}
async function regenerateClient(uid,cid){
  if(!confirm(t('یک لینک/UUID جدید برای این کلاینت صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{await api(`/api/links/${cid}/regenerate`,{method:'POST'});toast('لینک کلاینت تعویض شد ✓');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}
async function resetClientUsage(uid,cid){
  if(!confirm(t('حجم مصرفی این کلاینت از صفر شروع شود؟'))) return;
  try{await api(`/api/links/${cid}/reset-usage`,{method:'POST'});toast('حجم مصرف ریست شد ✓');openClients(uid);loadLinks();}catch(e){toast(e.message,false)}
}

// ============================================================
// Standalone Client Manager page (بخش جدای ساخت کلاینت)
// ============================================================
let CM_INBOUNDS = [];
let CM_SELECTED_UID = '';
async function loadClientManager(){
  try{
    const res = await api('/api/links');
    CM_INBOUNDS = res.links || [];
    const sel = $('cmInboundSelect');
    const keep = CM_SELECTED_UID;
    sel.innerHTML = '<option value="">— انتخاب کنید —</option>' + CM_INBOUNDS.map(l=>
      `<option value="${l.uuid}">${escapeHtml(l.label||'Inbound')} · ${escapeHtml(protoLabel(l))} ${l.live_status==='live'?'(LIVE)':'(LINK-ONLY)'}</option>`
    ).join('');
    if(keep && CM_INBOUNDS.some(l=>l.uuid===keep)){
      sel.value = keep;
      loadClientManagerClients(keep);
    } else {
      $('cmInboundInfo').innerHTML = '';
      $('cmBody').innerHTML = `<div class="empty"><i class="ti ti-router"></i>ابتدا یک اینباند را از بالا انتخاب کن</div>`;
    }
  }catch(e){ toast(e.message, false); }
}
async function loadClientManagerClients(uid){
  CM_SELECTED_UID = uid || '';
  if(!uid){
    $('cmInboundInfo').innerHTML = '';
    $('cmBody').innerHTML = `<div class="empty"><i class="ti ti-router"></i>ابتدا یک اینباند را از بالا انتخاب کن</div>`;
    return;
  }
  const inbound = CM_INBOUNDS.find(x=>x.uuid===uid);
  try{
    const d = await api(`/api/links/${uid}/clients`);
    const clients = d.clients || [];
    $('cmInboundInfo').innerHTML = inbound ? `
      <div class="client-hero" style="margin-top:12px"><div><b>${escapeHtml(inbound.label||'Inbound')}</b><small>${escapeHtml(protoLabel(inbound))} · ${escapeHtml(inbound.address||'')}:${inbound.port||443}</small></div><span class="badge ${inbound.live_status==='live'?'green':'red'}">${inbound.live_status==='live'?'LIVE':'LINK-ONLY'}</span></div>
      ${inbound.live_status!=='live'?`<div class="notice danger-note" style="margin-top:10px">این اینباند فعلاً فقط لینک تولید می‌کند. برای Client واقعی، ابتدا یک ترکیب Live مثل VLESS + WS/TCP/XHTTP انتخاب کنید.</div>`:''}
    ` : '';
    $('cmBody').innerHTML = `
      <div class="card" style="padding:16px;margin-bottom:14px">
        <div class="client-create">
          <div class="grp"><label>نام کلاینت</label><input id="cmClientName" placeholder="مثلاً iPhone · User 01"></div>
          <div class="row2">
            <div class="grp"><label>حجم (GB، خالی = والد)</label><input id="cmClientLimit" type="number" min="0" placeholder="0"></div>
            <div class="grp"><label>انقضا (روز، 0 = والد)</label><input id="cmClientDays" type="number" min="0" placeholder="0"></div>
          </div>
          <button class="btn primary" style="width:100%" onclick="createClientMgr('${uid}')"><i class="ti ti-user-plus"></i>ساخت کلاینت واقعی</button>
        </div>
      </div>
      <div class="card" style="padding:16px">
        <div class="panel-head" style="padding:0 0 12px;border:0"><div><b>کلاینت‌های این اینباند</b><small>${clients.length} کلاینت</small></div></div>
        <div class="client-list">${clients.length ? clients.map(c=>`<article class="client-row"><div class="client-avatar"><i class="ti ti-device-laptop"></i></div><div class="client-main"><b>${escapeHtml(c.label||'Client')}</b><small class="mono">${escapeHtml(c.uuid)}</small><div class="client-tags"><span>${c.active?'فعال':'خاموش'}</span><span>${fmtBytes(c.used_bytes||0)}${c.limit_bytes?' / '+fmtBytes(c.limit_bytes):''}</span><span>${c.expires_at?escapeHtml(c.expires_at.slice(0,10)):'∞'}</span></div></div><div class="client-actions"><button class="iconbtn" title="لینک اشتراک" onclick="showClientSubLink(${escapeHtml(JSON.stringify(c.sub||''))})"><i class="ti ti-qrcode"></i></button><button class="iconbtn" title="کپی VLESS" onclick="copyText(${escapeHtml(JSON.stringify(c.vless_full||''))})"><i class="ti ti-copy"></i></button><button class="iconbtn" title="تعویض لینک (UUID جدید)" onclick="regenerateClientMgr('${uid}','${c.uuid}')"><i class="ti ti-replace"></i></button><button class="iconbtn" title="ریست حجم مصرفی" onclick="resetClientMgrUsage('${uid}','${c.uuid}')"><i class="ti ti-refresh"></i></button><button class="iconbtn" title="حذف" onclick="deleteClientMgr('${uid}','${c.uuid}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button></div></article>`).join('') : '<div class="empty-client">هنوز کلاینتی برای این اینباند ساخته نشده.</div>'}</div>
      </div>
    `;
  }catch(e){ toast(e.message, false); }
}
async function createClientMgr(uid){
  const label = $('cmClientName').value.trim();
  const limit = Number($('cmClientLimit').value) || 0;
  const days = Number($('cmClientDays').value) || 0;
  try{
    await api(`/api/links/${uid}/clients`, {method:'POST', body: JSON.stringify({label, limit_bytes: limit ? limit*1024*1024*1024 : 0, expires_days: days})});
    toast('کلاینت واقعی ساخته شد ✓');
    loadClientManagerClients(uid);
  }catch(e){ toast(e.message, false); }
}
async function deleteClientMgr(uid, cid){
  if(!confirm(t('این کلاینت حذف شود؟'))) return;
  try{ await api(`/api/links/${uid}/clients/${cid}`, {method:'DELETE'}); toast('کلاینت حذف شد'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function regenerateClientMgr(uid, cid){
  if(!confirm(t('یک لینک/UUID جدید برای این کلاینت صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{ await api(`/api/links/${cid}/regenerate`, {method:'POST'}); toast('لینک کلاینت تعویض شد ✓'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function resetClientMgrUsage(uid, cid){
  if(!confirm(t('حجم مصرفی این کلاینت از صفر شروع شود؟'))) return;
  try{ await api(`/api/links/${cid}/reset-usage`, {method:'POST'}); toast('حجم مصرف ریست شد ✓'); loadClientManagerClients(uid); }
  catch(e){ toast(e.message, false); }
}
async function copyText(v){
  v = v || '';
  if(window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText){
    try{ await navigator.clipboard.writeText(v); toast('کپی شد ✓'); return; }catch(e){ /* برو سراغ روش قدیمی */ }
  }
  if(legacyCopy(v)){ toast('کپی شد ✓'); } else { prompt('کپی کنید:', v); }
}
function showClientSubLink(subUrl){
  if(!subUrl){ toast('لینک ساب برای این کلاینت در دسترس نیست', false); return; }
  const qr = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(subUrl);
  openDrawer('لینک اشتراک کلاینت', `
    <div class="qr-box"><img src="${qr}"></div>
    <div class="grp"><label>لینک ساب</label><div class="copy-row"><input readonly value="${escapeHtml(subUrl)}" id="clientSubLinkInp"></div></div>
    <p class="hint">اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('clientSubLinkInp')"><i class="ti ti-copy"></i>کپی لینک ساب</button>`);
}

function showSubLink(uid){
  const l = LINKS.find(x=>x.uuid===uid);
  if(!l) return;
  const qr = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(l.sub_url || l.sub);
  openDrawer('لینک اشتراک', `
    <div class="qr-box"><img src="${qr}"></div>
    <div class="grp"><label>لینک ساب</label><div class="copy-row"><input readonly value="${escapeHtml(l.sub_url||l.sub)}" id="subLinkInp"></div></div>
    <div class="grp"><label>صفحه‌ی نمایش اشتراک (برای مشتری)</label><div class="copy-row"><input readonly value="${escapeHtml((l.sub_url||l.sub||'').replace('/sub/','/subscription/'))}" id="subPortalInp"></div></div>
    <p class="hint">اگر این لینک برای مشتری باز نمی‌شود، ابتدا از تب «تنظیمات» آدرس عمومی پنل را درست تنظیم کنید.</p>
  `, `<button class="btn primary" style="width:100%" onclick="copyInput('subLinkInp')"><i class="ti ti-copy"></i>کپی لینک ساب</button>`);
}
function legacyCopy(text){
  // execCommand روی همه‌ی مرورگرها حتی بدون HTTPS (secure context) کار می‌کند.
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.top = '-9999px';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  let ok = false;
  try{ ok = document.execCommand('copy'); }catch(e){ ok = false; }
  document.body.removeChild(ta);
  return ok;
}
async function copyInput(id){
  const el = $(id);
  if(!el) return;
  const value = el.value || '';
  el.focus();
  el.select();
  // navigator.clipboard فقط در HTTPS (secure context) در دسترسه؛ اگر پنل با HTTP
  // (بدون دامنه/SSL) باز شده باشه این آبجکت اصلاً وجود نداره و باید مستقیم به
  // روش قدیمی (execCommand) یا در آخرین حالت به prompt دستی سوییچ کنیم.
  if(window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText){
    try{
      await navigator.clipboard.writeText(value);
      toast('کپی شد ✓');
      return;
    }catch(e){ /* برو سراغ روش قدیمی */ }
  }
  if(legacyCopy(value)){
    toast('کپی شد ✓');
  } else {
    prompt('کپی کنید:', value);
  }
}
async function toggleLink(uid, active){
  try{ await api(`/api/links/${uid}`, {method:'PATCH', body: JSON.stringify({active})}); toast('بروزرسانی شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function deleteLink(uid){
  if(!confirm(t('این کانفیگ حذف شود؟'))) return;
  try{ await api(`/api/links/${uid}`, {method:'DELETE'}); toast('حذف شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function resetLinkUsage(uid){
  if(!confirm(t('حجم مصرفی این کانفیگ از صفر شروع شود؟'))) return;
  try{ await api(`/api/links/${uid}/reset-usage`, {method:'POST'}); toast('حجم مصرف ریست شد'); loadLinks(); }
  catch(e){ toast(e.message, false); }
}
async function regenerateLink(uid){
  if(!confirm(t('یک لینک/UUID جدید صادر شود؟ لینک قبلی بلافاصله از کار می‌افتد و باید لینک جدید را دوباره برای کاربر بفرستید.'))) return;
  try{ const r = await api(`/api/links/${uid}/regenerate`, {method:'POST'}); toast('لینک جدید صادر شد'); loadLinks(); showSubLink(r.uuid); }
  catch(e){ toast(e.message, false); }
}
async function openAutoLink(){
  const profile = await askAutoProfile();
  if(profile===null) return;
  const outbound_proxy_ids = await askOutboundChoice({title:'ساخت هوشمند', sub:'ترافیک از کجا خارج شود؟ (می‌توانی چند لوکیشن انتخاب کنی)', current: localStorage.getItem('fp_quick_outbound_proxy') || '', multi:true});
  if(outbound_proxy_ids===null) return;
  const outbound_proxy_id = outbound_proxy_ids[0] || '';
  try{
    const r = await api('/api/links/auto', {method:'POST', body: JSON.stringify({profile, outbound_proxy_id, outbound_proxy_ids})});
    toast('ساخته شد: ' + (r.label || 'کانفیگ خودکار') + ' ✓'); loadLinks();
  }catch(e){ toast(e.message, false); }
}
// Single source of truth for turning a link's stored fields into
// {base_protocol, network, security}. Both the builder's initial render and
// the edit-drawer's hidden-field sync must agree, or the visible transport
// card and the value that actually gets submitted can diverge (this used to
// happen for links whose `protocol` was a legacy shortcut like "vless-ws":
// the card correctly showed WebSocket, but the hidden #mNetwork field fell
// back to a stale/defaulted "tcp" a moment later).
function deriveManualParts(l){
  l = l || {};
  const proto = l.protocol || 'manual';
  if(proto === 'manual'){
    // Created by the advanced builder: base_protocol/network/security were
    // explicitly written by the backend and are always reliable.
    return {bp: l.base_protocol || 'vless', net: l.network || 'ws', sec: l.security || 'tls'};
  }
  if(proto==='vless-ws') return {bp:'vless',net:'ws',sec:'tls'};
  if(proto==='vless-tcp') return {bp:'vless',net:'tcp',sec:'none'};
  if(proto.startsWith('xhttp-')) return {bp:'vless',net:'xhttp',sec:'tls'};
  if(proto==='vmess-ws') return {bp:'vmess',net:'ws',sec:'tls'};
  if(proto==='trojan-ws') return {bp:'trojan',net:'ws',sec:'tls'};
  return {bp: l.base_protocol || 'vless', net: l.network || 'ws', sec: l.security || 'tls'};
}
function manualBuilderHtml(l){
  l = l || {};
  const parts = deriveManualParts(l);
  let bp = parts.bp, net = parts.net, sec = parts.sec;
  const methods = MANUAL_META.shadowsocks_methods || ['chacha20-ietf-poly1305','aes-128-gcm','aes-256-gcm'];
  const icons = {vless:'ti-bolt',vmess:'ti-brand-vscode',trojan:'ti-shield-lock',shadowsocks:'ti-brand-shield'};
  const bpLabels = {vless:'VLESS',vmess:'VMess',trojan:'Trojan',shadowsocks:'Shadowsocks'};
  const nets = [
    ['tcp','TCP','Raw / direct','ti-arrows-right-left'],
    ['ws','WebSocket','WS over HTTP','ti-world'],
    ['grpc','gRPC','HTTP/2 transport','ti-transfer'],
    ['xhttp','XHTTP','Modern HTTP transport','ti-brand-xamarin']
  ];
  const secs = (MANUAL_META.securities||[]);
  const fpOpts=(MANUAL_META.fingerprints||['chrome','firefox','safari','ios','android','edge','random']).map(x=>`<option value="${x}" ${(l.fingerprint||'chrome')===x?'selected':''}>${x}</option>`).join('');
  const methodOpts=methods.map(x=>`<option value="${x}" ${(l.ss_method||methods[0])===x?'selected':''}>${x}</option>`).join('');
  const conn=Number(l.connection_limit||0), speed=Number(l.speed_limit_bytes||0), speedMbit=speed?Math.max(1,Math.round(speed*8/1000000)):'';
  return `
    <div class="inbound-builder">
      <div class="ib-hero">
        <div class="ib-title"><div class="ib-icon"><i class="ti ti-adjustments-horizontal"></i></div><div><b>${l.uuid?'ویرایش اینباند':'ساخت اینباند حرفه‌ای'}</b><small>پروتکل پایه، ترنسپورت و امنیت کاملاً تفکیک‌شده</small></div></div>
        <span class="badge gray">INBOUND BUILDER</span>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">1</span><div><b>پروتکل پایه</b><small>اول مشخص کن با چه پروتکلی کانفیگ ساخته شود</small></div></div>
          <div id="ibProtocolCards" class="ib-matrix">
            ${Object.entries(bpLabels).map(([id,label])=>`<label class="ib-opt ${bp===id?'on':''}" data-proto-card="${id}"><input type="radio" name="ibBaseProtocol" value="${id}" ${bp===id?'checked':''} onchange="selectBaseProtocol('${id}')"><span class="ib-opt-icon"><i class="ti ${icons[id]||'ti-network'}"></i></span><span><b>${label}</b><small>${id==='vless'?'UUID / XTLS ecosystem':id==='vmess'?'Legacy-compatible':id==='trojan'?'Password-style auth':'AEAD proxy'}</small></span></label>`).join('')}
          </div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">2</span><div><b>Transport / Network</b><small>حالا مسیر انتقال را جداگانه انتخاب کن</small></div></div>
          <div id="ibTransportCards" class="ib-matrix">
            ${nets.map(([id,label,sub,icon])=>`<label class="ib-opt ${net===id?'on':''}" data-net-card="${id}"><input type="radio" name="ibNetwork" value="${id}" ${net===id?'checked':''} onchange="selectTransport('${id}')"><span class="ib-opt-icon"><i class="ti ${icon}"></i></span><span><b>${label}</b><small>${sub}</small></span></label>`).join('')}
          </div>
          <div id="ibTransportNote" class="ib-status" style="margin-top:10px"></div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body">
          <div class="ib-step"><span class="num">3</span><div><b>Security</b><small>TLS / Reality / None را مستقل از ترنسپورت انتخاب کن</small></div></div>
          <div id="ibSecurityCards" class="ib-matrix">
            ${secs.map(x=>`<label class="ib-opt ${sec===x.id?'on':''}" data-sec-card="${x.id}"><input type="radio" name="ibSecurity" value="${x.id}" ${sec===x.id?'checked':''} onchange="selectSecurity('${x.id}')"><span class="ib-opt-icon"><i class="ti ${x.id==='reality'?'ti-key':x.id==='tls'?'ti-lock':'ti-lock-open'}"></i></span><span><b>${x.label}</b><small>${x.id==='reality'?'Reality public-key mode':x.id==='tls'?'Standard TLS':'No TLS wrapper'}</small></span></label>`).join('')}
          </div>
          <div id="mLiveHint" class="ib-status" style="margin-top:10px"></div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-head"><div><b>4. Endpoint & Advanced Parameters</b><small>فقط فیلدهای مرتبط با انتخاب بالا نمایش داده می‌شوند</small></div><i class="ti ti-server-2"></i></div>
        <div class="ib-section-body">
          <div class="ib-grid">
            <div class="grp"><label>نام / Remark</label><input id="fLabel" value="${escapeHtml(l.label||'')}" placeholder="مثلاً: VIP-01"></div>
            <div class="grp"><label>دسته‌بندی</label><select id="fCategory"><option value="0">بدون دسته</option>${CATEGORIES.map(c=>`<option value="${c.id}" ${String(l.category_id)===String(c.id)?'selected':''}>${escapeHtml(c.name)}</option>`).join('')}</select></div>
            <div class="grp"><label>آدرس / Domain</label><div class="endpoint-input"><input id="mAddress" placeholder="example.com" value="${escapeHtml(l.address||'')}" oninput="updateBuilderSummary()"><button type="button" class="btn endpoint-btn" onclick="loadRailwayEndpoint()"><i class="ti ti-cloud"></i>Railway</button></div></div>
            <div class="grp"><label>Port</label><div class="endpoint-input"><input id="mPort" type="number" min="1" max="65535" value="${l.port||443}" oninput="updateBuilderSummary()"><button type="button" class="btn endpoint-btn" onclick="testCurrentTcp()"><i class="ti ti-activity"></i>Ping</button></div></div>
            <div class="grp"><label>Fingerprint</label><select id="mFingerprint">${fpOpts}</select></div>
            <div class="grp"><label>ALPN</label><input id="mAlpn" value="${escapeHtml(l.alpn||'')}" placeholder="h2,http/1.1"></div>
            <div id="mWsXhttpWrap" class="ib-grid ib-full">
              <div class="grp"><label>Path</label><input id="mPath" placeholder="/ws" value="${escapeHtml(l.path||'')}"></div>
              <div class="grp"><label>Host Header</label><input id="mHost" placeholder="domain.com" value="${escapeHtml(l.host_header||'')}"></div>
            </div>
            <div id="mXhttpModeWrap" class="grp ib-full"><label>XHTTP Mode</label><select id="mXhttpMode">${(MANUAL_META.xhttp_modes||['auto','packet-up','stream-up','stream-one']).map(x=>`<option value="${x}" ${(l.xhttp_mode||'packet-up')===x?'selected':''}>${x}</option>`).join('')}</select><small style="opacity:.7">packet-up و stream-up توسط این پنل واقعاً سرو می‌شن؛ auto به‌صورت خودکار روی packet-up قفل می‌شه، stream-one فقط لینک می‌سازه (Live نیست).</small></div>
            <div id="mGrpcWrap" class="ib-grid ib-full"><div class="grp"><label>Service Name</label><input id="mGrpcService" placeholder="service" value="${escapeHtml(l.grpc_service_name||'')}"></div><div class="grp"><label>gRPC Mode</label><select id="mGrpcMode"><option value="gun" ${(l.grpc_mode||'gun')==='gun'?'selected':''}>gun</option><option value="multi" ${l.grpc_mode==='multi'?'selected':''}>multi</option></select></div></div>
            <div id="mTcpWrap" class="ib-grid ib-full"><div class="grp"><label>Header Type</label><select id="mHeaderType"><option value="" ${!l.header_type?'selected':''}>none</option><option value="http" ${l.header_type==='http'?'selected':''}>http</option></select></div><div class="grp"><label>Flow</label><select id="mFlow"><option value="" ${!l.flow?'selected':''}>—</option><option value="xtls-rprx-vision" ${l.flow==='xtls-rprx-vision'?'selected':''}>xtls-rprx-vision</option></select></div></div>
            <div id="mTlsWrap" class="ib-grid ib-full"><div class="grp"><label>SNI</label><input id="mSni" value="${escapeHtml(l.sni||'')}" placeholder="example.com"></div><label class="chk" style="align-self:end;margin-bottom:16px"><input id="mAllowInsecure" type="checkbox" ${l.allow_insecure?'checked':''}> Allow Insecure</label></div>
            <div id="mRealityWrap" class="ib-grid ib-full"><div class="grp"><label>Reality SNI</label><input id="mRealitySni" value="${escapeHtml(l.sni||'')}" placeholder="www.example.com"></div><div class="grp"><label>Public Key</label><input id="mRealityPbk" value="${escapeHtml(l.reality_public_key||'')}" placeholder="public key"></div><div class="grp"><label>Short ID</label><input id="mRealitySid" value="${escapeHtml(l.reality_short_id||'')}" placeholder="short id"></div><div class="grp"><label>Spider X</label><input id="mRealitySpx" value="${escapeHtml(l.reality_spider_x||'/')}" placeholder="/"></div><div class="grp ib-full"><label>Private Key (فقط برای نود Xray-core خودتان — این پنل ذخیره‌اش نمی‌کند)</label><div class="endpoint-input"><input id="mRealityPrivRaw" readonly placeholder="بعد از «Generate Reality Keypair» اینجا نمایش داده می‌شود" value=""><button type="button" class="btn endpoint-btn" onclick="copyText($('mRealityPrivRaw').value)"><i class="ti ti-copy"></i>Copy</button></div></div><div class="ib-full"><button type="button" class="btn" onclick="generateRealityKeys()"><i class="ti ti-key"></i>Generate Reality Keypair</button></div></div>
            <div id="mShadowWrap" class="ib-grid ib-full"><div class="grp"><label>Encryption Method</label><select id="mSsMethod">${methodOpts}</select></div><div class="grp"><label>Password</label><input id="mSsPassword" type="password" value="${escapeHtml(l.ss_password||'')}" placeholder="Password / secret"></div></div>
            <div class="grp"><label>حجم (GB)</label><input id="fLimitVal" type="number" min="0" value="${l.limit_bytes?Math.round(l.limit_bytes/1073741824):''}"></div>
            <div class="grp"><label>اعتبار (روز)</label><input id="fDays" type="number" min="0" value="${l.expires_at?Math.max(0,Math.ceil((new Date(l.expires_at).getTime()-Date.now())/86400000)):''}"></div>
            <div class="grp"><label>زمان دقیق انقضا</label><input id="fExpiresAt" type="datetime-local" value="${l.expires_at?new Date(l.expires_at).toISOString().slice(0,16):''}"></div>
            <div class="grp"><label>IP Limit</label><input id="fIpLimit" type="number" min="0" value="${l.ip_limit||0}"></div>
            <div class="grp"><label>Connection Limit</label><input id="fConnLimit" type="number" min="0" value="${conn}"></div>
            <div class="grp"><label>تعداد کاربر</label><input id="fClientLimit" type="number" min="0" max="1000" value="${l.client_limit||0}" placeholder="0 = نامحدود"></div>
            <div class="grp"><label>تعداد خروجی</label><input id="fConfigCount" type="number" min="1" max="40" value="${l.config_count||1}"></div>
            <div class="grp ib-full"><label>آی‌پی‌های تمیز (Clean IP) — هر خط یک آی‌پی/دامنه</label><textarea id="fCleanIps" rows="3" placeholder="1.2.3.4&#10;5.6.7.8&#10;clean.example.com" style="width:100%;resize:vertical;font-family:monospace">${escapeHtml((l.clean_ips||[]).join('\n'))}</textarea><small style="opacity:.7">اگه اینجا چند آی‌پی/دامنه بذاری، «تعداد خروجی» به همون تعداد کانفیگ می‌سازه که هرکدوم روی یکی از این آی‌پی‌ها می‌ره (همه توی یک سابسکریپشن)؛ اگه خالی باشه، فقط همون تعداد کپیِ یک کانفیگ با نام‌های متفاوت ساخته می‌شه.</small></div>
            <div class="grp"><label>Speed (Mbit/s)</label><input id="fSpeed" type="number" min="0" value="${speedMbit}" placeholder="0 = نامحدود"></div>
            <div class="grp ib-full"><label>یادداشت داخلی</label><input id="fNote" value="${escapeHtml(l.note||'')}" placeholder="توضیحات اختیاری"></div>
          </div>
        </div>
      </div>

      <div class="ib-section">
        <div class="ib-section-body"><div class="ib-step"><span class="num">5</span><div><b>Summary</b><small>قبل از ذخیره ترکیب نهایی را بررسی کن</small></div></div>
          <div class="ib-summary"><div class="sum"><small>PROTOCOL</small><b id="sumProtocol">${bp.toUpperCase()}</b></div><div class="sum"><small>NETWORK</small><b id="sumNetwork">${net.toUpperCase()}</b></div><div class="sum"><small>SECURITY</small><b id="sumSecurity">${sec.toUpperCase()}</b></div><div class="sum"><small>PORT</small><b id="sumPort">${l.port||443}</b></div><div class="sum"><small>TRAFFIC</small><b id="sumTraffic">—</b></div><div class="sum"><small>LIMITS</small><b id="sumLimits">—</b></div></div>
        </div>
      </div>
    </div>`;
}

function refreshInboundCards(){
  const bp=$('mBase')?.value || document.querySelector('input[name="ibBaseProtocol"]:checked')?.value || 'vless';
  const net=$('mNetwork')?.value || document.querySelector('input[name="ibNetwork"]:checked')?.value || 'ws';
  const sec=$('mSecurity')?.value || document.querySelector('input[name="ibSecurity"]:checked')?.value || 'tls';
  document.querySelectorAll('[data-proto-card]').forEach(e=>e.classList.toggle('on',e.dataset.protoCard===bp));
  document.querySelectorAll('[data-net-card]').forEach(e=>e.classList.toggle('on',e.dataset.netCard===net));
  document.querySelectorAll('[data-sec-card]').forEach(e=>e.classList.toggle('on',e.dataset.secCard===sec));
}
function selectBaseProtocol(id){
  let hidden=document.getElementById('mBase'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mBase';document.body.appendChild(hidden)} hidden.value=id;
  const ss=id==='shadowsocks';
  const secWrap=document.getElementById('ibSecurityCards');
  if(secWrap){document.querySelectorAll('[data-sec-card]').forEach(e=>{const sid=e.dataset.secCard; e.classList.toggle('off',ss && sid!=='none'); const inp=e.querySelector('input'); if(inp) inp.disabled=ss&&sid!=='none';}); if(ss){selectSecurity('none');}}
  if(ss && document.querySelector('input[name="ibNetwork"]:checked')?.value!=='tcp') selectTransport('tcp');
  document.getElementById('mShadowWrap')?.style.setProperty('display',ss?'':'none');
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}
function selectTransport(id){
  let hidden=document.getElementById('mNetwork'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mNetwork';document.body.appendChild(hidden)} hidden.value=id;
  const ss=document.getElementById('mBase')?.value==='shadowsocks';
  if(ss && id!=='tcp'){toast('Shadowsocks در این سازنده فقط با TCP پشتیبانی می‌شود',false);hidden.value='tcp';return selectTransport('tcp');}
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}
function selectSecurity(id){
  let hidden=document.getElementById('mSecurity'); if(!hidden){hidden=document.createElement('input');hidden.type='hidden';hidden.id='mSecurity';document.body.appendChild(hidden)} hidden.value=id;
  refreshInboundCards(); onManualChange(); updateBuilderSummary();
}

function updateBuilderSummary(){
  const val=id=>$(id)?.value || '—'; const set=(id,v)=>{const e=$(id);if(e)e.textContent=v};
  set('sumProtocol',(val('mBase')||'vless').toUpperCase()); set('sumNetwork',(val('mNetwork')||'tcp').toUpperCase()); set('sumSecurity',(val('mSecurity')||'none').toUpperCase()); set('sumPort',val('mPort'));
  const traffic=Number(val('fLimitVal'))||0; set('sumTraffic',traffic?`${traffic} GB`:'نامحدود');
  const ip=Number(val('fIpLimit'))||0, conn=Number(val('fConnLimit'))||0; set('sumLimits',`IP ${ip||'∞'} / CONN ${conn||'∞'}`);
}
function onManualChange(){
  const base=$('mBase')?.value || 'vless', net=$('mNetwork')?.value || 'ws', sec=$('mSecurity')?.value || 'tls';
  const show=(id,yes)=>{const e=$(id);if(e)e.style.display=yes?'':'none'};
  show('mWsXhttpWrap',net==='ws'||net==='xhttp'); show('mXhttpModeWrap',net==='xhttp'); show('mGrpcWrap',net==='grpc'); show('mTcpWrap',net==='tcp'); show('mTlsWrap',sec==='tls'); show('mRealityWrap',sec==='reality'); show('mShadowWrap',base==='shadowsocks');
  if(base==='shadowsocks'){ if($('mNetwork') && $('mNetwork').value!=='tcp') $('mNetwork').value='tcp'; if($('mSecurity')) $('mSecurity').value='none'; }
  const hint=$('mLiveHint');
  if(hint){
    const live=base!=='shadowsocks' && (MANUAL_META.live_combos||[]).some(c=>c[0]===net&&c[1]===sec) && !(net==='xhttp'&&($('mXhttpMode')?.value||'packet-up')==='stream-one');
    hint.className='ib-status '+(live?'ok':'warn'); hint.innerHTML=live?'<i class="ti ti-circle-check"></i> این ترکیب آماده استفاده است.':'<i class="ti ti-alert-triangle"></i> این ترکیب برای ساخت لینک و مدیریت سرویس آماده شده است.';
  }
  const tn=$('ibTransportNote');
  if(tn){tn.innerHTML=base==='shadowsocks'?'<i class="ti ti-info-circle"></i> Shadowsocks به‌صورت TCP-only در این Builder ارائه می‌شود.':'<i class="ti ti-adjustments-horizontal"></i> Transport فقط مسیر انتقال است و جدا از پروتکل پایه انتخاب می‌شود.';}
  refreshInboundCards(); updateBuilderSummary();
}

async function testCurrentTcp(){
  const host=($('mAddress')?.value||'').trim();
  const port=Number($('mPort')?.value||0);
  if(!host){toast('ابتدا آدرس یا دامنه را وارد کنید',false);return}
  if(!Number.isInteger(port)||port<1||port>65535){toast('پورت نامعتبر است',false);return}
  const btn=document.querySelector('.endpoint-btn[onclick="testCurrentTcp()"]');
  if(btn){btn.disabled=true;btn.innerHTML='<i class="ti ti-loader-2 spin"></i> در حال تست'}
  try{
    const r=await api('/api/network/tcp-ping',{method:'POST',body:JSON.stringify({host,port,timeout:4})});
    if(r.ok) toast(`TCP OK • ${r.latency_ms}ms • ${host}:${port}`);
    else toast(r.message||'اتصال برقرار نشد',false);
  }catch(e){toast(e.message||'خطا در تست TCP',false)}
  finally{if(btn){btn.disabled=false;btn.innerHTML='<i class="ti ti-activity"></i> تست پینگ'}}
}

async function loadRailwayEndpoint(){
  try{
    const r=await api('/api/network/railway');
    if(!r.is_railway && !r.tcp_proxy_domain){toast('اطلاعات TCP Proxy ریل‌وی در این سرویس پیدا نشد',false);return}
    if(r.tcp_proxy_domain){$('mAddress').value=r.tcp_proxy_domain; if(r.tcp_proxy_port) $('mPort').value=r.tcp_proxy_port; updateBuilderSummary(); toast(`Railway TCP Proxy: ${r.tcp_proxy_domain}:${r.tcp_proxy_port||'?'}`)}
    else if(r.public_domain){$('mAddress').value=r.public_domain; updateBuilderSummary(); toast('دامنه عمومی Railway وارد شد؛ برای TCP خام باید TCP Proxy فعال باشد')}
  }catch(e){toast(e.message||'خطا در دریافت اطلاعات Railway',false)}
}

async function generateRealityKeys(){
  try{
    const r=await api('/api/reality-keypair');
    $('mRealityPbk').value=r.public_key;
    $('mRealitySid').value=r.short_id;
    if($('mRealityPrivRaw')) $('mRealityPrivRaw').value=r.private_key||'';
    toast('کلید Reality ساخته شد — Private Key را همین‌جا کپی کنید و روی نود Xray-core خودتان قرار دهید (این پنل آن را ذخیره نمی‌کند).');
  }
  catch(e){ toast(e.message, false); }
}

function onProtocolModeChange(){
  // Kept for compatibility with older inline handlers; the new builder is always advanced.
  const wrap=$('manualBuilderWrap'); if(wrap) wrap.style.display='block'; const quick=$('quickFieldsWrap'); if(quick) quick.style.display='none';
}
function openLinkDrawer(uid){
  const editing=!!uid, l=editing?(LINKS.find(x=>x.uuid===uid)||{}):{};
  openDrawer(editing?'ویرایش اینباند':'ساخت اینباند', `${manualBuilderHtml(l)}`,
    `${editing?`<button class="btn danger" onclick="deleteLink('${uid}');closeDrawer()"><i class="ti ti-trash"></i>حذف</button>`:''}<button class="btn primary" style="flex:1" onclick="submitLink('${uid||''}')"><i class="ti ti-device-floppy"></i>${editing?'ذخیره تغییرات':'ساخت اینباند'}</button>`);
  setTimeout(()=>{
    let bp=document.getElementById('mBase'); if(!bp){bp=document.createElement('input');bp.type='hidden';bp.id='mBase';document.querySelector('.drawer .dr-body')?.appendChild(bp)}
    let net=document.getElementById('mNetwork'); if(!net){net=document.createElement('input');net.type='hidden';net.id='mNetwork';document.querySelector('.drawer .dr-body')?.appendChild(net)}
    let sec=document.getElementById('mSecurity'); if(!sec){sec=document.createElement('input');sec.type='hidden';sec.id='mSecurity';document.querySelector('.drawer .dr-body')?.appendChild(sec)}
    let proto=l.protocol||'manual'; const parts=deriveManualParts(l);
    bp.value=parts.bp;
    net.value=parts.net;
    sec.value=parts.sec;
    if(bp.value==='shadowsocks'){net.value='tcp';sec.value='none'}
    refreshInboundCards(); onManualChange(); updateBuilderSummary();
  },0);
}

async function submitLink(uid){
  const base=$('mBase')?.value || 'vless', net=$('mNetwork')?.value || 'ws', sec=$('mSecurity')?.value || 'tls';
  const port=Number($('mPort')?.value||443);
  if(!Number.isInteger(port)||port<1||port>65535){toast('پورت باید بین 1 تا 65535 باشد',false);return}
  if(base==='shadowsocks' && net!=='tcp'){toast('Shadowsocks فقط با TCP ساخته می‌شود',false);return}
  const num=id=>Math.max(0,Number($(id)?.value||0));
  const body={label:($('fLabel')?.value||'').trim(),protocol:'manual',category_id:$('fCategory')?.value||'0',limit_value:num('fLimitVal'),limit_unit:'GB',expires_days:num('fDays'),expires_at:$('fExpiresAt')?.value||'',ip_limit:num('fIpLimit'),connection_limit:num('fConnLimit'),client_limit:num('fClientLimit'),config_count:Math.max(1,Math.min(40,num('fConfigCount')||1)),clean_ips:($('fCleanIps')?.value||'').trim(),speed_limit_value:num('fSpeed'),speed_limit_unit:'MBIT',note:($('fNote')?.value||'').trim(),port,fingerprint:$('mFingerprint')?.value||'chrome',alpn:$('mAlpn')?.value||''};
  body.manual={base_protocol:base,network:net,security:base==='shadowsocks'?'none':sec,address:$('mAddress')?.value||'',path:$('mPath')?.value||'',host_header:$('mHost')?.value||'',sni:sec==='reality'?($('mRealitySni')?.value||''):($('mSni')?.value||''),alpn:$('mAlpn')?.value||'',flow:$('mFlow')?.value||'',grpc_service_name:$('mGrpcService')?.value||'',grpc_mode:$('mGrpcMode')?.value||'gun',xhttp_mode:$('mXhttpMode')?.value||'packet-up',header_type:$('mHeaderType')?.value||'',allow_insecure:!!$('mAllowInsecure')?.checked,reality_public_key:$('mRealityPbk')?.value||'',reality_short_id:$('mRealitySid')?.value||'',reality_spider_x:$('mRealitySpx')?.value||'/',ss_method:$('mSsMethod')?.value||'chacha20-ietf-poly1305',ss_password:$('mSsPassword')?.value||''};
  if(!uid){
    const ob = await askOutboundChoice({title:'اینباند جدید', sub:'ترافیک از کجا خارج شود؟ (چند لوکیشن = چند کانفیگ جدا در ساب)', multi:true});
    if(ob===null) return;
    body.outbound_proxy_ids = ob; body.outbound_proxy_id = ob[0] || '';
  }
  try{if(uid) await api(`/api/links/${uid}`,{method:'PATCH',body:JSON.stringify(body)});else await api('/api/links',{method:'POST',body:JSON.stringify(body)});toast(uid?'اینباند بروزرسانی شد':'اینباند با موفقیت ساخته شد');closeDrawer();loadLinks();}
  catch(e){toast(e.message||'خطا در ذخیره اینباند',false)}
}

// ============================================================
// CATEGORIES
// ============================================================
async function loadCategories(){
  try{
    const res = await api('/api/categories');
    CATEGORIES = res.categories||[];
    $('catsBody').innerHTML = CATEGORIES.map(c=>`
      <tr><td>${escapeHtml(c.name)}</td><td>${c.limit_bytes?fmtBytes(c.limit_bytes):'نامحدود'}</td>
      <td>${c.expires_days||'—'}</td><td>${c.ip_limit||'—'}</td>
      <td><div class="row-actions">
        <button class="iconbtn" onclick="openCategoryDrawer('${c.id}')"><i class="ti ti-pencil"></i></button>
        ${['0','1'].includes(String(c.id))?'':`<button class="iconbtn" onclick="deleteCategory('${c.id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>`}
      </div></td></tr>
    `).join('') || `<tr><td colspan="5" class="empty">دسته‌بندی‌ای وجود ندارد</td></tr>`;
  }catch(e){ toast(e.message, false); }
}
function openCategoryDrawer(cid){
  const editing = !!cid;
  const c = editing ? CATEGORIES.find(x=>String(x.id)===String(cid)) : {};
  openDrawer(editing?'ویرایش دسته':'دسته جدید', `
    <div class="grp"><label>نام</label><input id="cName" value="${escapeHtml(c.name||'')}"></div>
    <div class="row2">
      <div class="grp"><label>حجم پیش‌فرض (GB)</label><input id="cLimit" type="number" min="0" value="${c.limit_bytes?Math.round(c.limit_bytes/1073741824):''}"></div>
      <div class="grp"><label>انقضا (روز)</label><input id="cDays" type="number" min="0" value="${c.expires_days||''}"></div>
    </div>
    <div class="grp"><label>محدودیت IP</label><input id="cIp" type="number" min="0" value="${c.ip_limit||''}"></div>
  `, `<button class="btn primary" style="flex:1" onclick="submitCategory('${cid||''}')"><i class="ti ti-device-floppy"></i>ذخیره</button>`);
}
async function submitCategory(cid){
  const body = {name:$('cName').value, limit_value:$('cLimit').value||0, limit_unit:'GB', expires_days:$('cDays').value||0, ip_limit:$('cIp').value||0};
  try{
    if(cid){ await api(`/api/categories/${cid}`, {method:'PATCH', body:JSON.stringify(body)}); }
    else{ await api('/api/categories', {method:'POST', body:JSON.stringify(body)}); }
    toast('ذخیره شد'); closeDrawer(); loadCategories();
  }catch(e){ toast(e.message, false); }
}
async function deleteCategory(cid){
  if(!confirm(t('این دسته حذف شود؟'))) return;
  try{ await api(`/api/categories/${cid}`, {method:'DELETE'}); toast('حذف شد'); loadCategories(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// SUB GROUPS
// ============================================================
async function loadSubGroups(){
  try{
    const res = await api('/api/subs');
    const subs = res.subs || [];
    SUBS_CACHE = subs;
    $('nb-subs').textContent = subs.length;
    $('subsBody').innerHTML = subs.map(s=>`
      <tr><td>${escapeHtml(s.name||'—')}</td><td>${s.links_count||0}</td>
      <td class="mono">${escapeHtml(s.sub_url||'')}</td>
      <td><div class="row-actions"><button class="iconbtn" title="اعضا (این پنل + نودها)" onclick="openSubMembersDrawer('${s.sub_id}')"><i class="ti ti-users-group"></i></button><button class="iconbtn" onclick="deleteSubGroup('${s.sub_id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button></div></td></tr>
    `).join('') || `<tr><td colspan="4" class="empty">گروهی وجود ندارد</td></tr>`;
  }catch(e){ $('subsBody').innerHTML = `<tr><td colspan="4" class="empty">در دسترس نیست</td></tr>`; }
}
function openSubGroupDrawer(){
  openDrawer('گروه ساب جدید', `<div class="grp"><label>نام گروه</label><input id="sgName" placeholder="مثلاً: بسته-VIP"></div>
  <p class="hint">بعد از ساخت گروه، از صفحه‌ی کانفیگ‌ها می‌توانید کانفیگ‌ها را به این گروه اضافه کنید.</p>`,
  `<button class="btn primary" style="flex:1" onclick="submitSubGroup()"><i class="ti ti-device-floppy"></i>ساخت</button>`);
}
async function submitSubGroup(){
  try{ await api('/api/subs', {method:'POST', body: JSON.stringify({name: $('sgName').value})}); toast('ساخته شد'); closeDrawer(); loadSubGroups(); }
  catch(e){ toast(e.message, false); }
}
async function deleteSubGroup(id){
  if(!confirm(t('این گروه حذف شود؟'))) return;
  try{ await api(`/api/subs/${id}`, {method:'DELETE'}); toast('حذف شد'); loadSubGroups(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// PLANS
// ============================================================
async function loadPlans(){
  try{
    const res = await api('/api/plans');
    const plans = res.plans||[];
    $('plansBody').innerHTML = plans.map(p=>`
      <tr><td>${escapeHtml(p.name)}</td><td>${p.days} روز</td><td>${p.volume_gb} GB</td><td>${p.speed_mbps||0} Mbps</td>
      <td>⭐ ${p.stars}</td><td>${p.featured?'<span class="badge green">بله</span>':'—'}</td>
      <td><div class="row-actions">
        <button class="iconbtn" onclick="openPlanDrawer('${p.id}')"><i class="ti ti-pencil"></i></button>
        <button class="iconbtn" onclick="deletePlan('${p.id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>
      </div></td></tr>
    `).join('') || `<tr><td colspan="7" class="empty">پلنی وجود ندارد</td></tr>`;
  }catch(e){ toast(e.message, false); }
}
function openPlanDrawer(pid){
  openDrawer(pid?'ویرایش پلن':'پلن جدید', `
    <div class="grp"><label>نام</label><input id="pName"></div>
    <div class="row2"><div class="grp"><label>مدت (روز)</label><input id="pDays" type="number" value="30"></div>
    <div class="grp"><label>حجم (GB)</label><input id="pVolume" type="number" value="50"></div></div>
    <div class="row2"><div class="grp"><label>سرعت (Mbps، 0=نامحدود)</label><input id="pSpeed" type="number" value="0"></div>
    <div class="grp"><label>قیمت (Stars)</label><input id="pStars" type="number" value="99"></div></div>
    <label class="chk"><input type="checkbox" id="pFeatured"> پیشنهاد ویژه</label>
  `, `<button class="btn primary" style="flex:1" onclick="submitPlan('${pid||''}')"><i class="ti ti-device-floppy"></i>ذخیره</button>`);
}
async function submitPlan(pid){
  const body = {name:$('pName').value, days:$('pDays').value, volume_gb:$('pVolume').value, speed_mbps:$('pSpeed').value, stars:$('pStars').value, featured:$('pFeatured').checked};
  try{
    if(pid){ await api(`/api/plans/${pid}`, {method:'PATCH', body:JSON.stringify(body)}); }
    else{ await api('/api/plans', {method:'POST', body:JSON.stringify(body)}); }
    toast('ذخیره شد'); closeDrawer(); loadPlans();
  }catch(e){ toast(e.message, false); }
}
async function deletePlan(pid){
  if(!confirm(t('این پلن حذف شود؟'))) return;
  try{ await api(`/api/plans/${pid}`, {method:'DELETE'}); toast('حذف شد'); loadPlans(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// REPORTS
// ============================================================
async function loadReports(){
  try{
    const days = $('repDays').value;
    const res = await api(`/api/reports/summary?days=${days}`);
    const t = res.totals||{};
    $('repStats').innerHTML = `
      ${statCard('ti-link','#4f7cff', t.links, 'کل کانفیگ‌ها')}
      ${statCard('ti-shopping-cart','#22c58b', t.orders, 'تعداد سفارش')}
      ${statCard('ti-star','#f5a524', t.stars, 'مجموع ⭐ فروش')}
      ${statCard('ti-users','#4f7cff', t.customers, 'مشتری‌ها')}
    `;
    $('repTopBody').innerHTML = (res.top_links||[]).map(l=>`
      <tr><td>${escapeHtml(l.label)}</td><td><span class="badge gray">${protoLabel(l)}</span></td><td class="mono">${fmtBytes(l.used_bytes)}</td></tr>
    `).join('') || `<tr><td colspan="3" class="empty">داده‌ای موجود نیست</td></tr>`;
  }catch(e){ toast(e.message, false); }
}

// ============================================================
// ADMINS
// ============================================================
const ADMIN_PERM_LABELS = {dashboard:'داشبورد',inbounds:'اینباند و کلاینت',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',plans:'پلن فروش',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات'};
async function loadAdmins(){
  try{
    const res = await api('/api/admins');
    ADMIN_CACHE = res.admins || [];
    const adminRows = res.admins || [];
    const activeAdmins = adminRows.filter(a=>a.active).length;
    if($('adminTotal')) $('adminTotal').textContent = adminRows.length;
    if($('adminActive')) $('adminActive').textContent = activeAdmins;
    $('adminsBody').innerHTML = adminRows.map(a=>{
      const isOwner = a.role==='owner';
      const initials = (a.username||'?').replace(/[^A-Za-z0-9آ-ی]/g,'').slice(0,2).toUpperCase() || '?';
      const lastLogin = a.last_login_at ? a.last_login_at.slice(0,16).replace('T',' ') : 'بدون ورود';
      const chips = isOwner
        ? '<span class="admin-perm-chip all"><i class="ti ti-shield-star"></i> دسترسی کامل</span>'
        : ((a.permissions||[]).length
            ? (a.permissions||[]).map(p=>`<span class="admin-perm-chip">${ADMIN_PERM_LABELS[p]||p}</span>`).join('')
            : '<span class="admin-perm-chip">بدون دسترسی</span>');
      const actions = isOwner ? '' : `
        <button class="iconbtn edit" title="ویرایش دسترسی" aria-label="ویرایش دسترسی" onclick="editAdmin('${a.id}')"><i class="ti ti-edit"></i></button>
        <button class="iconbtn power" title="${a.active?'غیرفعال‌سازی':'فعال‌سازی'}" onclick="toggleAdmin('${a.id}', ${!a.active})"><i class="ti ti-power"></i></button>
        <button class="iconbtn danger" title="حذف ادمین" aria-label="حذف ادمین" onclick="deleteAdmin('${a.id}')"><i class="ti ti-trash" style="color:var(--bad)"></i></button>`;
      return `
      <div class="admin-card ${isOwner?'is-owner':''} ${a.active?'':'is-inactive'}">
        <div class="admin-card-top">
          <div class="admin-id">
            <div class="admin-avatar">${escapeHtml(initials)}</div>
            <div class="admin-meta">
              <div class="admin-name">${escapeHtml(a.username)}</div>
              <div class="admin-sub"><span class="admin-status-dot"></span>${a.active?'فعال':'غیرفعال'}</div>
            </div>
          </div>
          <span class="admin-role-badge ${isOwner?'owner':'admin'}"><i class="ti ti-${isOwner?'crown':'shield-check'}"></i>${isOwner?'مالک':'ادمین'}</span>
        </div>
        <div class="admin-perm-row">${chips}</div>
        <div class="admin-card-foot">
          <div class="admin-login-block"><span class="admin-login-label">آخرین فعالیت</span><span class="admin-login mono"><i class="ti ti-clock"></i> ${escapeHtml(lastLogin)}</span></div>
          <div class="row-actions"><span class="admin-actions-label">کنترل حساب</span>${actions}</div>
        </div>
      </div>`;
    }).join('');
  }catch(e){ toast(e.message, false); }
}
function openAdminDrawer(){
  openDrawer('ادمین جدید', `
    <div class="grp"><label>نام کاربری</label><input id="aUser"></div>
    <div class="grp"><label>رمز عبور</label><input type="password" id="aPass"></div>
    <div class="perm-grid">${Object.entries({dashboard:'داشبورد',inbounds:'ساخت و مدیریت اینباند',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',plans:'پلن فروش',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات'}).map(([k,v])=>`<label class="perm-item"><input type="checkbox" data-perm="${k}" ${['dashboard','inbounds','subscriptions'].includes(k)?'checked':''}>${v}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="submitAdmin()"><i class="ti ti-device-floppy"></i>ساخت</button>`);
}
function editAdmin(id){
  const a = ADMIN_CACHE.find(x=>x.id===id); if(!a || a.role==='owner') return;
  const perms=['dashboard','inbounds','clients','subscriptions','categories','plans','reports','messages','bot','admins','settings'];
  const labels={dashboard:'داشبورد',inbounds:'اینباند و کلاینت',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',plans:'پلن فروش',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات'};
  openDrawer('ویرایش ادمین', `
    <div class="grp"><label>نام کاربری</label><input id="eUser" value="${escapeHtml(a.username||'')}"></div>
    <div class="grp"><label>رمز جدید <small>(اختیاری)</small></label><input type="password" id="ePass" placeholder="بدون تغییر خالی بگذار"></div>
    <div class="perm-grid">${perms.map(k=>`<label class="perm-item"><input type="checkbox" data-eperm="${k}" ${((a.permissions||[]).includes(k)?'checked':'')}>${labels[k]}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="saveAdminEdit('${a.id}')"><i class="ti ti-device-floppy"></i>ذخیره تغییرات</button>`);
}
async function saveAdminEdit(id){
  try{ const permissions=[...document.querySelectorAll('[data-eperm]:checked')].map(x=>x.dataset.eperm); const body={username:$('eUser').value.trim(),permissions}; if($('ePass').value) body.password=$('ePass').value; await api(`/api/admins/${id}`,{method:'PATCH',body:JSON.stringify(body)}); toast('اطلاعات ادمین بروزرسانی شد ✓'); closeDrawer(); loadAdmins(); }catch(e){toast(e.message,false)}
}

async function submitAdmin(){
  try{ await api('/api/admins', {method:'POST', body: JSON.stringify({username:$('aUser').value, password:$('aPass').value, permissions:[...document.querySelectorAll('[data-perm]:checked')].map(x=>x.dataset.perm)})}); toast('ساخته شد'); closeDrawer(); loadAdmins(); }
  catch(e){ toast(e.message, false); }
}
async function toggleAdmin(id, active){
  try{ await api(`/api/admins/${id}`, {method:'PATCH', body:JSON.stringify({active})}); loadAdmins(); }
  catch(e){ toast(e.message, false); }
}
async function deleteAdmin(id){
  if(!confirm(t('این ادمین حذف شود؟'))) return;
  try{ await api(`/api/admins/${id}`, {method:'DELETE'}); toast('حذف شد'); loadAdmins(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// Admin registration requests
// ============================================================
let ADMIN_REQ_CACHE = [];
async function loadAdminRequests(){
  try{
    const res = await api('/api/admin-requests');
    ADMIN_REQ_CACHE = res.requests || [];
    const card = $('adminReqCard');
    const pending = ADMIN_REQ_CACHE.filter(r=>r.status==='pending');
    $('adminReqBadge').textContent = pending.length + ' درخواست';
    if(!ADMIN_REQ_CACHE.length){ card.style.display='none'; return; }
    card.style.display = '';
    const rows = [...pending, ...ADMIN_REQ_CACHE.filter(r=>r.status!=='pending')].slice(0, 30);
    $('adminReqBody').innerHTML = rows.length ? rows.map(r=>{
      const date = r.created_at ? r.created_at.slice(0,16).replace('T',' ') : '';
      let statusHtml = '';
      let actions = '';
      if(r.status==='pending'){
        actions = `<button class="btn primary" style="padding:8px 12px;font-size:11px" onclick="approveAdminReq('${r.id}')"><i class="ti ti-check"></i>تایید و ساخت ادمین</button>
                   <button class="btn" style="padding:8px 12px;font-size:11px" onclick="rejectAdminReq('${r.id}')"><i class="ti ti-x"></i>رد</button>`;
      } else {
        statusHtml = `<span class="areq-status ${r.status}">${r.status==='approved'?'تایید شده':'رد شده'}</span>`;
      }
      return `<div class="areq-row">
        <div class="areq-info">
          <div class="areq-name">${escapeHtml(r.full_name||'-')}</div>
          <div class="areq-meta"><span><i class="ti ti-brand-telegram"></i>@${escapeHtml(r.telegram_id||'-')}</span><span><i class="ti ti-clock"></i>${escapeHtml(date)}</span></div>
          ${r.note ? `<div class="areq-note">${escapeHtml(r.note)}</div>` : ''}
        </div>
        <div class="areq-actions">${actions}${statusHtml}</div>
      </div>`;
    }).join('') : `<div class="areq-empty">درخواستی ثبت نشده است</div>`;
  }catch(e){ /* silent: پنل قدیمی‌تر ممکنه این endpoint رو نداشته باشه */ }
}
function approveAdminReq(id){
  const r = ADMIN_REQ_CACHE.find(x=>x.id===id); if(!r) return;
  const suggestedUser = (r.telegram_id||'admin').replace(/[^A-Za-z0-9_]/g,'').toLowerCase() || 'admin';
  openDrawer('تایید ادمین: ' + r.full_name, `
    <div class="grp"><label>درخواست‌کننده</label><input value="${escapeHtml(r.full_name)} (@${escapeHtml(r.telegram_id)})" disabled></div>
    <div class="grp"><label>نام کاربری</label><input id="arUser" value="${escapeHtml(suggestedUser)}"></div>
    <div class="grp"><label>رمز عبور</label><input id="arPass" value="${Math.random().toString(36).slice(-8)}"></div>
    <div class="grp"><label>شارژ اولیه (استارز)</label><input id="arCredit" type="number" min="0" value="0"></div>
    <div class="perm-grid">${Object.entries({dashboard:'داشبورد',inbounds:'ساخت و مدیریت اینباند',clients:'ساخت کلاینت (بخش جدا)',subscriptions:'سابسکریپشن',categories:'دسته‌بندی',plans:'پلن فروش',reports:'گزارش‌ها',messages:'پیام‌ها و خطاها',bot:'ربات',admins:'مدیریت حساب',settings:'تنظیمات'}).map(([k,v])=>`<label class="perm-item"><input type="checkbox" data-arperm="${k}" ${['dashboard','inbounds','subscriptions'].includes(k)?'checked':''}>${v}</label>`).join('')}</div>
  `, `<button class="btn primary" style="flex:1" onclick="confirmApproveAdminReq('${r.id}')"><i class="ti ti-check"></i>تایید و ساخت حساب</button>`);
}
async function confirmApproveAdminReq(id){
  try{
    const permissions=[...document.querySelectorAll('[data-arperm]:checked')].map(x=>x.dataset.arperm);
    const body={
      username: $('arUser').value.trim(),
      password: $('arPass').value,
      permissions,
      credit_stars: Number($('arCredit').value)||0,
    };
    const res = await api(`/api/admin-requests/${id}/approve`, {method:'POST', body: JSON.stringify(body)});
    closeDrawer();
    const msg = res.delivery_message || '';
    openDrawer('اطلاعات ورود ادمین', `
      <p style="font-size:11.5px;color:var(--sub);line-height:1.9">این متن را برای <b>@${escapeHtml(res.telegram_id||'')}</b> در تلگرام ارسال کن:</p>
      <textarea id="arDeliveryMsg" readonly style="width:100%;min-height:150px;background:var(--panel2);border:1px solid var(--line);color:var(--text);border-radius:12px;padding:12px;font:inherit;line-height:1.9">${escapeHtml(msg)}</textarea>
    `, `<button class="btn primary" style="flex:1" onclick="copyDeliveryMsg()"><i class="ti ti-copy"></i>کپی متن</button><button class="btn" style="flex:1" onclick="closeDrawer()">بستن</button>`);
    loadAdmins(); loadAdminRequests();
  }catch(e){ toast(e.message, false); }
}
function copyDeliveryMsg(){
  const el = document.getElementById('arDeliveryMsg');
  if(!el) return;
  el.select();
  try{ navigator.clipboard.writeText(el.value); toast('کپی شد ✓'); }catch(e){ document.execCommand('copy'); toast('کپی شد ✓'); }
}
async function rejectAdminReq(id){
  if(!confirm('این درخواست رد شود؟')) return;
  try{ await api(`/api/admin-requests/${id}/reject`, {method:'POST', body: JSON.stringify({})}); toast('درخواست رد شد'); loadAdminRequests(); }
  catch(e){ toast(e.message, false); }
}

// ============================================================
// ACTIVITY
// ============================================================
async function loadActivity(){
  try{
    const res = await api('/api/activity');
    $('activityBody').innerHTML = (res.logs||[]).slice().reverse().map(l=>`
      <tr><td class="mono">${(l.time||l.ts||'').toString().slice(0,16).replace('T',' ')}</td>
      <td><span class="badge ${l.level==='err'?'red':l.level==='warn'?'orange':'green'}">${l.type||l.kind||'—'}</span></td>
      <td>${escapeHtml(l.message||l.text||'')}</td></tr>
    `).join('') || `<tr><td colspan="3" class="empty">لاگی وجود ندارد</td></tr>`;
  }catch(e){ toast(e.message, false); }
}

// ============================================================
// MESSAGE CENTER
// ============================================================
function setMessageFilter(filter){
  MESSAGE_FILTER=filter;
  document.querySelectorAll('[data-message-filter]').forEach(b=>b.classList.toggle('on',b.dataset.messageFilter===filter));
  loadMessages();
}
function messageIcon(level, source){
  if(source==='client') return 'browser';
  if(level==='warn') return 'alert-triangle';
  if(level==='err') return 'alert-circle';
  return 'info-circle';
}
async function clearErrors(){
  if(!confirm(t('همه خطاهای ثبت‌شده پاک شوند؟'))) return;
  try{await api('/api/errors/clear',{method:'POST'});toast('خطاها پاک شدند ✓');loadMessages();}
  catch(e){toast(e.message,false);}
}
async function loadMessages(){
  try{
    const [er,act]=await Promise.all([api('/api/errors'),api('/api/activity')]);
    const errors=(er.errors||[]).slice().reverse();
    const filtered=errors.filter(x=>MESSAGE_FILTER==='all' || x.level===MESSAGE_FILTER || x.source===MESSAGE_FILTER);
    $('messageStats').innerHTML=`
      <div class="message-stat ${er.total_errors?'danger':'good'}"><div class="ms-icon"><i class="ti ti-alert-circle"></i></div><b>${Number(er.total_errors||0)}</b><small>کل خطاهای ثبت‌شده</small></div>
      <div class="message-stat warn"><div class="ms-icon"><i class="ti ti-alert-triangle"></i></div><b>${Number(er.warnings||0)}</b><small>هشدارهای اخیر</small></div>
      <div class="message-stat"><div class="ms-icon"><i class="ti ti-browser"></i></div><b>${Number(er.client_errors||0)}</b><small>خطاهای مرورگر</small></div>
      <div class="message-stat good"><div class="ms-icon"><i class="ti ti-heartbeat"></i></div><b>${er.healthy?'OK':'CHECK'}</b><small>وضعیت سیستم</small></div>`;
    $('nb-errors').textContent=String(Math.min(99,Number(er.total_errors||0)));
    $('nb-errors').style.display=Number(er.total_errors||0)?'inline-flex':'none';
    $('messageLastSync').textContent='آخرین بروزرسانی '+new Date().toLocaleTimeString('fa-IR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
    $('messageList').innerHTML=filtered.length?filtered.map(x=>{
      const lvl=x.level||'err'; const src=x.source||'server';
      return `<article class="message-row ${lvl}"><div class="mi"><i class="ti ti-${messageIcon(lvl,src)}"></i></div><div class="mt"><b>${escapeHtml(x.error||x.message||'خطای نامشخص')}</b><p>${escapeHtml(src==='client'?'Frontend / Browser':(x.method||'SERVER')+' · '+(x.path||''))}</p>${x.stack||x.details?`<div class="error-detail">${escapeHtml(x.stack||x.details||'')}</div>`:''}</div><div class="meta"><strong>${escapeHtml(x.time||'—')}</strong><span>${escapeHtml(src)}</span></div></article>`;
    }).join(''):`<div class="message-empty"><i class="ti ti-shield-check"></i>خطای ثبت‌شده‌ای وجود ندارد. سیستم سالم است.</div>`;
    const logs=(act.logs||[]).slice().reverse().slice(0,25);
    $('messageActivityList').innerHTML=logs.length?logs.map(l=>`<article class="message-row ${l.level==='err'?'err':l.level==='warn'?'warn':'ok'}"><div class="mi"><i class="ti ti-${l.level==='err'?'alert-circle':l.level==='warn'?'alert-triangle':'circle-check'}"></i></div><div class="mt"><b>${escapeHtml(l.message||l.text||'')}</b><p>${escapeHtml(l.kind||l.type||'system')}</p></div><div class="meta"><strong>${escapeHtml((l.time||l.ts||'').toString().replace('T',' ').slice(0,19))}</strong></div></article>`).join(''):'<div class="message-empty">رویدادی وجود ندارد.</div>';
  }catch(e){toast(e.message,false);reportClientError(e.message,'messages',{stack:e.stack});}
}
if(messageTimer) clearInterval(messageTimer);
let messagesTimer=setInterval(()=>{if(!document.hidden && CURRENT_PAGE==='messages') loadMessages()},15000);

// ============================================================
// SETTINGS
// ============================================================
function setBotDot(running){
  $('botDot').className = 'status-dot ' + (running?'on':'off');
  $('botStatusText').textContent = running ? 'ربات در حال اجراست' : 'ربات خاموش است';
  $('botStartBtn').disabled = !!running;
  $('botStopBtn').disabled = !running;
}
async function loadSettings(){
  try{
    const s = await api('/api/settings');
    $('setBaseUrl').value = s.public_base_url || '';
    if($('adminUsername')) $('adminUsername').value = s.admin_username || '';
    $('setTcpHost').value = s.tcp_public_host || '';
    $('setTcpPort').value = s.tcp_public_port || '';
    $('tcpListenHint').textContent = `سرور TCP روی پورت داخلی ${s.tcp_listen_port} گوش می‌دهد — این را در Railway به همین پورت داخلی متصل کن، نه به PORT اصلی HTTP.`;
    $('setBotToken').value = s.bot_token || '';
    $('setBotAdmins').value = s.bot_admin_ids || '';
    setBotDot(s.bot_running);
    if($('subTplName')) $('subTplName').checked = s.sub_remark_show_name !== false;
    if($('subTplVolume')) $('subTplVolume').checked = !!s.sub_remark_show_volume;
    if($('subTplId')) $('subTplId').checked = !!s.sub_remark_show_id;
    if($('subTplInbound')) $('subTplInbound').checked = !!s.sub_remark_show_inbound;
    if($('setSalesEnabled')) $('setSalesEnabled').checked = !!s.sales_enabled;
    if($('nameStyleEnabled')) $('nameStyleEnabled').checked = s.name_style_enabled !== false;
    updateBrandPreview();
    updateSubTemplatePreview();
    try{ const bt=await api('/api/bot/texts'); const x=bt.texts||{}; if($('botTxtWelcome'))$('botTxtWelcome').value=x.welcome||''; if($('botTxtAdmin'))$('botTxtAdmin').value=x.admin_menu||''; if($('botTxtCreated'))$('botTxtCreated').value=x.config_created||''; if($('botTxtStore'))$('botTxtStore').value=x.store_intro||''; if($('botTxtPayment'))$('botTxtPayment').value=x.payment_success||''; }catch(_){}
  }catch(e){ toast(e.message, false); }
}
function updateSubTemplatePreview(){
  const parts=[];
  if($('subTplName')?.checked) parts.push('MyConfig');
  if($('subTplVolume')?.checked) parts.push('50 GB');
  if($('subTplId')?.checked) parts.push('a1b2c3d4');
  if($('subTplInbound')?.checked) parts.push('Inbound-1');
  const el=$('subTplPreview'); if(el) el.textContent = parts.join(' | ') || 'MyConfig';
}
document.addEventListener('change', e=>{ if(['subTplName','subTplVolume','subTplId','subTplInbound'].includes(e.target?.id)) updateSubTemplatePreview(); });
async function saveSubTemplate(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({
      sub_remark_show_name: !!$('subTplName')?.checked,
      sub_remark_show_volume: !!$('subTplVolume')?.checked,
      sub_remark_show_id: !!$('subTplId')?.checked,
      sub_remark_show_inbound: !!$('subTplInbound')?.checked,
    })});
    toast('الگوی نام کانفیگ‌های ساب ذخیره شد ✓');
  }catch(e){ toast(e.message, false); }
}
async function saveTcpSettings(){
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({tcp_public_host: $('setTcpHost').value, tcp_public_port: $('setTcpPort').value})});
    toast('آدرس TCP ذخیره شد');
  }catch(e){ toast(e.message, false); }
}
async function saveSalesToggle(){
  const on = !!$('setSalesEnabled')?.checked;
  try{
    await api('/api/settings', {method:'POST', body: JSON.stringify({sales_enabled: on})});
    toast(on ? 'فروشگاه فعال شد ✓' : 'فروشگاه غیرفعال شد');
  }catch(e){ toast(e.message, false); $('setSalesEnabled').checked = !on; }
}
async function saveBaseUrl(){
  try{ await api('/api/settings', {method:'POST', body: JSON.stringify({public_base_url: $('setBaseUrl').value})}); toast('آدرس ذخیره شد'); refreshOverview(); }
  catch(e){ toast(e.message, false); }
}
async function saveBotSettings(){
  try{
    const r = await api('/api/settings', {method:'POST', body: JSON.stringify({bot_token: $('setBotToken').value, bot_admin_ids: $('setBotAdmins').value})});
    toast(r.bot_restarted ? 'ذخیره شد و ربات با تنظیمات جدید ری‌استارت شد' : 'ذخیره شد — برای اعمال، ربات را روشن کنید');
    setBotDot(r.running);
  }catch(e){ toast(e.message, false); }
}
async function botStart(){
  try{
    const r = await api('/api/settings/bot/start', {method:'POST'});
    toast(r.running ? 'ربات روشن شد ✓' : 'ربات روشن نشد', !!r.running);
    setBotDot(r.running);
  }
  catch(e){ toast(e.message, false); }
}
async function botStop(){
  try{ const r = await api('/api/settings/bot/stop', {method:'POST'}); toast('ربات خاموش شد'); setBotDot(r.running); }
  catch(e){ toast(e.message, false); }
}
async function saveBotTexts(){
  try{ await api('/api/bot/texts',{method:'POST',body:JSON.stringify({texts:{welcome:$('botTxtWelcome').value,admin_menu:$('botTxtAdmin').value,config_created:$('botTxtCreated').value,store_intro:$('botTxtStore').value,payment_success:$('botTxtPayment').value}})}); toast('متن‌های ربات ذخیره شد ✓'); }catch(e){toast(e.message,false)}
}
function toggleSettingsPass(id, btn){
  const inp = $(id);
  if(!inp) return;
  const icon = btn ? btn.querySelector('i') : null;
  if(inp.type === 'password'){ inp.type = 'text'; if(icon) icon.className = 'ti ti-eye-off'; }
  else { inp.type = 'password'; if(icon) icon.className = 'ti ti-eye'; }
}
function passwordMeter(){
  const val = $('newPass') ? $('newPass').value : '';
  const bar = $('passMeterBar'), hint = $('passHint');
  if(!bar) return;
  let score = 0;
  if(val.length >= 8) score++;
  if(val.length >= 12) score++;
  if(/[a-z]/.test(val) && /[A-Z]/.test(val)) score++;
  if(/[0-9]/.test(val)) score++;
  if(/[^A-Za-z0-9]/.test(val)) score++;
  const levels = [
    {pct:4,  color:'var(--bad)',  label:'خیلی ضعیف'},
    {pct:25, color:'var(--bad)',  label:'ضعیف'},
    {pct:50, color:'var(--warn)', label:'متوسط'},
    {pct:75, color:'var(--warn)', label:'خوب'},
    {pct:100,color:'var(--good)', label:'قوی'},
    {pct:100,color:'var(--good)', label:'خیلی قوی'},
  ];
  const lv = levels[Math.min(score, levels.length-1)];
  bar.style.width = (val ? lv.pct : 0) + '%';
  bar.style.background = lv.color;
  if(hint) hint.textContent = val ? `قدرت رمز: ${lv.label} — حداقل ۸ کاراکتر، ترکیب حروف بزرگ/کوچک، عدد و نماد پیشنهاد می‌شود.` : 'حداقل ۸ کاراکتر، ترجیحاً ترکیب حروف، عدد و نماد.';
}
async function revokeOtherSessions(){
  if(!confirm(t('همه نشست‌های قبلی این حساب لغو شوند؟'))) return;
  try{const r=await api('/api/security/revoke-other-sessions',{method:'POST'});toast(`${r.revoked||0} نشست قبلی لغو شد ✓`)}catch(e){toast(e.message,false)}
}
function fmtDiagBytes(n){return fmtBytes(Number(n||0))}
async function loadDiagnostics(){
  const box=$('diagGrid'), st=$('diagStatus'); if(!box) return;
  st.textContent='CHECKING'; st.className='badge orange';
  try{
    const d=await api('/api/system/diagnostics'); const r=d.resources||{}, o=d.objects||{}, b=d.bot||{}, sec=d.security||{};
    box.innerHTML=`<div class="diag-item"><small>Service</small><b>${escapeHtml(d.service?.status||'—')}</b><span>${escapeHtml(d.uptime||'—')}</span></div><div class="diag-item"><small>CPU</small><b>${Number(r.cpu_percent||0).toFixed(1)}%</b><span>Process load</span></div><div class="diag-item"><small>Memory</small><b>${Number(r.memory_percent||0).toFixed(1)}%</b><span>${fmtDiagBytes(r.memory_rss)}</span></div><div class="diag-item"><small>Disk</small><b>${Number(r.disk_percent||0).toFixed(1)}%</b><span>Root filesystem</span></div><div class="diag-item"><small>Inbounds</small><b>${o.inbounds||0}</b><span>${o.active_links||0} active</span></div><div class="diag-item"><small>Clients</small><b>${o.clients||0}</b><span>${o.subscriptions||0} subscriptions</span></div><div class="diag-item"><small>Bot</small><b>${b.running?'ONLINE':'OFFLINE'}</b><span>${b.admin_count||0} bot admins</span></div><div class="diag-item"><small>Sessions</small><b>${sec.session_count||0}</b><span>${escapeHtml(sec.username||'—')}</span></div>`;
    st.textContent='HEALTHY'; st.className='badge green';
  }catch(e){box.innerHTML=`<div class="diag-empty">${escapeHtml(e.message||'Diagnostics unavailable')}</div>`;st.textContent='ERROR';st.className='badge red';}
}

async function changeUsername(){
  const username = ($('adminUsername')?.value || '').trim();
  if(!username){ toast('نام کاربری را وارد کنید', false); return; }
  if(username.length < 3 || username.length > 40 || /\s/.test(username)){ toast('نام کاربری باید ۳ تا ۴۰ کاراکتر و بدون فاصله باشد', false); return; }
  const btn = document.activeElement && document.activeElement.tagName === 'BUTTON' ? document.activeElement : null; const originalHtml = btn ? btn.innerHTML : '';
  if(btn){ btn.disabled=true; btn.innerHTML='<i class="ti ti-loader-2 spin"></i>در حال ذخیره...'; }
  try{
    const r = await api('/api/change-username',{method:'POST',body:JSON.stringify({username})});
    if($('userName')) $('userName').textContent=r.username;
    if($('userChip')?.querySelector('.av')) $('userChip').querySelector('.av').textContent=(r.username||'?').slice(0,1).toUpperCase();
    toast('نام کاربری با موفقیت تغییر کرد ✓');
  }catch(e){ toast(e.message,false); }
  finally{ if(btn){btn.disabled=false;btn.innerHTML=originalHtml;} }
}
async function changePassword(){
  const current_password = $('curPass').value, new_password = $('newPass').value, repeat_password = $('repPass').value;
  if(!current_password || !new_password || !repeat_password){ toast('همه‌ی فیلدهای رمز عبور را پر کنید', false); return; }
  if(new_password.length < 8){ toast('رمز جدید باید حداقل ۸ کاراکتر باشد', false); return; }
  if(new_password !== repeat_password){ toast('تکرار رمز یکسان نیست', false); return; }
  if(new_password === current_password){ toast('رمز جدید باید با رمز فعلی متفاوت باشد', false); return; }
  const btn = document.activeElement && document.activeElement.tagName === 'BUTTON' ? document.activeElement : null;
  const originalHtml = btn ? btn.innerHTML : '';
  if(btn){ btn.disabled = true; btn.innerHTML = '<i class="ti ti-loader-2 spin"></i>در حال ذخیره...'; }
  try{
    await api('/api/change-password', {method:'POST', body: JSON.stringify({current_password, new_password, repeat_password})});
    toast('رمز عبور با موفقیت تغییر کرد ✓');
    $('curPass').value=$('newPass').value=$('repPass').value='';
    passwordMeter();
  }catch(e){ toast(e.message, false); }
  finally{ if(btn){ btn.disabled = false; btn.innerHTML = originalHtml; } }
}
</script>
</body>
</html>
"""


# ---- Untitled UI design system (applied to every page) ----
from untitled_ui import inject as _uui
LOGIN_HTML = _uui(LOGIN_HTML, "login")
DASHBOARD_HTML = _uui(DASHBOARD_HTML, "app")
