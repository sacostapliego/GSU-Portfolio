import { Box, Container, Flex, Heading, Image, SimpleGrid, Text } from '@chakra-ui/react'
import { motion } from 'framer-motion'
import { useEffect, useMemo, useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { findNode, getCourseTree } from '../data/courseFiles'
import type { FileNode, FolderNode, TreeNode } from '../data/courseFiles'
import type { Course } from '../types'

interface CourseExplorerProps {
  course: Course
  /** Course-relative path of the open folder or file ("" is the course root). */
  path: string
  onNavigate: (path: string) => void
  onBack: () => void
}

const MotionBox = motion.create(Box)

/** Text beyond this many characters is cut off so huge datasets don't freeze the page. */
const PREVIEW_LIMIT = 100_000

const IMAGE_EXTS = new Set(['png', 'jpg', 'jpeg', 'gif', 'ico', 'svg'])

const PRISM_LANGUAGES: Record<string, string> = {
  py: 'python',
  java: 'java',
  c: 'c',
  h: 'c',
  asm: 'nasm',
  sql: 'sql',
  js: 'jsx',
  jsx: 'jsx',
  ts: 'typescript',
  tsx: 'tsx',
  css: 'css',
  html: 'markup',
  php: 'php',
  md: 'markdown',
  json: 'json',
  yml: 'yaml',
  yaml: 'yaml',
  sh: 'bash',
  r: 'r',
}

/** Badge colors for file tiles, loosely following GitHub's language colors. */
const EXT_COLORS: Record<string, string> = {
  py: '#3572A5',
  ipynb: '#DA5B0B',
  java: '#b07219',
  c: '#555555',
  asm: '#6E4C13',
  sql: '#e38c00',
  js: '#d4b90b',
  css: '#563d7c',
  html: '#e34c26',
  php: '#4F5D95',
  md: '#083fa1',
  csv: '#237346',
  pdf: '#b30b00',
}

function languageFor(file: FileNode) {
  if (file.name === 'Dockerfile') return 'docker'
  return PRISM_LANGUAGES[file.ext] ?? 'text'
}

const parentPath = (path: string) => path.split('/').slice(0, -1).join('/')

/** "a/b/c" -> ["a", "a/b", "a/b/c"] */
const pathPrefixes = (path: string) => {
  const segments = path ? path.split('/') : []
  return segments.map((_, i) => segments.slice(0, i + 1).join('/'))
}

export default function CourseExplorer({ course, path, onNavigate, onBack }: CourseExplorerProps) {
  const tree = useMemo(() => getCourseTree(course.path), [course.path])
  // Unknown paths (stale links) fall back to the course root.
  const current = findNode(tree, path) ?? tree
  const currentFolder = current.kind === 'folder' ? current : (findNode(tree, parentPath(current.path)) as FolderNode)

  const [expanded, setExpanded] = useState<Set<string>>(() => new Set(pathPrefixes(currentFolder.path)))

  // Folders above the current item always stay open, even after back/forward navigation.
  const visibleExpanded = useMemo(
    () => new Set([...expanded, ...pathPrefixes(parentPath(current.path))]),
    [expanded, current.path],
  )

  const openPath = (target: string) => {
    const node = findNode(tree, target)
    const folderPath = node?.kind === 'folder' ? target : parentPath(target)
    setExpanded((prev) => new Set([...prev, ...pathPrefixes(folderPath)]))
    onNavigate(target)
  }

  const toggleFolder = (folder: FolderNode) => {
    setExpanded((prev) => {
      const next = new Set(prev)
      if (next.has(folder.path)) next.delete(folder.path)
      else next.add(folder.path)
      return next
    })
  }

  const breadcrumbs = current.path ? current.path.split('/') : []

  return (
    <Box minH="100vh" bg="#fafafa" py={{ base: 6, md: 10 }}>
      <Container maxW="container.2xl" px={{ base: 4, md: 8 }}>
        <Flex align="center" gap={4} mb={8} wrap="wrap">
          <Box
            as="button"
            onClick={onBack}
            bg="white"
            px={5}
            py={2}
            borderRadius="full"
            shadow="sm"
            color="gray.700"
            fontSize="md"
            transition="all 0.2s"
            _hover={{ shadow: 'md', transform: 'translateX(-2px)' }}
          >
            ← All courses
          </Box>
          <Box>
            <Heading size="4xl" fontWeight="light" lineHeight="1.1">
              {course.code}
            </Heading>
            <Flex align="baseline" gap={3} wrap="wrap">
              <Text fontSize="xl" color="gray.600">
                {course.name}
              </Text>
              <Text fontSize="sm" color="gray.500">
                | will be updated with a unique page in the future
              </Text>
            </Flex>
          </Box>
        </Flex>

        <Flex gap={6} align="stretch" h={{ md: 'calc(100vh - 220px)' }} minH="480px">
          <Box
            as="nav"
            display={{ base: 'none', md: 'block' }}
            w="280px"
            flexShrink={0}
            bg="white"
            borderRadius="xl"
            shadow="md"
            py={4}
            overflowY="auto"
          >
            <Text px={4} mb={2} fontSize="xs" letterSpacing="widest" color="gray.500" fontFamily="'Arsenal SC', serif">
              Explorer
            </Text>
            <TreeRow
              node={tree}
              depth={0}
              label={course.code}
              activePath={current.path}
              expanded={visibleExpanded}
              onToggle={toggleFolder}
              onOpen={openPath}
              isRoot
            />
          </Box>

          <Flex direction="column" flex={1} minW={0}>
            <Flex align="center" wrap="wrap" gap={1} mb={4} fontSize="lg" color="gray.500">
              <Crumb label={course.code} onClick={() => openPath('')} isLast={breadcrumbs.length === 0} />
              {breadcrumbs.map((segment, i) => (
                <Flex key={i} align="center" gap={1}>
                  <Text as="span">/</Text>
                  <Crumb
                    label={segment}
                    onClick={() => openPath(breadcrumbs.slice(0, i + 1).join('/'))}
                    isLast={i === breadcrumbs.length - 1}
                  />
                </Flex>
              ))}
            </Flex>

            <Box flex={1} minH={0} overflowY="auto" p={1}>
              {current.kind === 'folder' ? (
                <FolderGrid folder={current} onOpen={openPath} />
              ) : (
                <FilePreview key={current.path} file={current} />
              )}
            </Box>
          </Flex>
        </Flex>
      </Container>
    </Box>
  )
}

function Crumb({ label, onClick, isLast }: { label: string; onClick: () => void; isLast: boolean }) {
  return (
    <Box
      as="button"
      onClick={onClick}
      color={isLast ? 'gray.800' : 'gray.500'}
      _hover={{ color: 'blue.500' }}
      transition="color 0.2s"
    >
      {label}
    </Box>
  )
}

interface TreeRowProps {
  node: TreeNode
  depth: number
  label?: string
  activePath: string
  expanded: Set<string>
  onToggle: (folder: FolderNode) => void
  onOpen: (path: string) => void
  isRoot?: boolean
}

function TreeRow({ node, depth, label, activePath, expanded, onToggle, onOpen, isRoot }: TreeRowProps) {
  const isFolder = node.kind === 'folder'
  const isOpen = isRoot || (isFolder && expanded.has(node.path))
  const isActive = node.path === activePath

  return (
    <>
      <Flex
        as="button"
        w="full"
        align="center"
        gap={2}
        pl={`${12 + depth * 14}px`}
        pr={3}
        py="3px"
        textAlign="left"
        fontSize="md"
        pos="relative"
        color={isActive ? 'gray.900' : 'gray.700'}
        _hover={{ bg: 'gray.50' }}
        onClick={() => {
          if (isFolder && !isRoot && (isActive || !isOpen)) onToggle(node)
          onOpen(node.path)
        }}
      >
        {isActive && (
          // Shared layoutId: one border that glides to whichever row is selected.
          <MotionBox
            layoutId="tree-selection"
            pos="absolute"
            inset="0 6px"
            border="1.5px solid"
            borderColor="blue.400"
            borderRadius="md"
            pointerEvents="none"
            transition={{ type: 'spring', stiffness: 350, damping: 35 }}
          />
        )}
        <Box w="10px" flexShrink={0} fontSize="xs" color="gray.400">
          {isFolder && !isRoot ? (isOpen ? '▾' : '▸') : ''}
        </Box>
        {isFolder ? <FolderIcon size={16} /> : <FileIcon file={node} size={16} />}
        <Text truncate fontWeight={isRoot ? 'semibold' : 'normal'}>
          {label ?? node.name}
        </Text>
      </Flex>
      {isFolder &&
        isOpen &&
        node.children.map((child) => (
          <TreeRow
            key={child.path}
            node={child}
            depth={isRoot ? depth : depth + 1}
            activePath={activePath}
            expanded={expanded}
            onToggle={onToggle}
            onOpen={onOpen}
          />
        ))}
    </>
  )
}

function FolderGrid({ folder, onOpen }: { folder: FolderNode; onOpen: (path: string) => void }) {
  if (folder.children.length === 0) {
    return (
      <Text color="gray.500" textAlign="center" py={20}>
        Nothing has been uploaded for this course yet.
      </Text>
    )
  }

  return (
    <SimpleGrid columns={{ base: 2, md: 3, lg: 4, xl: 5 }} gap={{ base: 4, md: 6 }}>
      {folder.children.map((child) => (
        <Flex
          key={child.path}
          as="button"
          onClick={() => onOpen(child.path)}
          direction="column"
          align="center"
          justify="center"
          gap={3}
          aspectRatio={1}
          p={4}
          bg="white"
          borderRadius="xl"
          shadow="md"
          transition="all 0.2s"
          _hover={{ transform: 'translateY(-4px)', shadow: 'lg' }}
        >
          {child.kind === 'folder' ? <FolderIcon size={56} /> : <FileIcon file={child} size={56} />}
          <Text fontSize="lg" lineHeight="1.2" textAlign="center" lineClamp={2} wordBreak="break-word">
            {child.name}
          </Text>
          <Text fontSize="sm" color="gray.500">
            {child.kind === 'folder'
              ? `${child.children.length} item${child.children.length === 1 ? '' : 's'}`
              : child.ext.toUpperCase() || 'File'}
          </Text>
        </Flex>
      ))}
    </SimpleGrid>
  )
}

function FilePreview({ file }: { file: FileNode }) {
  return (
    <Box bg="white" borderRadius="xl" shadow="md" overflow="hidden">
      <Flex align="center" gap={3} px={5} py={3} borderBottom="1px solid" borderColor="gray.100">
        <FileIcon file={file} size={20} />
        <Text fontSize="lg" truncate flex={1}>
          {file.name}
        </Text>
        {file.url && (
          <a href={file.url} download={file.name}>
            <Text fontSize="sm" color="blue.500" _hover={{ textDecoration: 'underline' }}>
              Download
            </Text>
          </a>
        )}
      </Flex>
      <FileBody file={file} />
    </Box>
  )
}

function FileBody({ file }: { file: FileNode }) {
  const [text, setText] = useState<string | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    if (!file.loadText) return
    let cancelled = false
    file
      .loadText()
      .then((content) => !cancelled && setText(content))
      .catch(() => !cancelled && setError(true))
    return () => {
      cancelled = true
    }
  }, [file])

  if (file.url) {
    if (IMAGE_EXTS.has(file.ext)) {
      return (
        <Flex justify="center" p={6} bg="gray.50">
          <Image src={file.url} alt={file.name} maxH="70vh" borderRadius="md" shadow="sm" />
        </Flex>
      )
    }
    if (file.ext === 'pdf') {
      return <Box as="iframe" {...{ src: file.url, title: file.name }} w="full" h="75vh" border={0} />
    }
    return (
      <Text color="gray.500" textAlign="center" py={16}>
        This file can't be previewed in the browser — use Download to open it.
      </Text>
    )
  }

  if (error) {
    return (
      <Text color="gray.500" textAlign="center" py={16}>
        This file couldn't be loaded.
      </Text>
    )
  }
  if (text === null) {
    return (
      <Text color="gray.500" textAlign="center" py={16}>
        Loading…
      </Text>
    )
  }

  if (!text.trim()) {
    return (
      <Text color="gray.500" textAlign="center" py={16}>
        This file is empty.
      </Text>
    )
  }

  if (file.ext === 'ipynb') return <NotebookView source={text} />

  const isTruncated = text.length > PREVIEW_LIMIT
  return (
    <>
      {isTruncated && (
        <Text px={5} py={2} fontSize="sm" color="gray.600" bg="yellow.50">
          Large file — showing the first {Math.round(PREVIEW_LIMIT / 1000)} KB.
        </Text>
      )}
      <CodeBlock code={isTruncated ? text.slice(0, PREVIEW_LIMIT) : text} language={languageFor(file)} showLineNumbers />
    </>
  )
}

function CodeBlock({ code, language, showLineNumbers }: { code: string; language: string; showLineNumbers?: boolean }) {
  return (
    <SyntaxHighlighter
      language={language}
      style={oneLight}
      showLineNumbers={showLineNumbers}
      wrapLongLines={language === 'text' || language === 'markdown'}
      customStyle={{ margin: 0, padding: '16px 20px', background: 'transparent', fontSize: '13px' }}
      codeTagProps={{ style: { background: 'transparent' } }}
    >
      {code}
    </SyntaxHighlighter>
  )
}

interface NotebookCell {
  cell_type: 'code' | 'markdown' | 'raw'
  source: string | string[]
  outputs?: Array<{
    output_type: string
    text?: string | string[]
    data?: Record<string, string | string[]>
    ename?: string
    evalue?: string
  }>
}

const joinSource = (source: string | string[] | undefined) =>
  Array.isArray(source) ? source.join('') : (source ?? '')

/** Minimal read-only Jupyter renderer: code, plain-text markdown, and text/image outputs. */
function NotebookView({ source }: { source: string }) {
  const notebook = useMemo(() => {
    try {
      return JSON.parse(source) as {
        cells: NotebookCell[]
        metadata?: { kernelspec?: { language?: string }; language_info?: { name?: string } }
      }
    } catch {
      return null
    }
  }, [source])

  if (!notebook?.cells) return <CodeBlock code={source.slice(0, PREVIEW_LIMIT)} language="json" />

  const language =
    notebook.metadata?.kernelspec?.language ?? notebook.metadata?.language_info?.name ?? 'python'

  return (
    <Flex direction="column" gap={4} p={5}>
      {notebook.cells.map((cell, i) => {
        const cellSource = joinSource(cell.source)
        if (cell.cell_type !== 'code') {
          return (
            <Box key={i} px={2}>
              {cellSource.split('\n').map((line, j) => {
                const heading = line.match(/^#{1,6}\s+(.*)/)
                return heading ? (
                  <Text key={j} fontSize="xl" fontWeight="semibold" color="gray.800" mt={j > 0 ? 3 : 0}>
                    {heading[1]}
                  </Text>
                ) : (
                  <Text key={j} whiteSpace="pre-wrap" fontSize="md" color="gray.700" minH="1em">
                    {line}
                  </Text>
                )
              })}
            </Box>
          )
        }
        return (
          <Box key={i}>
            <Box bg="gray.50" borderRadius="md" border="1px solid" borderColor="gray.100">
              <CodeBlock code={cellSource} language={language} />
            </Box>
            {cell.outputs?.map((output, j) => {
              const image = output.data?.['image/png']
              if (image) {
                return (
                  <Image key={j} src={`data:image/png;base64,${joinSource(image)}`} alt="Cell output" maxW="full" mt={2} />
                )
              }
              const outputText =
                output.output_type === 'error'
                  ? `${output.ename}: ${output.evalue}`
                  : joinSource(output.text ?? output.data?.['text/plain'])
              if (!outputText) return null
              return (
                <Box
                  key={j}
                  as="pre"
                  mt={2}
                  px={4}
                  py={2}
                  fontSize="12px"
                  fontFamily="mono"
                  whiteSpace="pre-wrap"
                  color={output.output_type === 'error' ? 'red.600' : 'gray.700'}
                  borderLeft="3px solid"
                  borderColor={output.output_type === 'error' ? 'red.200' : 'gray.200'}
                  maxH="400px"
                  overflowY="auto"
                >
                  {outputText.slice(0, PREVIEW_LIMIT)}
                </Box>
              )
            })}
          </Box>
        )
      })}
    </Flex>
  )
}

function FolderIcon({ size }: { size: number }) {
  return (
    <Box as="span" color="blue.400" flexShrink={0} display="inline-flex">
      <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" aria-hidden>
        <path d="M3 6.5A2.5 2.5 0 0 1 5.5 4h3.59a2 2 0 0 1 1.42.59L12 6h6.5A2.5 2.5 0 0 1 21 8.5v9a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5z" />
      </svg>
    </Box>
  )
}

function FileIcon({ file, size }: { file: FileNode; size: number }) {
  const color = EXT_COLORS[file.ext] ?? '#8a8f98'
  const showLabel = size >= 40 && file.ext.length > 0 && file.ext.length <= 5
  return (
    <Box as="span" flexShrink={0} display="inline-flex">
      <svg width={size} height={size} viewBox="0 0 24 24" aria-hidden>
        <path d="M6 2h8l6 6v12.5A1.5 1.5 0 0 1 18.5 22h-12A1.5 1.5 0 0 1 5 20.5v-17A1.5 1.5 0 0 1 6.5 2z" fill="#f1f3f5" stroke={color} strokeWidth="1.2" />
        <path d="M14 2v6h6" fill="none" stroke={color} strokeWidth="1.2" />
        {showLabel ? (
          <text
            x="12.5"
            y="17.5"
            textAnchor="middle"
            fill={color}
            // inline style so the page's font rules can't override the tiny SVG font size
            style={{ fontSize: '5px', fontWeight: 700, fontFamily: 'system-ui, sans-serif' }}
          >
            {file.ext.toUpperCase()}
          </text>
        ) : (
          <rect x="8" y="14" width="9" height="2" rx="1" fill={color} />
        )}
      </svg>
    </Box>
  )
}
