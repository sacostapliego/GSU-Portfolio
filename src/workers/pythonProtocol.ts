/**
 * Message contract shared by the main thread and the Pyodide worker.
 *
 * Layout of the stdin SharedArrayBuffer:
 *
 *   Int32Array header, 2 slots
 *     [0] state -- one of StdinState, written last so it publishes the payload
 *     [1] byteLength of the pending line
 *   Uint8Array payload, STDIN_PAYLOAD_BYTES
 *
 * The worker parks on Atomics.wait(header, 0, WAITING) and the main thread
 * fills the payload, stores the length, stores the state and notifies. That
 * gives Python a genuinely synchronous input() without a modal dialog.
 */

export const STDIN_HEADER_SLOTS = 2
export const STDIN_PAYLOAD_BYTES = 64 * 1024
export const STDIN_BUFFER_BYTES = STDIN_HEADER_SLOTS * 4 + STDIN_PAYLOAD_BYTES

export const StdinState = {
  /** Worker is parked, waiting for the user to submit a line. */
  waiting: 0,
  /** A line is available in the payload region. */
  ready: 1,
  /** End of input -- Python should see EOFError. */
  eof: 2,
  /** User pressed Ctrl+C -- Python should see KeyboardInterrupt. */
  interrupt: 3,
} as const

/** Pyodide's interrupt buffer signal value for SIGINT. */
export const SIGINT = 2

export type MainToWorkerMessage =
  | { type: 'init'; stdinBuffer: SharedArrayBuffer | null; interruptBuffer: SharedArrayBuffer | null }
  | { type: 'run'; runId: number; fileName: string; code: string; queuedStdin: string[] }

export type WorkerToMainMessage =
  | { type: 'status'; status: 'loading' | 'ready'; message?: string }
  | { type: 'output'; runId: number; stream: 'stdout' | 'stderr'; text: string }
  /** Python has blocked on input(); the prompt has already been written to stdout. */
  | { type: 'input-request'; runId: number }
  | { type: 'done'; runId: number; error?: string }
  | { type: 'fatal'; message: string }
