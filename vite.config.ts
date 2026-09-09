import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// SharedArrayBuffer (used by the Python terminal worker for blocking stdin)
// is only exposed to cross-origin isolated documents.
const crossOriginIsolationHeaders = {
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Embedder-Policy': 'credentialless',
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: { headers: crossOriginIsolationHeaders },
  preview: { headers: crossOriginIsolationHeaders },
  worker: { format: 'es' },
})
