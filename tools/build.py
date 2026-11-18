# Збирає public/index.html (PWA для iPhone) з основної сторінки калькулятора.
import re, sys, json, os, hashlib
src = sys.argv[1]; out_dir = sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)

rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="theme-color" content="#17212b">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
    '<meta name="apple-mobile-web-app-title" content="АКБ 21700">\n'
    '<meta name="format-detection" content="telephone=no">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
    '<link rel="icon" type="image/png" href="icons/favicon.png">')
s = re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\s*<link href="https://fonts.googleapis.com/css2[^"]*" rel="stylesheet">',
    '<link rel="stylesheet" href="fonts.css">', s)
assert 'fonts.googleapis' not in s

# Додаткові стилі для iPhone
rep('</style>', '''
/* ---------- iPhone / PWA ---------- */
.wrap { padding-left: max(16px, env(safe-area-inset-left)); padding-right: max(16px, env(safe-area-inset-right));
        padding-top: max(20px, env(safe-area-inset-top)); padding-bottom: max(48px, calc(env(safe-area-inset-bottom) + 24px)); }
html { -webkit-text-size-adjust: 100%; }
body { -webkit-tap-highlight-color: transparent; overscroll-behavior-y: none; }
@media (pointer: coarse) {
  input, select, textarea { font-size: 16px; } /* iOS не збільшує сторінку при фокусі */
  textarea { min-height: 220px; }
  button { min-height: 40px; }
  button.chip { min-height: 34px; padding: 6px 11px; }
}
.install-hint { position: fixed; z-index: 50; left: max(12px, env(safe-area-inset-left)); right: max(12px, env(safe-area-inset-right));
  bottom: calc(env(safe-area-inset-bottom) + 12px); display: flex; gap: 10px; align-items: center;
  background: var(--panel); border: 1px solid var(--accent); border-radius: 12px; padding: 10px 10px 10px 14px;
  box-shadow: 0 8px 28px rgba(0,0,0,.18); font-size: 14px; }
.install-hint p { margin: 0; flex: 1; }
.install-hint svg { vertical-align: -3px; color: var(--accent); }
.install-hint button { flex: 0 0 auto; }
.offline-note { font: 600 12px var(--font-mono); color: var(--ok); }
</style>''')

# Реєстрація офлайн-кешу і підказка встановлення
rep('</body>', '''<script>
(function () {
  if ("serviceWorker" in navigator && window.isSecureContext) {
    window.addEventListener("load", function () { navigator.serviceWorker.register("sw.js").catch(function () {}); });
  }
  var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var standalone = navigator.standalone === true || (window.matchMedia && matchMedia("(display-mode: standalone)").matches);
  var seen = false; try { seen = localStorage.getItem("akb-install-hint") === "1"; } catch (e) {}
  if (!ios || standalone || seen) return;
  var el = document.createElement("div"); el.className = "install-hint"; el.setAttribute("role", "note");
  el.innerHTML = '<p>Встановіть як додаток: натисніть <svg width="16" height="16" viewBox="0 0 24 24" aria-label="Поділитися"><path d="M12 3v12M7 8l5-5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg> «Поділитися», потім <b>«На екран "Додому"»</b>.</p><button type="button">Зрозуміло</button>';
  el.querySelector("button").addEventListener("click", function () { el.remove(); try { localStorage.setItem("akb-install-hint", "1"); } catch (e) {} });
  document.body.appendChild(el);
})();
</script>
</body>''')

open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(s)

# Список файлів для офлайн-кешу й версія = хеш вмісту
files = []
for root, _, names in os.walk(out_dir):
    for n in sorted(names):
        rel = os.path.relpath(os.path.join(root, n), out_dir).replace(os.sep, "/")
        if rel in ("sw.js", "_headers"): continue
        files.append(rel)
files.sort()
h = hashlib.sha1()
for f in files: h.update(open(os.path.join(out_dir, f), "rb").read())
version = h.hexdigest()[:10]
sw = open(os.path.join(os.path.dirname(__file__), "sw.template.js"), encoding="utf-8").read()
sw = sw.replace("__VERSION__", version).replace("__FILES__", json.dumps(["./"] + files, ensure_ascii=False, indent=2))
open(os.path.join(out_dir, "sw.js"), "w", encoding="utf-8").write(sw)
print("версія кешу", version, "файлів", len(files))
