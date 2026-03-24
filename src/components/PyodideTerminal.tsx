import { Alert, Box, Button, Flex, Spinner, Stack, Text, Textarea } from '@chakra-ui/react'
import { useMemo, useState } from 'react'

interface PyodideTerminalProps {
  programTitle: string
  sourceCode: string
  suggestedInput?: string
}

type PyodideWindow = Window & {
  loadPyodide?: (options: { indexURL: string }) => Promise<PyodideRuntime>
  __portfolioPyodidePromise?: Promise<PyodideRuntime>
}

interface PyodideRuntime {
  globals: {
    set: (name: string, value: unknown) => void
  }
  runPythonAsync: (code: string) => Promise<unknown>
}

const PYODIDE_SCRIPT_URL = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js'
const PYODIDE_INDEX_URL = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'

function terminalStamp(): string {
  return new Date().toLocaleTimeString([], { hour12: false })
}

async function ensurePyodide(): Promise<PyodideRuntime> {
  const pyodideWindow = window as PyodideWindow

  if (pyodideWindow.__portfolioPyodidePromise) {
    return pyodideWindow.__portfolioPyodidePromise
  }

  pyodideWindow.__portfolioPyodidePromise = new Promise<PyodideRuntime>((resolve, reject) => {
    const initialize = async () => {
      try {
        if (!pyodideWindow.loadPyodide) {
          reject(new Error('Pyodide runtime is unavailable after script load.'))
          return
        }

        const runtime = await pyodideWindow.loadPyodide({ indexURL: PYODIDE_INDEX_URL })
        resolve(runtime)
      } catch (error) {
        reject(error instanceof Error ? error : new Error('Failed to initialize Pyodide.'))
      }
    }

    if (pyodideWindow.loadPyodide) {
      void initialize()
      return
    }

    const existingScript = document.querySelector(`script[src="${PYODIDE_SCRIPT_URL}"]`) as HTMLScriptElement | null

    if (existingScript) {
      existingScript.addEventListener('load', () => {
        void initialize()
      })
      existingScript.addEventListener('error', () => {
        reject(new Error('Unable to load the Pyodide script from CDN.'))
      })
      return
    }

    const script = document.createElement('script')
    script.src = PYODIDE_SCRIPT_URL
    script.async = true
    script.onload = () => {
      void initialize()
    }
    script.onerror = () => {
      reject(new Error('Unable to load the Pyodide script from CDN.'))
    }
    document.head.appendChild(script)
  })

  return pyodideWindow.__portfolioPyodidePromise
}

const RUNNER_SCRIPT = `
import io
import sys
import traceback
import builtins

_raw_input = USER_INPUT.replace('\\r\\n', '\\n').replace('\\r', '\\n')
_input_lines = _raw_input.split('\\n') if _raw_input != '' else []
_input_index = 0


def _portfolio_input(prompt=''):
    global _input_index
    if prompt:
        print(prompt, end='')
    if _input_index < len(_input_lines):
        value = _input_lines[_input_index]
        _input_index += 1
        print(value)
        return value
    raise EOFError('Input exhausted in browser runner.')


builtins.input = _portfolio_input
_stdout = io.StringIO()
_stderr = io.StringIO()
_previous_stdout = sys.stdout
_previous_stderr = sys.stderr

try:
    sys.stdout = _stdout
    sys.stderr = _stderr
    exec(compile(USER_CODE, '<portfolio>', 'exec'), {})
except Exception:
    traceback.print_exc()
finally:
    sys.stdout = _previous_stdout
    sys.stderr = _previous_stderr

RUN_OUTPUT = _stdout.getvalue() + _stderr.getvalue()
`

export default function PyodideTerminal({ programTitle, sourceCode, suggestedInput }: PyodideTerminalProps) {
  const [stdinValue, setStdinValue] = useState(suggestedInput ?? '')
  const [outputValue, setOutputValue] = useState<string>('')
  const [errorValue, setErrorValue] = useState<string>('')
  const [isPreparing, setIsPreparing] = useState(false)
  const [isRunning, setIsRunning] = useState(false)

  const canRun = useMemo(() => !isPreparing && !isRunning, [isPreparing, isRunning])

  const handleRun = async () => {
    setErrorValue('')
    setOutputValue((previous) => {
      const divider = previous ? '\n' : ''
      return `${previous}${divider}[${terminalStamp()}] Starting ${programTitle}...\n`
    })

    try {
      setIsPreparing(true)
      const pyodide = await ensurePyodide()
      setIsPreparing(false)

      setIsRunning(true)
      pyodide.globals.set('USER_CODE', sourceCode)
      pyodide.globals.set('USER_INPUT', stdinValue)

      await pyodide.runPythonAsync(RUNNER_SCRIPT)
      const result = (await pyodide.runPythonAsync('RUN_OUTPUT')) as string

      setOutputValue((previous) => {
        const trimmed = result.trimEnd()
        const separator = previous.endsWith('\n') ? '' : '\n'
        return `${previous}${separator}${trimmed || '[no output]'}\n`
      })
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unexpected execution failure.'
      setErrorValue(message)
    } finally {
      setIsPreparing(false)
      setIsRunning(false)
    }
  }

  return (
    <Stack gap={4}>
      <Text color="#9ef7c4" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace" fontSize="0.95rem">
        Input lines (one per prompt):
      </Text>

      <Textarea
        value={stdinValue}
        onChange={(event) => setStdinValue(event.target.value)}
        placeholder="Type input lines here..."
        minH="110px"
        bg="#000000"
        color="#31ff77"
        borderColor="#11632f"
        _focusVisible={{ borderColor: '#31ff77', boxShadow: '0 0 0 1px #31ff77 inset' }}
        fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
      />

      <Flex gap={3} wrap="wrap">
        <Button
          onClick={handleRun}
          disabled={!canRun}
          bg="#022d13"
          color="#72ffad"
          border="1px solid"
          borderColor="#1e9e53"
          _hover={{ bg: '#03411b' }}
          fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
        >
          {isPreparing ? 'Loading Pyodide...' : isRunning ? 'Running...' : 'Run in Browser'}
        </Button>

        <Button
          onClick={() => setOutputValue('')}
          variant="outline"
          borderColor="#1e9e53"
          color="#72ffad"
          _hover={{ bg: '#022d13' }}
          fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
        >
          Clear Output
        </Button>

        {(isPreparing || isRunning) && <Spinner color="#72ffad" size="sm" mt={2} />}
      </Flex>

      {errorValue && (
        <Alert.Root status="error" bg="#2b0000" borderColor="#7a1c1c" color="#ffd8d8">
          <Alert.Indicator />
          <Alert.Content>
            <Alert.Title>Runner Error</Alert.Title>
            <Alert.Description>{errorValue}</Alert.Description>
          </Alert.Content>
        </Alert.Root>
      )}

      <Box
        bg="#000000"
        border="1px solid"
        borderColor="#1e9e53"
        borderRadius="md"
        p={4}
        minH="180px"
        maxH="340px"
        overflowY="auto"
        boxShadow="inset 0 0 24px rgba(18, 160, 73, 0.25)"
      >
        <Text
          whiteSpace="pre-wrap"
          color="#31ff77"
          fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
          fontSize="0.9rem"
        >
          {outputValue || '[terminal idle] Press Run in Browser to execute this script.'}
        </Text>
      </Box>
    </Stack>
  )
}
