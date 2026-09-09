import { Box, Button, Flex, Text, Textarea } from '@chakra-ui/react'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { getPythonRunner, supportsBlockingStdin } from '../lib/pythonRunner'

interface PythonTerminalProps {
  fileName: string
  sourceCode: string
  /** Pre-filled stdin, used only when the browser can't give us blocking input. */
  suggestedInput?: string
  accentColor?: string
}

type Phase = 'booting' | 'loading' | 'ready' | 'running' | 'awaiting-input' | 'error'

const FONT_FAMILY = "'SF Mono', 'Consolas', 'Courier New', monospace"

const colors = {
  bg: '#1e1e1e',
  text: '#cccccc',
  dim: '#8b949e',
  error: '#f48771',
  system: '#4ec9b0',
  buttonBg: '#3a3d41',
  buttonHover: '#4d5157',
  border: '#3c3c3c',
}

interface OutputChunk {
  id: number
  text: string
  stream: 'stdout' | 'stderr' | 'system'
}

/** Splits pre-supplied stdin into lines, ignoring the trailing newline. */
function toStdinQueue(raw: string): string[] {
  const lines = raw.split('\n')
  if (lines.length > 0 && lines[lines.length - 1] === '') lines.pop()
  return lines
}

export default function PythonTerminal({
  fileName,
  sourceCode,
  suggestedInput,
  accentColor = '#007acc',
}: PythonTerminalProps) {
  const [chunks, setChunks] = useState<OutputChunk[]>([])
  // Read the shared runner's current state, since a terminal mounted after
  // Pyodide finished loading never sees the 'ready' message.
  const [phase, setPhase] = useState<Phase>(() => {
    const runner = getPythonRunner()
    if (runner.isBusy) return 'running'
    return runner.isReady ? 'ready' : 'booting'
  })
  const [draft, setDraft] = useState('')
  const [fatal, setFatal] = useState('')
  const [queuedStdin, setQueuedStdin] = useState(suggestedInput ?? '')

  const scrollRef = useRef<HTMLDivElement | null>(null)
  const inputRef = useRef<HTMLInputElement | null>(null)
  const chunkId = useRef(0)

  const isBusy = phase === 'running' || phase === 'awaiting-input'

  const append = useCallback((text: string, stream: OutputChunk['stream']) => {
    chunkId.current += 1
    const id = chunkId.current
    setChunks((previous) => [...previous, { id, text, stream }])
  }, [])

  // The Pyodide worker is shared page-wide; this terminal just claims its
  // output while mounted, so switching files costs nothing.
  useEffect(() => {
    const runner = getPythonRunner()

    runner.setHandlers({
      onStatus: (status) => setPhase(status === 'loading' ? 'loading' : 'ready'),
      onOutput: (text, stream) => append(text, stream),
      onInputRequest: () => setPhase('awaiting-input'),
      onDone: (error) => {
        setPhase('ready')
        setDraft('')
        if (error) append(`\n${error}\n`, 'stderr')
      },
      onFatal: (message) => {
        setPhase('error')
        setFatal(message)
      },
    })

    return () => {
      // Don't leave a program running against a terminal that's going away.
      runner.interrupt()
      runner.clearHandlers()
    }
  }, [append])

  useEffect(() => {
    const node = scrollRef.current
    if (node) node.scrollTop = node.scrollHeight
  }, [chunks, draft, phase])

  useEffect(() => {
    if (phase === 'awaiting-input') inputRef.current?.focus()
  }, [phase])

  const handleRun = () => {
    const runner = getPythonRunner()
    if (isBusy) return

    setChunks([])
    setDraft('')
    setPhase('running')
    append(`$ python "${fileName}"\n`, 'system')

    runner.run(fileName, sourceCode, runner.interactive ? [] : toStdinQueue(queuedStdin))
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    const runner = getPythonRunner()

    if (event.ctrlKey && event.key.toLowerCase() === 'c') {
      event.preventDefault()
      append('^C', 'system')
      runner.interrupt()
      return
    }

    if (phase !== 'awaiting-input') return

    if (event.ctrlKey && event.key.toLowerCase() === 'd') {
      event.preventDefault()
      runner.submitEof()
      setPhase('running')
      return
    }

    if (event.key === 'Enter') {
      event.preventDefault()
      runner.submitLine(draft)
      setDraft('')
      setPhase('running')
    }
  }

  const statusLabel = useMemo(() => {
    switch (phase) {
      case 'booting':
      case 'loading':
        return 'Starting Python…'
      case 'running':
        return 'Running'
      case 'awaiting-input':
        return 'Waiting for input'
      case 'error':
        return 'Runtime error'
      default:
        return 'Ready'
    }
  }, [phase])

  const buttonProps = {
    size: 'xs' as const,
    color: colors.text,
    borderColor: colors.border,
    _hover: { bg: colors.buttonHover },
    fontFamily: FONT_FAMILY,
    fontWeight: 'normal' as const,
  }

  return (
    <Flex
      direction="column"
      h="100%"
      minH={0}
      gap={2}
      css={{
        '@keyframes terminalPulse': { '0%,100%': { opacity: 1 }, '50%': { opacity: 0.2 } },
        '@keyframes caretBlink': { '0%,49%': { opacity: 1 }, '50%,100%': { opacity: 0 } },
      }}
    >
      <Flex gap={2} align="center" wrap="wrap" flexShrink={0}>
        <Button
          {...buttonProps}
          onClick={handleRun}
          disabled={isBusy || phase === 'booting' || phase === 'loading' || phase === 'error'}
          bg={colors.buttonBg}
          border="1px solid"
        >
          {phase === 'booting' || phase === 'loading' ? 'Loading…' : '▶ Run'}
        </Button>

        <Button
          {...buttonProps}
          variant="outline"
          onClick={() => getPythonRunner().interrupt()}
          disabled={!isBusy}
        >
          {'■ Stop'}
        </Button>

        <Button {...buttonProps} variant="outline" onClick={() => setChunks([])} disabled={isBusy}>
          Clear
        </Button>

        <Flex align="center" gap={2} ml="auto" pr={1}>
          <Box
            w="7px"
            h="7px"
            borderRadius="full"
            bg={phase === 'awaiting-input' ? '#e2c08d' : isBusy ? accentColor : colors.dim}
            css={isBusy ? { animation: 'terminalPulse 1.2s ease-in-out infinite' } : undefined}
          />
          <Text fontSize="11px" color={colors.dim} fontFamily={FONT_FAMILY}>
            {statusLabel}
          </Text>
        </Flex>
      </Flex>

      {!supportsBlockingStdin && (
        <Box flexShrink={0}>
          <Text fontSize="11px" color={colors.dim} fontFamily={FONT_FAMILY} mb={1}>
            Live stdin is unavailable in this browser &mdash; supply the input lines up front:
          </Text>
          <Textarea
            value={queuedStdin}
            onChange={(event) => setQueuedStdin(event.target.value)}
            rows={2}
            bg="#252526"
            color={colors.text}
            borderColor={colors.border}
            fontFamily={FONT_FAMILY}
            fontSize="12px"
            resize="vertical"
          />
        </Box>
      )}

      <Box
        ref={scrollRef}
        flex="1"
        minH={0}
        bg={colors.bg}
        px={2}
        py={1}
        overflowY="auto"
        cursor="text"
        position="relative"
        onClick={() => inputRef.current?.focus()}
        css={{
          '&::-webkit-scrollbar': { width: '10px' },
          '&::-webkit-scrollbar-thumb': { background: '#424242', borderRadius: '5px' },
        }}
      >
        <Text
          as="pre"
          whiteSpace="pre-wrap"
          wordBreak="break-word"
          fontFamily={FONT_FAMILY}
          fontSize="13px"
          lineHeight="1.5"
          m={0}
        >
          {chunks.map((chunk) => (
            <Text
              as="span"
              key={chunk.id}
              color={
                chunk.stream === 'stderr'
                  ? colors.error
                  : chunk.stream === 'system'
                    ? colors.system
                    : colors.text
              }
            >
              {chunk.text}
            </Text>
          ))}

          {phase === 'awaiting-input' && (
            <Text as="span" color={colors.text}>
              {draft}
              <Box
                as="span"
                display="inline-block"
                w="7px"
                h="14px"
                bg={colors.text}
                verticalAlign="text-bottom"
                css={{ animation: 'caretBlink 1s step-end infinite' }}
              />
            </Text>
          )}
        </Text>

        {fatal && (
          <Text color={colors.error} fontFamily={FONT_FAMILY} fontSize="12px" mt={2}>
            {fatal}
          </Text>
        )}

        {/* Off-screen field that actually receives the keystrokes, so mobile
            keyboards and IME composition behave like a normal text input. */}
        <input
          ref={inputRef}
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={handleKeyDown}
          spellCheck={false}
          autoComplete="off"
          aria-label="Terminal input"
          style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            width: '1px',
            height: '1px',
            opacity: 0,
            padding: 0,
            border: 'none',
            outline: 'none',
          }}
        />
      </Box>
    </Flex>
  )
}
