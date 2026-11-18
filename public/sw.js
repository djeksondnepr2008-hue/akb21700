// Офлайн-кеш «Збірка АКБ 21700». Версія змінюється автоматично при кожній збірці (tools/build.py).
const CACHE = "akb21700-e119b29955";
const FILES = [
  "./",
  "fonts.css",
  "fonts/archivo.woff2",
  "fonts/plex-mono-400.woff2",
  "fonts/plex-mono-600.woff2",
  "fonts/plex-mono-700.woff2",
  "fonts/plex-sans.woff2",
  "icons/apple-touch-icon.png",
  "icons/favicon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  "index.html",
  "manifest.webmanifest"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});
// Спершу кеш (миттєвий старт і робота без мережі), паралельно оновлюємо з мережі
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const hit = await cache.match(e.request, { ignoreSearch: true });
    const net = fetch(e.request).then((r) => { if (r.ok) cache.put(e.request, r.clone()); return r; }).catch(() => null);
    if (hit) { e.waitUntil(net); return hit; }
    return (await net) || (await cache.match("./")) || Response.error();
  })());
});
