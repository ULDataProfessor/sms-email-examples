self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('fetch', event => {
  // basic offline caching
  event.respondWith(
    caches.open('club-cache').then(cache => {
      return cache.match(event.request).then(resp => {
        return resp || fetch(event.request).then(networkResp => {
          cache.put(event.request, networkResp.clone());
          return networkResp;
        });
      });
    })
  );
});
