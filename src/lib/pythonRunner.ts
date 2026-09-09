import {
  SIGINT,
  STDIN_BUFFER_BYTES,
  STDIN_HEADER_SLOTS,
  STDIN_PAYLOAD_BYTES,
  StdinState,
  type WorkerToMainMessage,
} from '../workers/pythonProtocol'

/**
 * Whether this document can give Python a real blocking input(). Requires
 * SharedArrayBuffer, which browsers only expose to cross-origin isolated pages
 * (see the COOP/COEP headers in vite.config.ts and public/coi-serviceworker.js).
 */
export const supportsBlockingStdin =
  typeof SharedArrayBuffer !== 'undefined' && self.crossOriginIsolated === true

export interface PythonRunnerHandlers {
  onOutput: (text: string, stream: 'stdout' | 'stderr') => void
  onInputRequest: () => void
  onDone: (error?: string) => void
  onStatus: (status: 'loading' | 'ready') => void
  onFatal: (message: string) => void
}

const noopHandlers: PythonRunnerHandlers = {
  onOutput: () => {},
  onInputRequest: () => {},
  onDone: () => {},
  onStatus: () => {},
  onFatal: () => {},
}

/**
 * Owns the Pyodide worker and the SharedArrayBuffers that let Python block on
 * input(). Where SharedArrayBuffer is unavailable it degrades to a stdin queue
 * supplied before the run -- output still streams, but the user can't type as
 * the program goes.
 */
export class PythonRunner {
  readonly interactive: boolean

  private worker: Worker
  private handlers: PythonRunnerHandlers = noopHandlers
  private stdinHeader: Int32Array | null = null
  private stdinPayload: Uint8Array | null = null
  private interruptSignal: Uint8Array | null = null
  private encoder = new TextEncoder()
  private runId = 0
  private awaitingInput = false
  private running = false
  private ready = false

  constructor() {
    this.interactive = supportsBlockingStdin

    let stdinBuffer: SharedArrayBuffer | null = null
    let interruptBuffer: SharedArrayBuffer | null = null

    if (this.interactive) {
      stdinBuffer = new SharedArrayBuffer(STDIN_BUFFER_BYTES)
      this.stdinHeader = new Int32Array(stdinBuffer, 0, STDIN_HEADER_SLOTS)
      this.stdinPayload = new Uint8Array(stdinBuffer, STDIN_HEADER_SLOTS * 4)

      interruptBuffer = new SharedArrayBuffer(1)
      this.interruptSignal = new Uint8Array(interruptBuffer)
    }

    this.worker = new Worker(new URL('../workers/pythonWorker.ts', import.meta.url), {
      type: 'module',
    })

    this.worker.addEventListener('message', this.handleMessage)
    this.worker.postMessage({ type: 'init', stdinBuffer, interruptBuffer })
  }

  get isBusy() {
    return this.running
  }

  /** True once Pyodide has finished loading. */
  get isReady() {
    return this.ready
  }

  get isAwaitingInput() {
    return this.awaitingInput
  }

  /** Points the worker's output at a new consumer. */
  setHandlers(handlers: PythonRunnerHandlers) {
    this.handlers = handlers
  }

  clearHandlers() {
    this.handlers = noopHandlers
  }

  private handleMessage = (event: MessageEvent<WorkerToMainMessage>) => {
    const message = event.data

    switch (message.type) {
      case 'status':
        this.ready = message.status === 'ready'
        this.handlers.onStatus(message.status)
        break
      case 'output':
        this.handlers.onOutput(message.text, message.stream)
        break
      case 'input-request':
        this.awaitingInput = true
        this.handlers.onInputRequest()
        break
      case 'done':
        this.running = false
        this.awaitingInput = false
        this.handlers.onDone(message.error)
        break
      case 'fatal':
        this.running = false
        this.awaitingInput = false
        this.handlers.onFatal(message.message)
        break
    }
  }

  run(fileName: string, code: string, queuedStdin: string[] = []) {
    this.runId += 1
    this.running = true
    this.awaitingInput = false

    // A fresh run must not inherit a stale SIGINT or a parked stdin state.
    if (this.interruptSignal) this.interruptSignal[0] = 0
    if (this.stdinHeader) Atomics.store(this.stdinHeader, 0, StdinState.waiting)

    this.worker.postMessage({ type: 'run', runId: this.runId, fileName, code, queuedStdin })
  }

  /** Hands a line to the blocked worker. The trailing newline is not included. */
  submitLine(line: string) {
    this.awaitingInput = false
    this.publish(StdinState.ready, line)
  }

  /** Ctrl+D -- Python sees EOFError. */
  submitEof() {
    this.awaitingInput = false
    this.publish(StdinState.eof, '')
  }

  /**
   * Ctrl+C. If Python is parked on input() we release the wait with the
   * interrupt state; otherwise we raise SIGINT through Pyodide's interrupt
   * buffer, which it checks between bytecodes.
   */
  interrupt() {
    if (!this.running) return

    if (this.awaitingInput) {
      this.awaitingInput = false
      this.publish(StdinState.interrupt, '')
      return
    }

    if (this.interruptSignal) this.interruptSignal[0] = SIGINT
  }

  private publish(state: number, line: string) {
    if (!this.stdinHeader || !this.stdinPayload) return

    const bytes = this.encoder.encode(line)
    const length = Math.min(bytes.length, STDIN_PAYLOAD_BYTES)
    this.stdinPayload.set(bytes.subarray(0, length))

    Atomics.store(this.stdinHeader, 1, length)
    // State is stored last so the worker never observes a half-written payload.
    Atomics.store(this.stdinHeader, 0, state)
    Atomics.notify(this.stdinHeader, 0)
  }
}

let singleton: PythonRunner | null = null

/**
 * Loading Pyodide costs several seconds and ~10MB, so the whole page shares one
 * worker. Terminals swap the handlers rather than spawning their own runtime.
 */
export function getPythonRunner(): PythonRunner {
  if (!singleton) singleton = new PythonRunner()
  return singleton
}
