import { Box, Flex, Text, VStack, Image } from '@chakra-ui/react'
import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import PyodideTerminal from '../components/PyodideTerminal'
import { csc1301Programs } from '../data/csc1301Programs'

interface CSC1301Props {
  onBack: () => void
}

export default function CSC1301({ onBack }: CSC1301Props) {
  const [selectedProgramIndex, setSelectedProgramIndex] = useState(0)

  const selectedProgram = csc1301Programs[selectedProgramIndex]

  // VS Code Dark Theme Colors
  const colors = {
    pageBg: '#0f0f11', // Very dark background providing "gap" styling
    bg: '#1e1e1e',
    sidebar: '#252526',
    border: '#3c3c3c',
    text: '#cccccc',
    activeText: '#ffffff',
    activeBg: '#37373d',
    header: '#323233',
  }

  return (
    <Box
      h="100vh"
      w="100vw"
      bgGradient="to-br"
      gradientFrom="#2563eb"
      gradientTo="#7c3aed"
      color={colors.text}
      display="flex"
      alignItems="center"
      justifyContent="center"
      overflow="hidden"
      position="relative"
      fontFamily="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    >
      {/* macOS Window */}
      <Flex
        w={{ base: '95vw', md: '85vw', lg: '70vw' }}
        h={{ base: '80vh', md: '80vh' }}
        bg={colors.bg}
        borderRadius="2xl"
        boxShadow="0 25px 50px -12px rgba(0, 0, 0, 0.75)"
        direction="column"
        overflow="hidden"
        border="1px solid"
        borderColor="#3c3c3c"
        mb={10} // Offset a bit to make room for the dock visually
      >
        {/* Title Bar (macOS style) */}
        <Flex h="36px" bg={colors.sidebar} align="center" justify="space-between" px={4}>
          {/* Traffic Lights */}
          <Flex gap="8px" flex={1}>
            <Box w="12px" h="12px" borderRadius="full" bg="#ff5f56" border="1px solid #e0443e" />
            <Box w="12px" h="12px" borderRadius="full" bg="#ffbd2e" border="1px solid #dea123" />
            <Box w="12px" h="12px" borderRadius="full" bg="#27c93f" border="1px solid #1aab29" />
          </Flex>
          
          <Text flex={2} textAlign="center" fontSize="xs" color="#8b949e">
            GSU Portfolio
          </Text>

          <Flex flex={1} justify="flex-end">
            {/* Controls removed in favor of the dock */}
          </Flex>
        </Flex>

        {/* Content Area */}
        <Flex flex={1} overflow="hidden">
          {/* Sidebar */}
          <Box w={{ base: '180px', md: '280px' }} bg={colors.sidebar} borderRight="1px" borderColor={colors.border} display="flex" flexDirection="column" overflow="hidden">
            <Text px={5} py={4} fontSize="sm" fontWeight="semibold" textTransform="uppercase" color="#8b949e">
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
                    <Image src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" boxSize="15px" flexShrink={0} />
                    <Text>{program.fileName}</Text>
                  </Box>
                )
              })}
            </VStack>
          </Box>

          {/* Editor + Terminal Area */}
          <Flex flex={1} direction="column" minW={0}>
            {/* Top Half: Code Editor */}
            <Box flex={1} bg={colors.bg} display="flex" flexDirection="column" overflow="hidden">
              {/* Editor Tabs */}
              <Flex h="45px" bg={colors.sidebar} borderBottom="1px " borderColor={colors.border} align="end">
                 <Box h="100%" px={5} bg={colors.bg} color={colors.activeText} borderTop="2px solid #007acc" display="flex" alignItems="center" gap={2}>
                   <Image src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" boxSize="16px" flexShrink={0} />
                   <Text fontSize="15px" whiteSpace="nowrap">{selectedProgram.fileName}</Text>
                 </Box>
              </Flex>
              {/* Code */}
              <Box flex={1} overflow="auto" bg={colors.bg} mt={2}>
                 <SyntaxHighlighter
                   language="python"
                   style={vscDarkPlus}
                   customStyle={{ margin: 0, background: colors.bg, fontSize: '16px', minHeight: '100%', padding: '0 10px' }}
                   showLineNumbers
                 >
                   {selectedProgram.originalSourceCode}
                 </SyntaxHighlighter>
              </Box>
            </Box>

            {/* Bottom Half: Terminal */}
            <Box h={{ base: "30rem", md: "45%" }} bg={colors.bg} borderTop="1px" borderColor={colors.border} display="flex" flexDirection="column" overflow="hidden">
               <Flex h="40px" align="center" px={5}>
                  <Text fontSize="14px" fontWeight="semibold" color={colors.text} textTransform="uppercase" letterSpacing="0.05em">TERMINAL</Text>
               </Flex>
               <Box flex={1} p={3} overflow="hidden">
                 <PyodideTerminal
                   key={selectedProgram.id} // Add key to force re-render when changing programs
                   programTitle={selectedProgram.title}
                   sourceCode={selectedProgram.pyodideSourceCode}
                   suggestedInput={selectedProgram.suggestedInput}
                 />
               </Box>
            </Box>
          </Flex>
        </Flex>
      </Flex>

      {/* macOS Dock */}
      <Flex
        position="absolute"
        bottom="16px"
        left="50%"
        transform="translateX(-50%)"
        direction="column"
        alignItems="center"
        gap={2}
      >
        <Text
          px={4}
          py={1.5}
          borderRadius="full"
          bg="rgba(255, 255, 255, 0.12)"
          border="1px solid rgba(255, 255, 255, 0.18)"
          color="#f5f7fb"
          fontSize="sm"
          fontWeight="medium"
          letterSpacing="0.02em"
          backdropFilter="blur(12px)"
        >
          Go back home
        </Text>

        <Flex
          bg="rgba(255, 255, 255, 0.15)"
          backdropFilter="blur(24px)"
          border="1px solid rgba(255, 255, 255, 0.3)"
          borderRadius="2xl"
          px={4}
          py={3}
          gap={3}
          boxShadow="0 25px 50px -12px rgba(0, 0, 0, 0.5)"
          alignItems="center"
        >
          <Flex
            as="button"
            onClick={onBack}
            w="64px"
            h="64px"
            bg="rgba(255, 255, 255, 0.08)"
            borderRadius="24px"
            justify="center"
            align="center"
            cursor="pointer"
            border="1px solid rgba(255, 255, 255, 0.18)"
            title="Go back home"
          >
            <Image src="/image.png" alt="GSU logo" boxSize="44px" objectFit="contain" />
          </Flex>
          <Box w="64px" h="64px" borderRadius="24px" bg="rgba(255, 255, 255, 0.08)" border="1px solid rgba(255, 255, 255, 0.12)" />
          <Box w="64px" h="64px" borderRadius="24px" bg="rgba(255, 255, 255, 0.08)" border="1px solid rgba(255, 255, 255, 0.12)" />
          <Box w="64px" h="64px" borderRadius="24px" bg="rgba(255, 255, 255, 0.08)" border="1px solid rgba(255, 255, 255, 0.12)" />
        </Flex>
      </Flex>
    </Box>
  )
}
