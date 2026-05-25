import { Alert, Box, Button, Flex, Spinner, Stack, Text } from '@chakra-ui/react'
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
from js import prompt

_stdout = io.StringIO()
_stderr = io.StringIO()
_previous_stdout = sys.stdout
_previous_stderr = sys.stderr

def _portfolio_input(p=''):
    if p:
        print(p, end='')
    
    # Capture all output so far
    current_out = _stdout.getvalue()
    
    # Extract the last 15 lines of the terminal output to provide context
    # since the browser prompt will block the UI from updating the drawn terminal
    lines = current_out.strip().split('\\n')
    context = '\\n'.join(lines[-18:]) if lines else ''
    
    # Show the pyodide prompt dialog taking input from the user directly,
    # and include the recent terminal output so they can see their cards!
    prompt_msg = f"{context}\\n\\n{p}" if context else p
    val = prompt(prompt_msg)
    
    if val is None:
        raise EOFError('Input cancelled by user')
    
    print(val)
    return val

builtins.input = _portfolio_input

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

  // VS Code Terminal Theme Colors
  const colors = {
    bg: '#1e1e1e', // Dark terminal background
    text: '#cccccc', // Default terminal text gray
    border: '#3c3c3c', // Editor borders
    buttonBg: '#3a3d41', // Standard VS Code button style
    buttonHover: '#4d5157',
    buttonBorder: '#3c3c3c',
  }

  const fontFamily = "'Consolas', 'Courier New', monospace"

  return (
    <Stack gap={4} h="100%" display="flex" flexDirection="column">
      <Flex gap={3} wrap="wrap">
        <Button
          size="sm"
          onClick={handleRun}
          disabled={!canRun}
          bg={colors.buttonBg}
          color={colors.text}
          border="1px solid"
          borderColor={colors.buttonBorder}
          _hover={{ bg: colors.buttonHover }}
          fontFamily={fontFamily}
          fontWeight="normal"
        >
          {isPreparing ? 'Loading Pyodide...' : isRunning ? 'Running...' : 'Run Code'}
        </Button>

        <Button
          size="sm"
          onClick={() => setOutputValue('')}
          variant="outline"
          borderColor={colors.buttonBorder}
          color={colors.text}
          _hover={{ bg: colors.buttonHover }}
          fontFamily={fontFamily}
          fontWeight="normal"
        >
          Clear Output
        </Button>

        {(isPreparing || isRunning) && <Spinner color="#4d5157" size="sm" mt={1} />}
      </Flex>

      {errorValue && (
        <Alert.Root status="error" bg="#4d1212" borderColor="#c92a2a" color="#ffd8d8">
          <Alert.Indicator />
          <Alert.Content>
            <Alert.Title>Runner Error</Alert.Title>
            <Alert.Description>{errorValue}</Alert.Description>
          </Alert.Content>
        </Alert.Root>
      )}

      <Box
        flex={1}
        bg={colors.bg}
        border="1px solid"
        borderColor="transparent"
        p={2}
        minH="180px"
        overflowY="auto"
      >
        <Text
          whiteSpace="pre-wrap"
          color={colors.text}
          fontFamily={fontFamily}
          fontSize="14px"
        >
          {outputValue || ''}
        </Text>
      </Box>
    </Stack>
  )
}

