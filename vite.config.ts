import { cpSync } from 'node:fs'
import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'

// SharedArrayBuffer (used by the Python terminal worker for blocking stdin)
// is only exposed to cross-origin isolated documents.
const crossOriginIsolationHeaders = {
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Embedder-Policy': 'credentialless',
}

// Course folders that are linked to as plain static sites rather than rendered
// by the app. The dev server already serves them from the project root; this
// copies them into the build so they exist on GitHub Pages too.
const staticCourseFolders = ['4370 - Web Programming']

function copyStaticCourses(): Plugin {
  return {
    name: 'copy-static-courses',
    apply: 'build',
    closeBundle() {
      for (const folder of staticCourseFolders) {
        cpSync(folder, `dist/${folder}`, { recursive: true })
      }
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  base: '/GSU-Portfolio/',
  plugins: [react(), copyStaticCourses()],
  server: { headers: crossOriginIsolationHeaders },
  preview: { headers: crossOriginIsolationHeaders },
  worker: { format: 'es' },
})
