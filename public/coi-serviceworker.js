/*
 * Cross-origin isolation shim.
 *
 * SharedArrayBuffer -- which the Python terminal uses to give Python a real
 * blocking input() -- is only handed to documents that are cross-origin
 * isolated, and that requires COOP/COEP response headers. Static hosts like
 * GitHub Pages don't let you set headers, so this service worker re-serves
 * every response with them attached.
 *
 * The dev/preview server sets the headers natively (see vite.config.ts), so
 * this only does real work in production.
 */

if (typeof window === 'undefined') {
  // ---- service worker side ----
  self.addEventListener('install', () => self.skipWaiting())

  self.addEventListener('activate', (event) => event.waitUntil(self.clients.claim()))

  self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'deregister') {
      self.registration
        .unregister()
        .then(() => self.clients.matchAll())
        .then((clients) => clients.forEach((client) => client.navigate(client.url)))
    }
  })

  self.addEventListener('fetch', (event) => {
    const request = event.request

    // Range requests replayed from the cache must be left alone.
    if (request.cache === 'only-if-cached' && request.mode !== 'same-origin') return

    event.respondWith(
      fetch(request.mode === 'no-cors' ? new Request(request, { credentials: 'omit' }) : request)
        .then((response) => {
          // Opaque responses carry no headers worth rewriting.
          if (response.status === 0) return response

          const headers = new Headers(response.headers)
          headers.set('Cross-Origin-Embedder-Policy', 'credentialless')
          headers.set('Cross-Origin-Opener-Policy', 'same-origin')

          return new Response(response.body, {
            status: response.status,
            statusText: response.statusText,
            headers,
          })
        })
        .catch((error) => {
          console.error('[coi-serviceworker]', error)
          throw error
        }),
    )
  })
} else {
  // ---- page side ----
  ;(() => {
    // Already isolated (the server sent the headers itself) -- nothing to do.
    if (window.crossOriginIsolated !== false) return
    if (!window.isSecureContext || !navigator.serviceWorker) return

    // Resolved from the script's own URL so this keeps working under a
    // project sub-path (e.g. GitHub Pages at /GSU-Portfolio/).
    const scriptUrl = document.currentScript && document.currentScript.src
    if (!scriptUrl) return

    navigator.serviceWorker
      .register(scriptUrl, { scope: new URL('./', scriptUrl).pathname })
      .then((registration) => {
        // The worker only governs responses fetched after it took control, so
        // the very first load has to be reloaded once to become isolated.
        registration.addEventListener('updatefound', () => window.location.reload())
        if (registration.active && !navigator.serviceWorker.controller) window.location.reload()
      })
      .catch((error) => console.error('[coi-serviceworker] registration failed', error))
  })()
}
