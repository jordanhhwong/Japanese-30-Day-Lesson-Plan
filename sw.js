// ── Japanese Holiday Coach — Service Worker ───────────────────────────────────
// Strategy:
//   Core assets (HTML, manifest, icon):  network-first, cache fallback
//   Audio MP3 files (audio/*.mp3):       cache-first, network fallback
//   Google Fonts:                         cache-first
//   Everything else:                      network-only (TTS, speech APIs)

const CORE_CACHE  = 'jp-core-v1';
const AUDIO_CACHE = 'jp-audio-v1';

// Files cached immediately on install
const CORE_ASSETS = [
  './japanese_coach.html',
  './manifest.json',
  './icon.svg',
];

// ── Install ───────────────────────────────────────────────────────────────────
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CORE_CACHE)
      .then(cache => cache.addAll(CORE_ASSETS))
      .then(() => self.skipWaiting())   // activate immediately
  );
});

// ── Activate ──────────────────────────────────────────────────────────────────
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(k => k !== CORE_CACHE && k !== AUDIO_CACHE)
          .map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())  // take control of open pages
  );
});

// ── Fetch ─────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // 1. Audio MP3 files — cache-first (local repo files, same origin)
  if (url.pathname.includes('/audio/') && url.pathname.endsWith('.mp3')) {
    e.respondWith(
      caches.open(AUDIO_CACHE).then(cache =>
        cache.match(e.request).then(cached => {
          if (cached) return cached;
          return fetch(e.request)
            .then(res => {
              if (res && res.ok) cache.put(e.request, res.clone());
              return res;
            })
            .catch(() => cached || new Response('', { status: 404 }));
        })
      )
    );
    return;
  }

  // 2. Google Fonts — cache-first (avoid re-downloading on every load)
  if (url.hostname.endsWith('googleapis.com') || url.hostname.endsWith('gstatic.com')) {
    e.respondWith(
      caches.open(CORE_CACHE).then(cache =>
        cache.match(e.request).then(cached => {
          if (cached) return cached;
          return fetch(e.request)
            .then(res => {
              if (res && res.ok) cache.put(e.request, res.clone());
              return res;
            })
            .catch(() => cached);
        })
      )
    );
    return;
  }

  // 3. Main HTML — network-first so updates propagate, cache as fallback
  if (e.request.mode === 'navigate' || url.pathname.endsWith('.html')
      || url.pathname.endsWith('/') || url.pathname.endsWith('.json')
      || url.pathname.endsWith('.svg')) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          caches.open(CORE_CACHE).then(c => c.put(e.request, res.clone()));
          return res;
        })
        .catch(() =>
          caches.match(e.request)
            .then(c => c || caches.match('./japanese_coach.html'))
        )
    );
    return;
  }

  // 4. Everything else (TTS, speech API, etc.) — network only, no caching
  //    These require live internet by nature and should fail gracefully.
});
