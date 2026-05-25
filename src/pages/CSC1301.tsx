import { Box, Button, Flex, Heading, Text, VStack } from '@chakra-ui/react'
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
    <Box h="100vh" w="100vw" bg={colors.pageBg} color={colors.text} display="flex" flexDirection="column" overflow="hidden">
      {/* Main Content */}
      <Flex flex={1} overflow="hidden" p={4} gap={4}>
        {/* Sidebar */}
        <Box w={{ base: '150px', md: '250px' }} bg={colors.sidebar} border="1px" borderColor={colors.border} borderRadius="xl" display="flex" flexDirection="column" overflow="hidden" boxShadow="lg">
          <Text px={4} py={3} fontSize="xs" fontWeight="bold" textTransform="uppercase" color={colors.text} borderBottom="1px" borderColor={colors.border}>
            Explorer
          </Text>
          <VStack align="stretch" gap={0} overflowY="auto" flex={1}>
            {csc1301Programs.map((program, index) => {
              const isActive = index === selectedProgramIndex
              return (
                <Box
                  key={program.id}
                  px={4}
                  py={2}
                  cursor="pointer"
                  bg={isActive ? colors.activeBg : 'transparent'}
                  color={isActive ? colors.activeText : colors.text}
                  _hover={{ bg: isActive ? colors.activeBg : '#2a2d2e' }}
                  onClick={() => setSelectedProgramIndex(index)}
                  fontSize="sm"
                  fontFamily="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                >
                  <Text>📄 {program.fileName}</Text>
                </Box>
              )
            })}
          </VStack>
        </Box>

        {/* Editor Area */}
        <Flex flex={1} direction="column" minW={0} gap={4}>
          {/* Top Half: Code Editor */}
          <Box flex={1} bg={colors.bg} border="1px" borderColor={colors.border} borderRadius="xl" display="flex" flexDirection="column" overflow="hidden" boxShadow="lg">
            {/* Editor Tabs */}
            <Flex h="38px" bg={colors.sidebar} borderBottom="1px " borderColor={colors.border} justify="space-between" align="center">
               <Box h="100%" px={4} bg={colors.bg} color={colors.activeText} borderTop="2px solid #007acc" display="flex" alignItems="center">
                 <Text fontSize="sm" whiteSpace="nowrap">📄 {selectedProgram.fileName}</Text>
               </Box>
               <Box pr={3}>
                 <Button size="xs" onClick={onBack} colorScheme="blue" variant="solid" style={{ borderRadius: '6px' }}>
                   Back to Courses
                 </Button>
               </Box>
            </Flex>
            {/* Code */}
            <Box flex={1} overflow="auto" bg={colors.bg}>
               <SyntaxHighlighter
                 language="python"
                 style={vscDarkPlus}
                 customStyle={{ margin: 0, background: colors.bg, fontSize: '14px', minHeight: '100%' }}
                 showLineNumbers
               >
                 {selectedProgram.originalSourceCode}
               </SyntaxHighlighter>
            </Box>
          </Box>

          {/* Bottom Half: Terminal */}
          <Box h={{ base: "300px", md: "40%" }} bg={colors.bg} border="1px " borderColor={colors.border} borderRadius="xl" display="flex" flexDirection="column" overflow="hidden" boxShadow="lg">
             <Flex h="38px" borderBottom="1px " borderColor={colors.border} align="center" px={4} bg={colors.sidebar}>
                <Text fontSize="sm" fontWeight="bold" color={colors.text} textTransform="uppercase" letterSpacing="0.05em">TERMINAL</Text>
             </Flex>
             <Box flex={1} p={2} overflow="hidden">
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
    </Box>
  )
}
