# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SRC_HTML = Path(r"C:\Users\crist\.gemini\antigravity\scratch\bonos.html\view-source_https___boneriolocal.com.ar.html")
OUT_DIR = Path(r"C:\Users\crist\.gemini\antigravity\scratch\alphabonos")
OUT_HTML = OUT_DIR / "index.html"
LIC_HTML = OUT_DIR / "licitaciones.html"

raw = SRC_HTML.read_text(encoding="utf-8", errors="ignore")

# 1. Remove auth.js and serviceWorker registration
raw = raw.replace('<script src="/auth.js?v=19"></script>', '<!-- auth.js removed for AlphaBonos -->')
raw = raw.replace(
    "if ('serviceWorker' in navigator) addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });",
    "/* serviceWorker disabled */"
)

# 2. Keep Cauciones & Book endpoints functional via worker URL, while live bond/note/corp quotes come 100% live from data912 without 20m delay
WORKER_URL = "https://bonerio-vivo.persijuanluis.workers.dev"
raw = raw.replace(
    "if (!window.BL_LIVE || !isAct() || !TJ) return; fetch(window.BL_LIVE.replace(/\\/+$/, '') + '/caucion'",
    f"if (!isAct() || !TJ) return; fetch('{WORKER_URL}/caucion'"
)
raw = raw.replace(
    "var B0 = window.BL_LIVE.replace(/\\/+$/, ''), td0 = todayBA();",
    f"var B0 = '{WORKER_URL}', td0 = todayBA();"
)
raw = raw.replace(
    "if (window.BL_LIVE && Date.now() - CVt > 6e4) { CVt = Date.now(); fetch(window.BL_LIVE.replace(/\\/+$/, '') + '/caucion'",
    f"if (Date.now() - CVt > 6e4) {{ CVt = Date.now(); fetch('{WORKER_URL}/caucion'"
)
raw = raw.replace(
    "window.BL_LIVE = 'https://bonerio-vivo.persijuanluis.workers.dev';",
    "window.BL_LIVE = '';"
)

# 3. Remove Acciones (acc) and Consultame (cons) buttons from #topbar .tabs
raw = raw.replace(
    """      <button class="tab-btn" onclick="if(window.switchTab) window.switchTab('acc')">Acciones</button>\n""",
    ""
)
raw = raw.replace(
    """      <button class="tab-btn" onclick="if(window.switchTab) window.switchTab('cons')">Consultame</button>\n""",
    ""
)

# 4. Remove Acciones and Consultame from #sideNav GR array
raw = raw.replace(
    "{ h: 'Acciones' }, ['acc', 'Acciones'], ",
    ""
)
raw = raw.replace(
    ", { sep: 1 }, ['cons', 'Consultame']];",
    "];"
)

# 5. Remove 'acc' from filter arrays in Variación Diaria, Volumen, and Resumen
raw = raw.replace(
    "var ORDER = ['usd', 'fija', 'cer', 'tamar', 'dl', 'dual', 'on', 'pv', 'acc'];",
    "var ORDER = ['usd', 'fija', 'cer', 'tamar', 'dl', 'dual', 'on', 'pv'];"
)
raw = raw.replace(
    "var FORD = ['fija', 'cer', 'tamar', 'dl', 'dual', 'bonar', 'glob', 'bop', 'on', 'pv', 'oth', 'acc'];",
    "var FORD = ['fija', 'cer', 'tamar', 'dl', 'dual', 'bonar', 'glob', 'bop', 'on', 'pv', 'oth'];"
)
raw = raw.replace(
    "['on', 'ONs'], ['acc', 'Acciones']];",
    "['on', 'ONs']];"
)
raw = raw.replace(
    ".concat(['usd', 'fija', 'cer', 'tamar', 'dl', 'acc'].map(",
    ".concat(['usd', 'fija', 'cer', 'tamar', 'dl'].map("
)
raw = raw.replace(
    "var FS = ['usd', 'fija', 'cer', 'tamar', 'dl', 'dual', 'acc'].map(",
    "var FS = ['usd', 'fija', 'cer', 'tamar', 'dl', 'dual'].map("
)

# 6. Remove <div id="acc" class="tab-content"></div>
raw = raw.replace('<div id="acc" class="tab-content"></div>', '<!-- acc removed -->')

# 7. Neutralize Bonerío PRO paywall, MSCI Merval ETF, ETF MERV options, and WhatsApp button at the end of the file
cut_marker = "/* ---------- Bonerío PRO: secciones gratis y el resto con candado (popup para suscribirse) ----------"
if cut_marker in raw:
    prefix = raw.split(cut_marker)[0]
    raw = prefix + """/* ---------- AlphaBonos: Acceso Completo Desbloqueado (Sin Paywall ni Acciones) ---------- */
window.BLPRO = function () { return true; };
window.BLPROPOP = function () {};
window.ACCQ = null;
</script>
</body>
</html>
"""

# 8. Replace the old BL canvas watermark with the custom AlphaBonos x AlphaQuant AB vector watermark
old_brandmark = """    ctx.save(); ctx.translate(lx, ly); ctx.scale(logo / 64, logo / 64);
    ctx.fillStyle = '#0a0a0b'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(0, 0, 64, 64, 14); else ctx.rect(0, 0, 64, 64); ctx.fill();
    ctx.save(); ctx.translate(13, 12); ctx.scale(0.5, 0.5); ctx.strokeStyle = '#f6b40e'; ctx.lineWidth = 9;
    ['M4.5 0 V56', 'M4.5 4.5 H20 A10.5 10.5 0 0 1 20 25.5 H4.5', 'M4.5 25.5 H22 A13 13 0 0 1 22 51.5 H4.5', 'M50.5 0 V56', 'M46 51.5 H76'].forEach(function(d) { ctx.stroke(new Path2D(d)); });
    ctx.restore();
    ctx.fillStyle = '#75aadb'; ctx.fillRect(12, 47, 40, 3.6); ctx.fillStyle = '#fff'; ctx.fillRect(12, 52, 40, 3.6);
    ctx.restore();"""

new_brandmark = """    ctx.save(); ctx.translate(lx, ly); ctx.scale(logo / 64, logo / 64);
    ctx.fillStyle = '#120926'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(0, 0, 64, 64, 15); else ctx.rect(0, 0, 64, 64); ctx.fill();
    ctx.strokeStyle = '#a855f7'; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle = '#d8b4fe'; ctx.font = '900 26px "Bricolage Grotesque", Inter, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('AB', 32, 30);
    ctx.fillStyle = '#a855f7'; ctx.fillRect(12, 49, 26, 4); ctx.fillStyle = '#38bdf8'; ctx.fillRect(40, 49, 12, 4);
    ctx.restore();"""

raw = raw.replace(old_brandmark, new_brandmark)
raw = raw.replace("const label = 'Bonerío Local';", "const label = 'AlphaBonos · AlphaQuant';")

# 9. Replace Sidebar Header & Main H1 with AlphaBonos x AlphaQuant lockup
raw = raw.replace(
    """sn.innerHTML = '<div class="sn-h"><img src="/favicon.svg?v=2" alt=""><b>BONERÍO LOCAL</b></div><nav>'""",
    """sn.innerHTML = '<div class="sn-h"><img src="/favicon.svg?v=3" alt=""><div class="sn-brand"><b>ALPHA<span class="ac-grad">BONOS</span></b><small>BY ALPHAQUANT</small></div></div><nav>'"""
)
raw = raw.replace('/favicon.svg?v=2', '/favicon.svg?v=3')
raw = raw.replace(
    "<h1>Bonerío Local: Terminal Analítica</h1>",
    '<h1><span class="tt">Alpha<span class="ac-grad">Bonos</span> <span class="aq-pill">BY ALPHAQUANT</span></span></h1>'
)
raw = raw.replace("<title>Bonerío Local: Terminal Analítica</title>", "<title>AlphaBonos · by AlphaQuant | Terminal de Renta Fija & Macro</title>")
raw = raw.replace('<meta name="theme-color" content="#0a0a0b">', '<meta name="theme-color" content="#0b0718">')

# Harmonize Chart.js internal grid, tooltip, and theme color maps with the Violet / Lavender palette
raw = raw.replace(
    "var V = {}, VK = '', TX = { '#f4f4f5': 1, '#141414': 1, '#a1a1aa': 1, '#5f5f68': 1 }, BD = { '#232326': 1, '#e4e4e0': 1 };",
    "var V = {}, VK = '', TX = { '#f4f4f5': 1, '#141414': 1, '#a1a1aa': 1, '#5f5f68': 1, '#f5f3ff': 1, '#1b1035': 1, '#9e91c7': 1, '#62518a': 1 }, BD = { '#232326': 1, '#e4e4e0': 1, '#281d4a': 1, '#dcd3f2': 1 };"
)
raw = raw.replace(
    "V.grid = V.light ? 'rgba(20,20,20,.07)' : 'rgba(255,255,255,.06)';",
    "V.grid = V.light ? 'rgba(109,40,217,.08)' : 'rgba(168,85,247,.09)';"
)
raw = raw.replace(
    "T.backgroundColor = function () { return vars().light ? 'rgba(255,255,255,.97)' : 'rgba(24,24,26,.96)'; };",
    "T.backgroundColor = function () { return vars().light ? 'rgba(255,255,255,.97)' : 'rgba(19,13,38,.96)'; };"
)

# 10. Inject Custom Violet Dark Mode & Lavender-Pearl Light Mode Palette
custom_theme_css = """
<style id="alphaQuantVioletTheme">
/* ==========================================================================
   ALPHABONOS × ALPHAQUANT — IDENTIDAD VISUAL PROPIA
   Modo Oscuro: Obsidian Amethyst & Electric Violet
   Modo Claro : Nordic Lavender Pearl & Royal Indigo
   ========================================================================== */
:root {
  --bg: #0b0716 !important;
  --card: #130d26 !important;
  --tx: #f5f3ff !important;
  --mu: #9e91c7 !important;
  --bd: #281d4a !important;
  --ac: #a855f7 !important;
  --acx: #ffffff !important;
  --ok: #2dd4bf !important;
  --bad: #fb7185 !important;
  --pill: #1b1336 !important;
  --pillb: #352563 !important;
  /* Familias de curvas armonizadas con la impronta AlphaQuant */
  --c-fija: #e879f9 !important;
  --c-cer: #2dd4bf !important;
  --c-tam: #fb7185 !important;
  --c-dl: #38bdf8 !important;
  --c-dual: #a78bfa !important;
  --c-cer-k: #14b8a6 !important;
  --c-on: #f472b6 !important;
  --c-pv: #fbbf24 !important;
  --c-usd: #a3e635 !important;
  --c-s1: #38bdf8 !important;
  --c-s2: #c084fc !important;
}

[data-theme="light"] {
  --bg: #f3effb !important;
  --card: #ffffff !important;
  --tx: #1b1035 !important;
  --mu: #62518a !important;
  --bd: #dcd3f2 !important;
  --ac: #7c3aed !important;
  --acx: #ffffff !important;
  --ok: #0d9488 !important;
  --bad: #e11d48 !important;
  --pill: #eae3f8 !important;
  --pillb: #cfc2eb !important;
  /* Familias de curvas en modo claro editorial */
  --c-fija: #9333ea !important;
  --c-cer: #0f766e !important;
  --c-tam: #be185d !important;
  --c-dl: #0284c7 !important;
  --c-dual: #4f46e5 !important;
  --c-cer-k: #0f766e !important;
  --c-on: #a21caf !important;
  --c-pv: #d97706 !important;
  --c-usd: #4d7c0f !important;
  --c-s1: #0284c7 !important;
  --c-s2: #7c3aed !important;
}

/* Fondo con atmósfera sutil violeta/índigo */
body {
  background-color: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -15%, rgba(168, 85, 247, 0.16), transparent 70%),
    radial-gradient(ellipse 50% 40% at 95% 10%, rgba(56, 189, 248, 0.08), transparent 65%) !important;
  background-attachment: fixed !important;
}
[data-theme="light"] body {
  background-color: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -15%, rgba(124, 58, 237, 0.11), transparent 70%),
    radial-gradient(ellipse 50% 40% at 95% 10%, rgba(14, 165, 233, 0.08), transparent 65%) !important;
  background-attachment: fixed !important;
}

/* Tarjetas con relieve sutil y bordes amatista */
.card {
  background: linear-gradient(180deg, rgba(168, 85, 247, 0.04) 0%, rgba(19, 13, 38, 0) 160px), var(--card) !important;
  border: 1px solid var(--bd) !important;
  box-shadow: 0 10px 30px -12px rgba(7, 3, 18, 0.65) !important;
}
[data-theme="light"] .card {
  background: linear-gradient(180deg, rgba(124, 58, 237, 0.03) 0%, rgba(255, 255, 255, 0) 140px), var(--card) !important;
  border: 1px solid var(--bd) !important;
  box-shadow: 0 8px 24px -8px rgba(91, 33, 182, 0.08) !important;
}

/* Menú lateral (Sidebar) con identidad AlphaQuant */
#sideNav {
  background: linear-gradient(180deg, #0e081f 0%, #090514 100%) !important;
  border-right: 1px solid var(--bd) !important;
  box-shadow: 6px 0 28px -10px rgba(0, 0, 0, 0.6) !important;
}
[data-theme="light"] #sideNav {
  background: linear-gradient(180deg, #faf8ff 0%, #efeaf9 100%) !important;
  border-right: 1px solid var(--bd) !important;
  box-shadow: 6px 0 24px -10px rgba(109, 40, 217, 0.09) !important;
}
#sideNav .sn-h {
  padding: 16px 16px 14px !important;
  background: linear-gradient(90deg, rgba(168, 85, 247, 0.10), transparent) !important;
}
#sideNav .sn-h img {
  width: 34px !important;
  height: 34px !important;
  border-radius: 9px !important;
  box-shadow: 0 0 14px rgba(168, 85, 247, 0.35) !important;
}
#sideNav .sn-brand {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
  min-width: 0;
}
#sideNav .sn-brand b {
  font-family: var(--fh);
  font-size: 16px !important;
  font-weight: 800 !important;
  letter-spacing: 0.04em !important;
  color: var(--tx) !important;
}
#sideNav .sn-brand small {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #38bdf8;
  margin-top: 3px;
  text-transform: uppercase;
}
[data-theme="light"] #sideNav .sn-brand small {
  color: #6d28d9;
}
body.sn-mini #sideNav .sn-brand {
  display: none !important;
}

/* Gradiente de marca en texto y pill superior */
.ac-grad {
  background: linear-gradient(135deg, #e879f9 0%, #a855f7 50%, #38bdf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
[data-theme="light"] .ac-grad {
  background: linear-gradient(135deg, #9333ea 0%, #6d28d9 55%, #0284c7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.aq-pill {
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 10px;
  margin-left: 8px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.18), rgba(56, 189, 248, 0.14));
  border: 1px solid rgba(168, 85, 247, 0.4);
  color: #e9d5ff;
}
[data-theme="light"] .aq-pill {
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(2, 132, 199, 0.10));
  border: 1px solid rgba(124, 58, 237, 0.35);
  color: #5b21b6;
}

/* Botones activos e ítems seleccionados con gradiente institucional Violeta-Índigo */
.seg button.on,
#home .hm-per button.on,
#qvP .f button.on,
.rp button.on,
#dash .dbC button.on,
#dash .dbL button.on,
#sideNav .sn-it.on,
.tab-btn.active {
  background: linear-gradient(135deg, #9333ea 0%, #6366f1 100%) !important;
  border-color: #a855f7 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px -2px rgba(147, 51, 234, 0.45) !important;
}
[data-theme="light"] .seg button.on,
[data-theme="light"] #home .hm-per button.on,
[data-theme="light"] #qvP .f button.on,
[data-theme="light"] .rp button.on,
[data-theme="light"] #dash .dbC button.on,
[data-theme="light"] #dash .dbL button.on,
[data-theme="light"] #sideNav .sn-it.on,
[data-theme="light"] .tab-btn.active {
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
  border-color: #6d28d9 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px -2px rgba(124, 58, 237, 0.35) !important;
}

#sideNav .sn-it:hover {
  background: rgba(168, 85, 247, 0.12) !important;
  color: var(--tx) !important;
}
[data-theme="light"] #sideNav .sn-it:hover {
  background: rgba(124, 58, 237, 0.10) !important;
  color: var(--tx) !important;
}

/* Hover de tarjetas en el Inicio y controles */
#home .hm-t:hover, #home .hm-q button:hover {
  border-color: var(--ac) !important;
  box-shadow: 0 8px 24px -6px rgba(168, 85, 247, 0.25) !important;
}
select:hover, input[type=number]:hover, input[type=date]:hover, button.act:hover {
  border-color: var(--ac) !important;
}

/* Botón flotante de acceso rápido (#qvB) */
#qvB {
  background: linear-gradient(135deg, #1b1035, #0f0822) !important;
  border: 1.5px solid #a855f7 !important;
  box-shadow: 0 8px 24px rgba(147, 51, 234, 0.4) !important;
}
[data-theme="light"] #qvB {
  background: linear-gradient(135deg, #ffffff, #f3effb) !important;
  border: 1.5px solid #7c3aed !important;
  box-shadow: 0 8px 22px rgba(124, 58, 237, 0.25) !important;
}

/* Barras de desplazamiento violetas */
* { scrollbar-color: rgba(168, 85, 247, 0.4) transparent !important; }
*::-webkit-scrollbar-thumb { background: rgba(168, 85, 247, 0.4) !important; background-clip: padding-box !important; }
*::-webkit-scrollbar-thumb:hover { background: rgba(168, 85, 247, 0.75) !important; background-clip: padding-box !important; }

/* ==========================================================================
   LAYOUT WIDESCREEN FULL-SPACE (100% PANTALLA, SIN ZOOM ACHICADO NI CAJAS ANGOSTAS)
   ========================================================================== */
html {
  zoom: 1 !important;
}
:root {
  --snw: 300px !important;
}
body.sn-mini {
  --snw: 76px !important;
}
main {
  max-width: 100% !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 22px 30px 44px !important;
  box-sizing: border-box !important;
}
@media (max-width: 900px) {
  main {
    padding: 16px 14px 40px !important;
  }
}

/* Menú lateral más amplio, cómodo y con mayor presencia visual */
#sideNav .sn-h {
  min-height: 76px !important;
  padding: 18px 20px 16px !important;
  gap: 13px !important;
}
#sideNav .sn-h img {
  width: 40px !important;
  height: 40px !important;
  border-radius: 11px !important;
}
#sideNav .sn-brand b {
  font-size: 18px !important;
  letter-spacing: 0.05em !important;
}
#sideNav .sn-brand small {
  font-size: 10.5px !important;
  margin-top: 4px !important;
}
#sideNav nav {
  padding: 14px 14px !important;
}
#sideNav .sn-hd {
  margin: 18px 14px 7px !important;
  font-size: 12px !important;
  letter-spacing: 0.1em !important;
  color: var(--ac) !important;
  opacity: 0.95 !important;
}
#sideNav .sn-it {
  padding: 11px 14px !important;
  margin: 3px 0 !important;
  border-radius: 12px !important;
  font-size: 15px !important;
  gap: 13px !important;
}
#sideNav .sn-it svg {
  width: 21px !important;
  height: 21px !important;
}
#sideNav .sn-sub {
  margin: 2px 0 8px 24px !important;
  padding-left: 10px !important;
}
#sideNav .sn-sub .sn-it {
  padding: 9px 12px !important;
  font-size: 14px !important;
}

/* Tarjetas, tablas y gráficos expandidos a todo el ancho disponible */
.card {
  padding: 24px 28px !important;
  border-radius: 22px !important;
  margin-bottom: 22px !important;
}
table {
  width: 100% !important;
}
.qx .qc.mid,
#pesos .qc.mid {
  max-width: none !important;
  width: 100% !important;
}
#home .hm-k {
  gap: 18px !important;
  margin-bottom: 20px !important;
}
#home .hm-t {
  padding: 18px 22px 14px !important;
  border-radius: 20px !important;
}
#home .hm-g,
#home .hm-g3 {
  gap: 20px !important;
  margin-bottom: 20px !important;
}
#home .hm-ch {
  height: 360px !important;
}
#home .hm-ch.s {
  min-height: 285px !important;
}
#home .hm-q {
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)) !important;
  gap: 16px !important;
}
#alert #alCard .dbF {
  max-width: none !important;
}
</style>
"""

raw = raw.replace("</head>", custom_theme_css + "\n</head>", 1)

# 11. Rebrand remaining strings
raw = raw.replace("Bonerío Local", "AlphaBonos")
raw = raw.replace("Bonerío", "AlphaBonos")
raw = raw.replace("boneriolocal.com.ar", "alphabonos.local")
raw = raw.replace("Bonerio_", "AlphaBonos_")
raw = raw.replace("Soberanos_", "AlphaBonos_")

# Custom footer
old_footer_re = re.compile(r'<footer id="siteFooter">.*?</footer>', re.DOTALL)
new_footer = """<footer id="siteFooter">
  <div class="ft"><b>AlphaBonos · by AlphaQuant</b> — Terminal Analítica de Renta Fija, Curvas, Tasas y Contexto Macro Local · Precios en vivo vía BYMA / data912.</div>
  <div class="ft" style="margin-top:6px">© <span id="fYear">2026</span> AlphaQuant &amp; AlphaBonos. Uso exclusivo personal e institucional.</div>
  <script>try{document.getElementById('fYear').textContent=new Date().getFullYear()}catch(e){}</script>
</footer>"""
raw = old_footer_re.sub(new_footer, raw)

OUT_HTML.write_text(raw, encoding="utf-8")
print(f"[OK] Wrote {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")

# 12. Also apply the Violet Dark / Lavender Light theme & new AB watermark to licitaciones.html
if LIC_HTML.exists():
    lic = LIC_HTML.read_text(encoding="utf-8", errors="ignore")
    lic = lic.replace("Bonerío Local", "AlphaBonos")
    lic = lic.replace("Bonerío", "AlphaBonos")
    lic = lic.replace("Bonerio_", "AlphaBonos_")
    lic = lic.replace("Soberanos_Licitaciones_", "AlphaBonos_Licitaciones_")
    # Replace root and light theme variables in licitaciones.html
    lic = re.sub(
        r":root\{--bg:#[0-9a-fA-F]+;--card:#[0-9a-fA-F]+;--tx:#[0-9a-fA-F]+;--mu:#[0-9a-fA-F]+;--bd:#[0-9a-fA-F]+;--ac:#[0-9a-fA-F]+;--acx:#[0-9a-fA-F]+;--ok:#[0-9a-fA-F]+;--bad:#[0-9a-fA-F]+;",
        ":root{--bg:#0b0716;--card:#130d26;--tx:#f5f3ff;--mu:#9e91c7;--bd:#281d4a;--ac:#a855f7;--acx:#ffffff;--ok:#2dd4bf;--bad:#fb7185;",
        lic
    )
    lic = re.sub(
        r"--soft:#18181b\}",
        "--soft:#1b1336}",
        lic
    )
    lic = re.sub(
        r'\[data-theme="light"\]\{--bg:#[0-9a-fA-F]+;--card:#[0-9a-fA-F]+;--tx:#[0-9a-fA-F]+;--mu:#[0-9a-fA-F]+;--bd:#[0-9a-fA-F]+;--ac:#[0-9a-fA-F]+;--acx:#[0-9a-fA-F]+;--ok:#[0-9a-fA-F]+;--bad:#[0-9a-fA-F]+;',
        '[data-theme="light"]{--bg:#f3effb;--card:#ffffff;--tx:#1b1035;--mu:#62518a;--bd:#dcd3f2;--ac:#7c3aed;--acx:#ffffff;--ok:#0d9488;--bad:#e11d48;',
        lic
    )
    lic = re.sub(
        r"--soft:#f4f4f2\}",
        "--soft:#eae3f8}",
        lic
    )
    lic = lic.replace(
        "main{max-width:1180px;margin:0 auto;padding:24px 16px 48px}",
        "main{max-width:100%;width:100%;margin:0;padding:20px 24px 48px}"
    )
    # Replace old BL vector watermark in licitaciones.html
    old_lic_brand = """    ctx.save(); ctx.translate(lx, ly); ctx.scale(logo / 64, logo / 64); ctx.fillStyle = '#1c1917'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(0, 0, 64, 64, 14); else ctx.rect(0, 0, 64, 64); ctx.fill();
    ctx.save(); ctx.translate(13, 12); ctx.scale(0.5, 0.5); ctx.strokeStyle = '#f6b40e'; ctx.lineWidth = 9;
    ['M4.5 0 V56', 'M4.5 4.5 H20 A10.5 10.5 0 0 1 20 25.5 H4.5', 'M4.5 25.5 H22 A13 13 0 0 1 22 51.5 H4.5', 'M50.5 0 V56', 'M46 51.5 H76'].forEach(function (d) { ctx.stroke(new Path2D(d)); });
    ctx.restore(); ctx.fillStyle = '#75aadb'; ctx.fillRect(12, 47, 40, 3.6); ctx.fillStyle = '#fff'; ctx.fillRect(12, 52, 40, 3.6); ctx.restore();"""
    new_lic_brand = """    ctx.save(); ctx.translate(lx, ly); ctx.scale(logo / 64, logo / 64); ctx.fillStyle = '#120926'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(0, 0, 64, 64, 15); else ctx.rect(0, 0, 64, 64); ctx.fill();
    ctx.strokeStyle = '#a855f7'; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle = '#d8b4fe'; ctx.font = '900 26px "Bricolage Grotesque", Inter, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('AB', 32, 30);
    ctx.fillStyle = '#a855f7'; ctx.fillRect(12, 49, 26, 4); ctx.fillStyle = '#38bdf8'; ctx.fillRect(40, 49, 12, 4); ctx.restore();"""
    lic = lic.replace(old_lic_brand, new_lic_brand)
    LIC_HTML.write_text(lic, encoding="utf-8")
    print(f"[OK] Styled {LIC_HTML} ({LIC_HTML.stat().st_size:,} bytes)")
