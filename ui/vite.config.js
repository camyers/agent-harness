import fs from 'node:fs'
import { fileURLToPath } from 'node:url'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

const LOG_FILE = fileURLToPath(new URL('../runs.jsonl', import.meta.url))

function serveRuns() {
  return {
    name: 'serve-runs',
    configureServer(server) {
      server.middlewares.use('/runs.jsonl', (req, res) => {
        res.setHeader('Content-Type', 'text/plain; charset=utf-8')
        res.end(fs.existsSync(LOG_FILE) ? fs.readFileSync(LOG_FILE, 'utf-8') : '')
      })
    },
  }
}

export default defineConfig({
  plugins: [react(), serveRuns()],
})