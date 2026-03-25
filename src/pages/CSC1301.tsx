import {
  Box,
  Button,
  Container,
  Flex,
  Heading,
  Stack,
  Text,
} from '@chakra-ui/react'
import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import PyodideTerminal from '../components/PyodideTerminal'
import { csc1301Programs } from '../data/csc1301Programs'

interface CSC1301Props {
  onBack: () => void
}

export default function CSC1301({ onBack }: CSC1301Props) {
  const [selectedProgramIndex, setSelectedProgramIndex] = useState(0)
  const [activeView, setActiveView] = useState<'run' | 'code'>('run')

  const selectedProgram = csc1301Programs[selectedProgramIndex]

  return (
    <Box minH="100vh" bg="#000000" py={{ base: 3, md: 4 }}>
      <Container maxW="100%" px={{ base: 3, md: 4 }}>
        <Box
          minH="calc(100vh - 32px)"
          bg="#000000"
          border="1px solid"
          borderRadius="md"
          p={{ base: 3, md: 4 }}
        >
          <Stack gap={4} h="full">
            <Flex justify="space-between" align={{ base: 'start', md: 'center' }} direction={{ base: 'column', md: 'row' }} gap={3}>
              <Heading color="#31ff77" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace" size={{ base: 'lg', md: 'xl' }}>
                CSC 1301 Terminal Session
              </Heading>

              <Button
                onClick={onBack}
                variant="outline"
                borderColor="#1a8f49"
                color="#31ff77"
                bg="#000000"
                _hover={{ bg: '#03180b', borderColor: '#4bff95' }}
                fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
                size="sm"
              >
                exit {'->'} courses
              </Button>
            </Flex>

            <Box
              border="1px solid"
              borderColor="#1a8f49"
              bg="#000000"
              borderRadius="md"
              p={3}
              fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
            >
              <Text color="#80e5a8" mt={1}>Welcome to CSC 1301: Principles of Computer Science I.</Text>
            </Box>

            <Flex direction={{ base: 'column', lg: 'row' }} gap={4} align="stretch" flex="1">
              <Box
                w={{ base: '100%', lg: '36%' }}
                border="1px solid"
                borderColor="#1a8f49"
                borderRadius="md"
                p={3}
                bg="#000000"
                maxH={{ base: '280px', lg: 'none' }}
                overflowY="auto"
              >
                <Text color="#31ff77" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace" mb={3}>
                  Available Programs
                </Text>

                <Stack gap={2}>
                  {csc1301Programs.map((program, index) => {
                    const selected = index === selectedProgramIndex
                    return (
                      <Button
                        key={program.id}
                        justifyContent="start"
                        onClick={() => setSelectedProgramIndex(index)}
                        bg={selected ? '#04381a' : '#000000'}
                        color={selected ? '#72ffad' : '#8de3b0'}
                        border="1px solid"
                        borderColor={selected ? '#4bff95' : '#1a8f49'}
                        _hover={{ bg: '#03250f', borderColor: '#4bff95' }}
                        fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
                        fontWeight="normal"
                        size="sm"
                        whiteSpace="normal"
                        h="auto"
                        py={2}
                      >
                        {`${index + 1}. ${program.fileName}`}
                      </Button>
                    )
                  })}
                </Stack>
              </Box>

              <Box
                w={{ base: '100%', lg: '64%' }}
                border="1px solid"
                borderColor="#1a8f49"
                borderRadius="md"
                p={3}
                bg="#000000"
                overflow="hidden"
              >
                <Stack gap={3} h="full">
                  <Box>
                    <Text color="#31ff77" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace">
                      $ load {selectedProgram.fileName}
                    </Text>
                    <Text color="#8de3b0" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace" mt={1}>
                      {selectedProgram.description}
                    </Text>
                  </Box>

                  <Flex gap={2} wrap="wrap">
                    <Button
                      onClick={() => setActiveView('run')}
                      size="sm"
                      bg={activeView === 'run' ? '#04381a' : '#000000'}
                      color={activeView === 'run' ? '#72ffad' : '#8de3b0'}
                      border="1px solid"
                      borderColor={activeView === 'run' ? '#4bff95' : '#1a8f49'}
                      _hover={{ bg: '#03250f', borderColor: '#4bff95' }}
                      fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
                    >
                      run
                    </Button>

                    <Button
                      onClick={() => setActiveView('code')}
                      size="sm"
                      bg={activeView === 'code' ? '#04381a' : '#000000'}
                      color={activeView === 'code' ? '#72ffad' : '#8de3b0'}
                      border="1px solid"
                      borderColor={activeView === 'code' ? '#4bff95' : '#1a8f49'}
                      _hover={{ bg: '#03250f', borderColor: '#4bff95' }}
                      fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace"
                    >
                      code
                    </Button>
                  </Flex>

                  {activeView === 'run' ? (
                    <Box border="1px solid" borderColor="#1a8f49" borderRadius="md" p={3} bg="#000000">
                      <Text color="#31ff77" fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace">
                        $ {selectedProgram.runCommand}
                      </Text>
                      <Text color="#8de3b0" mt={2} mb={4} fontFamily="'Cascadia Code', 'Consolas', 'Fira Code', monospace">
                        Running pyodide-adapted version in browser terminal.
                      </Text>

                      <PyodideTerminal
                        programTitle={selectedProgram.title}
                        sourceCode={selectedProgram.pyodideSourceCode}
                        suggestedInput={selectedProgram.suggestedInput}
                      />
                    </Box>
                  ) : (
                    <Box border="1px solid" borderColor="#1a8f49" borderRadius="md" overflowX="auto">
                      <SyntaxHighlighter
                        language="python"
                        style={atomDark}
                        customStyle={{ margin: 0, background: '#000000', fontSize: '0.9rem' }}
                        showLineNumbers
                      >
                        {selectedProgram.originalSourceCode}
                      </SyntaxHighlighter>
                    </Box>
                  )}
                </Stack>
              </Box>
            </Flex>
          </Stack>
        </Box>
      </Container>
    </Box>
  )
}
