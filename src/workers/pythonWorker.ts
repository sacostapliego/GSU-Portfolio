/// <reference lib="webworker" />

import bootstrapScript from './pythonBootstrap.py?raw'
import {
  STDIN_HEADER_SLOTS,
  StdinState,
  type MainToWorkerMessage,
  type WorkerToMainMessage,
} from './pythonProtocol'

const PYODIDE_VERSION = '0.27.7'
const PYODIDE_INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`
const PYODIDE_MODULE_URL = `${PYODIDE_INDEX_URL}pyodide.mjs`

interface PyodideRuntime {
  globals: { set: (name: string, value: unknown) => void }
  runPython: (code: string) => unknown
  setStdout: (options: { write: (buffer: Uint8Array) => number; isatty?: boolean }) => void
  setStderr: (options: { write: (buffer: Uint8Array) => number; isatty?: boolean }) => void
  setInterruptBuffer: (buffer: Uint8Array) => void
}

const post = (message: WorkerToMainMessage) => self.postMessage(message)

const decoder = new TextDecoder()

/**
 * TextDecoder rejects views backed by a SharedArrayBuffer ("must not be
 * shared"), which is exactly what the stdin payload is, so copy those into a
 * regular buffer before decoding.
 */
function decodeBytes(view: Uint8Array): string {
  const isShared =
    typeof SharedArrayBuffer !== 'undefined' && view.buffer instanceof SharedArrayBuffer
  return decoder.decode(isShared ? new Uint8Array(view) : view)
}

/** Returned from the stdin reader when the user pressed Ctrl+C while waiting. */
const INTERRUPT_SENTINEL = String.fromCharCode(0) + '__PORTFOLIO_INTERRUPT__'

let runtimePromise: Promise<PyodideRuntime> | null = null
let stdinHeader: Int32Array | null = null
let stdinPayload: Uint8Array | null = null
let interruptSignal: Uint8Array | null = null

/** Falls back to a pre-supplied stdin queue when SharedArrayBuffer is unavailable. */
let queuedStdin: string[] = []
let activeRunId = -1

/**
 * Blocks the worker until the main thread publishes a line. This is the whole
 * point of the worker: Atomics.wait is forbidden on the main thread, but here
 * it lets Python's input() behave exactly like it does in a real terminal.
 */
function readLineBlocking(): string | null {
  if (!stdinHeader || !stdinPayload) {
    // No SharedArrayBuffer -- drain the queue the caller supplied up front.
    return queuedStdin.length > 0 ? (queuedStdin.shift() as string) : null
  }

  Atomics.store(stdinHeader, 0, StdinState.waiting)
  post({ type: 'input-request', runId: activeRunId })
  Atomics.wait(stdinHeader, 0, StdinState.waiting)

  const state = Atomics.load(stdinHeader, 0)
  if (state === StdinState.eof) return null
  if (state === StdinState.interrupt) return INTERRUPT_SENTINEL

  const byteLength = Atomics.load(stdinHeader, 1)
  return decodeBytes(stdinPayload.subarray(0, byteLength))
}

async function loadRuntime(): Promise<PyodideRuntime> {
  if (runtimePromise) return runtimePromise

  runtimePromise = (async () => {
    post({ type: 'status', status: 'loading' })

    // Kept in a variable so Vite treats it as an external runtime URL rather
    // than something to resolve at build time.
    const moduleUrl = PYODIDE_MODULE_URL
    const { loadPyodide } = (await import(/* @vite-ignore */ moduleUrl)) as {
      loadPyodide: (options: { indexURL: string }) => Promise<PyodideRuntime>
    }

    const runtime = await loadPyodide({ indexURL: PYODIDE_INDEX_URL })

    // Stream every write straight to the terminal instead of buffering the
    // whole run and flushing at the end.
    const forward = (stream: 'stdout' | 'stderr') => ({
      write: (buffer: Uint8Array) => {
        // Decoded synchronously: the view points into WASM memory that Pyodide
        // reuses as soon as this returns.
        post({ type: 'output', runId: activeRunId, stream, text: decodeBytes(buffer) })
        return buffer.length
      },
      isatty: true,
    })

    runtime.setStdout(forward('stdout'))
    runtime.setStderr(forward('stderr'))

    if (interruptSignal) runtime.setInterruptBuffer(interruptSignal)

    runtime.globals.set('_portfolio_read_line', readLineBlocking)
    runtime.runPython(bootstrapScript)

    post({ type: 'status', status: 'ready' })
    return runtime
  })()

  return runtimePromise
}

self.addEventListener('message', async (event: MessageEvent<MainToWorkerMessage>) => {
  const message = event.data

  if (message.type === 'init') {
    if (message.stdinBuffer) {
      stdinHeader = new Int32Array(message.stdinBuffer, 0, STDIN_HEADER_SLOTS)
      stdinPayload = new Uint8Array(message.stdinBuffer, STDIN_HEADER_SLOTS * 4)
    }
    if (message.interruptBuffer) {
      interruptSignal = new Uint8Array(message.interruptBuffer)
    }

    try {
      await loadRuntime()
    } catch (error) {
      post({ type: 'fatal', message: error instanceof Error ? error.message : String(error) })
    }
    return
  }

  if (message.type === 'run') {
    activeRunId = message.runId
    queuedStdin = [...message.queuedStdin]

    try {
      const runtime = await loadRuntime()

      // Clear any SIGINT left over from a previous run's Ctrl+C.
      if (interruptSignal) interruptSignal[0] = 0

      runtime.globals.set('_portfolio_code', message.code)
      runtime.globals.set('_portfolio_file_name', message.fileName)
      runtime.runPython('_portfolio_run(_portfolio_code, _portfolio_file_name)')

      post({ type: 'done', runId: message.runId })
    } catch (error) {
      const raw = error instanceof Error ? error.message : String(error)

      if (raw.includes('KeyboardInterrupt')) {
        post({ type: 'output', runId: message.runId, stream: 'stderr', text: '\nKeyboardInterrupt\n' })
        post({ type: 'done', runId: message.runId })
        return
      }

      post({ type: 'done', runId: message.runId, error: raw })
    } finally {
      activeRunId = -1
    }
  }
})
