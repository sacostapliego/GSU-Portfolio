import { Box, Flex, Image, Text, VStack } from '@chakra-ui/react'
import { motion } from 'framer-motion'
import { useCallback, useRef, useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import PythonTerminal from '../components/PythonTerminal'
import { csc1301Programs } from '../data/csc1301Programs'
import { useDragResize } from '../hooks/useDragResize'
import { createInitialRect, useWindowFrame } from '../hooks/useWindowFrame'
import type { ResizeEdge, WindowRect } from '../hooks/useWindowFrame'

interface CSC1301Props {
  onBack: () => void
}

type WindowMode = 'normal' | 'maximized' | 'minimized' | 'closed'

const MotionFlex = motion.create(Flex)

// VS Code Dark Theme Colors
const colors = {
  bg: '#1e1e1e',
  sidebar: '#252526',
  border: '#3c3c3c',
  text: '#cccccc',
  activeText: '#ffffff',
  activeBg: '#37373d',
  accent: '#007acc',
}

/** Height reserved at the bottom of the screen for the dock. */
const DOCK_INSET = 104

// Explicit px strings: bare numbers would be read as Chakra spacing tokens.
const GRIP = '-7px'
const EDGE_THICKNESS = '14px'
const CORNER_INSET = '16px'
const CORNER_SIZE = '23px'

/** Position of each resize grip relative to the window box. */
const RESIZE_EDGES: Array<{ edge: ResizeEdge } & Record<string, string>> = [
  { edge: 'n', top: GRIP, left: CORNER_INSET, right: CORNER_INSET, height: EDGE_THICKNESS },
  { edge: 's', bottom: GRIP, left: CORNER_INSET, right: CORNER_INSET, height: EDGE_THICKNESS },
  { edge: 'w', left: GRIP, top: CORNER_INSET, bottom: CORNER_INSET, width: EDGE_THICKNESS },
  { edge: 'e', right: GRIP, top: CORNER_INSET, bottom: CORNER_INSET, width: EDGE_THICKNESS },
  { edge: 'nw', top: GRIP, left: GRIP, width: CORNER_SIZE, height: CORNER_SIZE },
  { edge: 'ne', top: GRIP, right: GRIP, width: CORNER_SIZE, height: CORNER_SIZE },
  { edge: 'sw', bottom: GRIP, left: GRIP, width: CORNER_SIZE, height: CORNER_SIZE },
  { edge: 'se', bottom: GRIP, right: GRIP, width: CORNER_SIZE, height: CORNER_SIZE },
]

type TrafficLightId = 'close' | 'minimize' | 'maximize'

const TRAFFIC_LIGHTS: Array<{ id: TrafficLightId; bg: string; ring: string; glyph: string }> = [
  { id: 'close', bg: '#ff5f56', ring: '#e0443e', glyph: '✕' },
  { id: 'minimize', bg: '#ffbd2e', ring: '#dea123', glyph: '–' },
  { id: 'maximize', bg: '#27c93f', ring: '#1aab29', glyph: '⤢' },
]

const SIDEBAR_DEFAULT = 260
const SIDEBAR_MIN = 150
const TERMINAL_DEFAULT = 260
const TERMINAL_MIN = 90

export default function CSC1301({ onBack }: CSC1301Props) {
  const [selectedProgramIndex, setSelectedProgramIndex] = useState(0)
  const [hoveredDockItem, setHoveredDockItem] = useState<string | null>(null)
  const [windowMode, setWindowMode] = useState<WindowMode>('normal')
  const [isChromeHovered, setIsChromeHovered] = useState(false)

  const [sidebarWidth, setSidebarWidth] = useState(SIDEBAR_DEFAULT)
  const [terminalHeight, setTerminalHeight] = useState(TERMINAL_DEFAULT)

  const [windowRect, setWindowRect] = useState<WindowRect>(() => createInitialRect(DOCK_INSET))
  // Where the window returns to when un-maximized.
  const restoreRect = useRef<WindowRect | null>(null)

  const contentRef = useRef<HTMLDivElement | null>(null)
  const editorColumnRef = useRef<HTMLDivElement | null>(null)

  const selectedProgram = csc1301Programs[selectedProgramIndex]
  const isWindowVisible = windowMode === 'normal' || windowMode === 'maximized'

  // Leave room for the editor pane so neither side can be dragged to nothing.
  const sidebarMax = useCallback(
    () => Math.max(SIDEBAR_MIN, (contentRef.current?.clientWidth ?? 900) - 360),
    [],
  )
  const terminalMax = useCallback(
    () => Math.max(TERMINAL_MIN, (editorColumnRef.current?.clientHeight ?? 600) - 140),
    [],
  )

  const sidebarResize = useDragResize({
    axis: 'x',
    value: sidebarWidth,
    onChange: setSidebarWidth,
    min: SIDEBAR_MIN,
    max: sidebarMax,
    defaultValue: SIDEBAR_DEFAULT,
  })

  const terminalResize = useDragResize({
    axis: 'y',
    value: terminalHeight,
    onChange: setTerminalHeight,
    min: TERMINAL_MIN,
    max: terminalMax,
    invert: true, // dragging the splitter up grows the terminal
    defaultValue: TERMINAL_DEFAULT,
  })

  const frameControls = useWindowFrame({
    rect: windowRect,
    onChange: setWindowRect,
    bottomInset: DOCK_INSET,
    disabled: windowMode !== 'normal',
  })

  const isInteractingWithFrame = frameControls.isMoving || frameControls.isResizing

  const toggleMaximize = useCallback(() => {
    if (windowMode === 'maximized') {
      if (restoreRect.current) setWindowRect(restoreRect.current)
      setWindowMode('normal')
      return
    }

    restoreRect.current = windowRect
    setWindowRect({
      x: 16,
      y: 16,
      width: window.innerWidth - 32,
      height: window.innerHeight - DOCK_INSET - 16,
    })
    setWindowMode('maximized')
  }, [windowMode, windowRect])

  // While hidden the window keeps its geometry, so it reopens where you left it.
  const frame = windowRect

  const handleTrafficLight = (id: TrafficLightId) => {
    if (id === 'close') setWindowMode('closed')
    else if (id === 'minimize') setWindowMode('minimized')
    else toggleMaximize()
  }

  return (
    <Box
      h="100vh"
      w="100vw"
      bgImage={`linear-gradient(rgba(15, 15, 17, 0.35), rgba(15, 15, 17, 0.65)), url('/gsu_background.jpg')`}
      bgSize="cover"
      bgPos="center"
      bgRepeat="no-repeat"
      bgAttachment="fixed"
      color={colors.text}
      overflow="hidden"
      position="relative"
      fontFamily="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    >
      {/* Outer box owns the geometry (position + size) so dragging and
          resizing never fight framer-motion's open/minimize transforms,
          which live on the inner element. */}
      <Box
        position="absolute"
        left={`${frame.x}px`}
        top={`${frame.y}px`}
        w={`${frame.width}px`}
        h={`${frame.height}px`}
        pointerEvents={isWindowVisible ? 'auto' : 'none'}
        // Snapping to maximize should glide; a drag must track the pointer exactly.
        transition={isInteractingWithFrame ? 'none' : 'left 0.2s ease, top 0.2s ease, width 0.2s ease, height 0.2s ease'}
      >
        {/* The window stays mounted while hidden so minimizing never restarts
            Pyodide or kills a program that is mid-run. */}
        <MotionFlex
          key="vscode-window"
          initial={{ opacity: 0, scale: 0.94, y: 24 }}
          animate={windowMode}
          variants={{
            normal: { opacity: 1, scale: 1, y: 0 },
            maximized: { opacity: 1, scale: 1, y: 0 },
            // Minimize genies down toward the dock; close just fades in place.
            minimized: { opacity: 0, scale: 0.28, y: 340, transition: { duration: 0.3 } },
            closed: { opacity: 0, scale: 0.94, y: 0, transition: { duration: 0.18 } },
          }}
          transition={{ type: 'spring', stiffness: 220, damping: 26 }}
          w="100%"
          h="100%"
          bg={colors.bg}
          borderRadius={windowMode === 'maximized' ? 'lg' : '2xl'}
          boxShadow="0 25px 50px -12px rgba(0, 0, 0, 0.75)"
          direction="column"
          overflow="hidden"
          border="1px solid"
          borderColor={colors.border}
        >
          {/* Title Bar (macOS style) */}
          <Flex
            {...frameControls.moveHandleProps}
            h="36px"
            bg={colors.sidebar}
            align="center"
            justify="space-between"
            px={4}
            flexShrink={0}
            onDoubleClick={toggleMaximize}
          >
            <Flex
              gap="8px"
              flex={1}
              onMouseEnter={() => setIsChromeHovered(true)}
              onMouseLeave={() => setIsChromeHovered(false)}
            >
              {TRAFFIC_LIGHTS.map((light) => (
                <Box
                  key={light.id}
                  as="button"
                  aria-label={light.id}
                  onClick={() => handleTrafficLight(light.id)}
                  w="12px"
                  h="12px"
                  p={0}
                  borderRadius="full"
                  bg={light.bg}
                  border="1px solid"
                  borderColor={light.ring}
                  cursor="pointer"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  lineHeight="1"
                  fontSize="8px"
                  fontWeight="bold"
                  color="rgba(0, 0, 0, 0.55)"
                  transition="opacity 0.12s ease"
                  _active={{ opacity: 0.6 }}
                >
                  <Box as="span" opacity={isChromeHovered ? 1 : 0} transition="opacity 0.12s ease">
                    {light.glyph}
                  </Box>
                </Box>
              ))}
            </Flex>

            <Text flex={2} textAlign="center" fontSize="xs" color="#8b949e" userSelect="none">
              {selectedProgram.fileName} — CSC 1301
            </Text>

            <Flex flex={1} justify="flex-end" />
          </Flex>

          {/* Content Area */}
          <Flex ref={contentRef} flex={1} overflow="hidden" minH={0}>
            {/* Sidebar */}
            <Box
              w={`${sidebarWidth}px`}
              flexShrink={0}
              bg={colors.sidebar}
              display="flex"
              flexDirection="column"
              overflow="hidden"
            >
              <Text
                px={5}
                py={4}
                fontSize="sm"
                fontWeight="semibold"
                textTransform="uppercase"
                color="#8b949e"
                whiteSpace="nowrap"
              >
                Explorer
              </Text>
              <VStack align="stretch" gap={0} overflowY="auto" flex={1}>
                {csc1301Programs.map((program, index) => {
                  const isActive = index === selectedProgramIndex
                  return (
                    <Box
                      key={program.id}
                      px={5}
                      py={2}
                      cursor="pointer"
                      bg={isActive ? colors.activeBg : 'transparent'}
                      color={isActive ? colors.activeText : colors.text}
                      _hover={{ bg: isActive ? colors.activeBg : '#2a2d2e' }}
                      onClick={() => setSelectedProgramIndex(index)}
                      fontSize="15px"
                      display="flex"
                      alignItems="center"
                      gap={3}
                    >
                      <Image src="/python-logo.svg" alt="" boxSize="15px" flexShrink={0} />
                      <Text truncate>{program.fileName}</Text>
                    </Box>
                  )
                })}
              </VStack>
            </Box>

            {/* Sidebar / editor splitter */}
            <Box
              {...sidebarResize.handleProps}
              w="5px"
              flexShrink={0}
              bg={sidebarResize.isDragging ? colors.accent : colors.border}
              opacity={sidebarResize.isDragging ? 1 : 0.5}
              _hover={{ bg: colors.accent, opacity: 1 }}
              transition="background 0.12s ease, opacity 0.12s ease"
              role="separator"
              aria-orientation="vertical"
            />

            {/* Editor + Terminal Column */}
            <Flex ref={editorColumnRef} flex={1} direction="column" minW={0} minH={0}>
              {/* Code Editor */}
              <Box flex={1} bg={colors.bg} display="flex" flexDirection="column" overflow="hidden" minH={0}>
                <Flex h="45px" bg={colors.sidebar} borderBottom="1px solid" borderColor={colors.border} align="end" flexShrink={0}>
                  <Box
                    h="100%"
                    px={5}
                    bg={colors.bg}
                    color={colors.activeText}
                    borderTop="2px solid"
                    borderTopColor={colors.accent}
                    display="flex"
                    alignItems="center"
                    gap={2}
                  >
                    <Image src="/python-logo.svg" alt="" boxSize="16px" flexShrink={0} />
                    <Text fontSize="15px" whiteSpace="nowrap">
                      {selectedProgram.fileName}
                    </Text>
                  </Box>
                </Flex>

                <Box flex={1} overflow="auto" bg={colors.bg} mt={2} minH={0}>
                  <SyntaxHighlighter
                    language="python"
                    style={vscDarkPlus}
                    customStyle={{
                      margin: 0,
                      background: colors.bg,
                      fontSize: '16px',
                      minHeight: '100%',
                      padding: '0 10px',
                    }}
                    showLineNumbers
                  >
                    {selectedProgram.sourceCode}
                  </SyntaxHighlighter>
                </Box>
              </Box>

              {/* Editor / terminal splitter */}
              <Box
                {...terminalResize.handleProps}
                h="5px"
                flexShrink={0}
                bg={terminalResize.isDragging ? colors.accent : colors.border}
                opacity={terminalResize.isDragging ? 1 : 0.5}
                _hover={{ bg: colors.accent, opacity: 1 }}
                transition="background 0.12s ease, opacity 0.12s ease"
                role="separator"
                aria-orientation="horizontal"
              />

              {/* Terminal */}
              <Box
                h={`${terminalHeight}px`}
                flexShrink={0}
                bg={colors.bg}
                display="flex"
                flexDirection="column"
                overflow="hidden"
              >
                <Flex h="34px" align="center" px={5} flexShrink={0}>
                  <Text
                    fontSize="12px"
                    fontWeight="semibold"
                    color={colors.text}
                    textTransform="uppercase"
                    letterSpacing="0.08em"
                  >
                    Terminal
                  </Text>
                </Flex>
                <Box flex={1} px={3} pb={3} overflow="hidden" minH={0}>
                  <PythonTerminal
                    key={selectedProgram.id}
                    fileName={selectedProgram.fileName}
                    sourceCode={selectedProgram.sourceCode}
                    suggestedInput={selectedProgram.suggestedInput}
                    accentColor={colors.accent}
                  />
                </Box>
              </Box>
            </Flex>
          </Flex>
        </MotionFlex>

        {/* Eight-way resize grips, outside the clipped window so they stay
            grabbable at the rounded corners. Hidden while maximized. */}
        {windowMode === 'normal' &&
          RESIZE_EDGES.map(({ edge, ...position }) => (
            <Box
              key={edge}
              {...frameControls.getResizeHandleProps(edge)}
              position="absolute"
              zIndex={5}
              {...position}
            />
          ))}
      </Box>

      {/* macOS Dock */}
      <Flex
        position="absolute"
        bottom="16px"
        left="50%"
        transform="translateX(-50%)"
        display="inline-flex"
        w="fit-content"
        bg="rgba(255, 255, 255, 0.06)"
        borderRadius="24px"
        px={3.5}
        py={2.5}
        gap={3}
        boxShadow="0 8px 32px rgba(0, 0, 0, 0.18)"
        alignItems="flex-end"
        justifyContent="center"
        overflow="visible"
        zIndex={10}
        style={{
          backdropFilter: 'blur(28px) saturate(160%)',
          WebkitBackdropFilter: 'blur(28px) saturate(160%)',
        }}
      >
        <DockItem
          id="home"
          label="Home"
          isHovered={hoveredDockItem === 'home'}
          onHoverChange={setHoveredDockItem}
          onClick={onBack}
        >
          <Image src="/image.png" alt="Home" w="100%" h="100%" objectFit="cover" display="block" />
        </DockItem>

        <DockItem
          id="editor"
          label={isWindowVisible ? 'Visual Studio Code' : 'Reopen Editor'}
          isHovered={hoveredDockItem === 'editor'}
          onHoverChange={setHoveredDockItem}
          onClick={() => setWindowMode(isWindowVisible ? 'minimized' : 'normal')}
          isRunning={isWindowVisible}
        >
          <Flex w="100%" h="100%" align="center" justify="center" bg="#0f1b2d" borderRadius="14px">
            <Image src="/python-logo.svg" alt="" w="60%" h="60%" objectFit="contain" />
          </Flex>
        </DockItem>
      </Flex>
    </Box>
  )
}

interface DockItemProps {
  id: string
  label: string
  isHovered: boolean
  onHoverChange: (id: string | null) => void
  onClick: () => void
  isRunning?: boolean
  children: React.ReactNode
}

function DockItem({ id, label, isHovered, onHoverChange, onClick, isRunning, children }: DockItemProps) {
  return (
    <Box
      position="relative"
      flexShrink={0}
      onMouseEnter={() => onHoverChange(id)}
      onMouseLeave={() => onHoverChange(null)}
    >
      <Text
        position="absolute"
        bottom="calc(100% + 12px)"
        left="50%"
        transform="translateX(-50%)"
        px={3}
        py={1}
        borderRadius="full"
        bg="rgba(30, 30, 30, 0.85)"
        color="white"
        fontSize="sm"
        fontWeight="bold"
        whiteSpace="nowrap"
        opacity={isHovered ? 1 : 0}
        pointerEvents="none"
        transition="opacity 0.15s ease"
        zIndex={20}
      >
        {label}
      </Text>

      <Box
        as="button"
        onClick={onClick}
        aria-label={label}
        w="64px"
        h="64px"
        borderRadius="14px"
        overflow="hidden"
        cursor="pointer"
        border="none"
        p={0}
        m={0}
        display="flex"
        alignItems="center"
        justifyContent="center"
        bg="transparent"
        transition="transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1)"
        transform={isHovered ? 'scale(1.14) translateY(-6px)' : 'scale(1)'}
      >
        {children}
      </Box>

      {/* Running indicator dot, like macOS. */}
      <Box
        position="absolute"
        bottom="-6px"
        left="50%"
        transform="translateX(-50%)"
        w="4px"
        h="4px"
        borderRadius="full"
        bg="rgba(255, 255, 255, 0.75)"
        opacity={isRunning ? 1 : 0}
        transition="opacity 0.2s ease"
      />
    </Box>
  )
}
