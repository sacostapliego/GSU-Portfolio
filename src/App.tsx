import { Box, Container, Heading, SimpleGrid, Image, Input, VStack, Text, Flex, useBreakpointValue } from '@chakra-ui/react'
import { useEffect, useState, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { courses } from './data/courses'
import CSC1301 from './pages/CSC1301'
import type { Course } from './types'

const MotionBox = motion(Box as any)

function App() {
  const [hashRoute, setHashRoute] = useState(() => window.location.hash)

  useEffect(() => {
    const handleHashChange = () => setHashRoute(window.location.hash)
    window.addEventListener('hashchange', handleHashChange)

    return () => {
      window.removeEventListener('hashchange', handleHashChange)
    }
  }, [])

  if (hashRoute === '#/courses/csc-1301') {
    return <CSC1301 onBack={() => (window.location.hash = '')} />
  }

  return <PortfolioHome onNavigation={(route) => {
    window.location.hash = route
  }}/>
}

function PortfolioHome({ onNavigation }: { onNavigation: (route: string) => void }) {
  const [currentIndex, setCurrentIndex] = useState(0)
  
  // Search and Filter State
  const [searchQuery, setSearchQuery] = useState('')
  const [isSearchFocused, setIsSearchFocused] = useState(false)
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null)
  
  const searchContainerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setIsSearchFocused(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  const languages = useMemo(() => {
    const langs = new Set<string>()
    courses.forEach(c => c.language && langs.add(c.language))
    return Array.from(langs)
  }, [])

  const filteredCourses = useMemo(() => {
    return courses.filter(c => {
      const matchSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.code.toLowerCase().includes(searchQuery.toLowerCase())
      const matchLang = selectedLanguage ? c.language === selectedLanguage : true
      return matchSearch && matchLang
    })
  }, [searchQuery, selectedLanguage])

  // Responsive Carousel Logic
  // 5 items for 2xl, 3 items for others
  const is2xl = useBreakpointValue({ base: false, '2xl': true })
  
  const handleNext = () => setCurrentIndex((prev) => (prev + 1) % courses.length)
  const handlePrev = () => setCurrentIndex((prev) => (prev - 1 + courses.length) % courses.length)

  const handleLinkCourse = (course: Course) => {
    if (course.link) {
      const isExternal = /^https?:\/\//.test(course.link)
      if (isExternal) {
        window.open(course.link, '_blank')
      } else {
        onNavigation(course.link)
      }
    }
  }

  // Calculate carousel positions
  const getCarouselItems = () => {
    const total = courses.length
    
    // We want to show a window of items. For 2xl it's 5 (-2, -1, 0, 1, 2)
    // For smaller screens, it's 3 (-1, 0, 1)
    const windowOffset = is2xl ? 2 : 1
    
    return courses.map((course, index) => {
        let diff = index - currentIndex
        // Handle wrapping for infinite carousel effect
        if (diff > total / 2) diff -= total
        if (diff < -total / 2) diff += total
        
        const isVisible = Math.abs(diff) <= windowOffset
        
        let zIndex = 10 - Math.abs(diff)
        // Scaled down progressively so they fit cleanly side-by-side on screen
        let scale = diff === 0 ? 1 : 0.9 - Math.abs(diff) * 0.1
        let opacity = diff === 0 ? 1 : 0.6
        
        // Spread items apart using relative sizing instead of absolute fixed pixels
        let translateX = `${diff * 110}%`

        if (!isVisible) {
            opacity = 0
            // Keep off-screen items slightly further out functionally
            translateX = diff > 0 ? `${(windowOffset + 1) * 110}%` : `-${(windowOffset + 1) * 110}%`
        }

        return {
            course,
            offset: diff,
            isVisible,
            styles: {
                zIndex,
                scale,
                opacity,
                translateX
            }
        }
    })
  }

  return (
    <Box minH="100vh" minW="100%" bg="#fafafa" py={10} overflowX="hidden">
      <Container maxW="container.2xl">
        <Heading size="5xl" mb={4} fontWeight="light" textAlign="center">
          GSU Computer Science Portfolio
        </Heading>
        <Heading size="2xl" mb={12} fontWeight="light" textAlign="center" color="gray.600">
          Steven Acosta-Pliego
        </Heading>
        
        {/* CAROUSEL SECTION */}
        <Box pos="relative" h={{ base: "300px", md: "400px", lg: "500px" }} mb={{ base: 24, lg: 32 }} mt={20} display="flex" alignItems="center" justifyContent="center">
            {getCarouselItems().map(({ course, offset, isVisible, styles }) => (
                <MotionBox
                    key={course.id} 
                    pos="absolute"
                    initial={false}
                    animate={{ 
                        opacity: styles.opacity, 
                        x: styles.translateX, 
                        scale: styles.scale 
                    }}
                    transition={{ type: "spring", stiffness: 350, damping: 35 }}
                    style={{ zIndex: styles.zIndex }}
                    cursor={offset === 0 ? 'pointer' : (isVisible ? 'pointer' : 'default')}
                    pointerEvents={isVisible ? "auto" : "none"}
                    onClick={() => {
                        if (!isVisible) return
                        if (offset === 0) handleLinkCourse(course)
                        else if (offset > 0) handleNext()
                        else handlePrev()
                    }}
                >
                    <Image 
                        src={course.image} 
                        alt={course.code} 
                        w={{ base: "250px", md: "350px", lg: "400px" }}
                        h="auto"
                        shadow="2xl"
                        borderRadius="xl"
                        filter={offset === 0 ? "none" : "grayscale(80%)"}
                        transition="filter 0.3s"
                        _hover={{ filter: offset === 0 ? "none" : "grayscale(50%)" }}
                    />
                </MotionBox>
            ))}
        </Box>

        {/* SEARCH AND GRID SECTION */}
        <Container maxW="container.xl" ref={searchContainerRef} pos="relative" zIndex={20} mt={16}>
            <VStack mb={10} w="full" maxW="lg" mx="auto" position="relative">
              <Box pos="relative" w="full">
                  {selectedLanguage && (
                      <Box pos="absolute" left={2} top="50%" transform="translateY(-50%)" zIndex={2}>
                          <Box 
                              bg="blue.500" 
                              color="white" 
                              px={3} 
                              py={0.5} 
                              borderRadius="full" 
                              fontSize="sm" 
                              fontWeight="medium"
                              textTransform="capitalize"
                              display="flex"
                              alignItems="center"
                          >
                              {selectedLanguage}
                              <Box 
                                  as="button" 
                                  onClick={(e) => { e.stopPropagation(); setSelectedLanguage(null); }} 
                                  ml={2} 
                                  fontSize="md"
                                  lineHeight={1}
                                  opacity={0.8}
                                  _hover={{ opacity: 1 }}
                              >
                                  ×
                              </Box>
                          </Box>
                      </Box>
                  )}
                  <Input
                      placeholder={selectedLanguage ? "Search more..." : "Search courses..."}
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      onFocus={() => setIsSearchFocused(true)}
                      size="lg"
                      bg="white"
                      borderRadius="full"
                      shadow="sm"
                      pl={selectedLanguage ? { base: "110px", md: "120px" } : 6}
                  />
              </Box>
              
              <AnimatePresence>
                  {isSearchFocused && (
                      <MotionBox
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          pos="absolute"
                          top="100%"
                          left={0}
                          right={0}
                          mt={2}
                          bg="white"
                          p={4}
                          borderRadius="xl"
                          shadow="xl"
                          border="1px"
                          borderColor="gray.100"
                      >
                          <Text fontWeight="medium" mb={3} fontSize="sm" color="gray.500">
                              Filter by Programming Language
                          </Text>
                          <Flex flexWrap="wrap" gap={2}>
                              <Box
                                  as="button"
                                  px={3} py={1}
                                  borderRadius="full"
                                  fontSize="sm"
                                  bg={selectedLanguage === null ? "blue.500" : "gray.100"}
                                  color={selectedLanguage === null ? "white" : "gray.700"}
                                  onClick={() => setSelectedLanguage(null)}
                              >
                                  All
                              </Box>
                              {languages.map(lang => (
                                  <Box
                                      key={lang}
                                      as="button"
                                      px={3} py={1}
                                      borderRadius="full"
                                      fontSize="sm"
                                      textTransform="capitalize"
                                      bg={selectedLanguage === lang ? "blue.500" : "gray.100"}
                                      color={selectedLanguage === lang ? "white" : "gray.700"}
                                      onClick={() => setSelectedLanguage(lang)}
                                  >
                                      {lang}
                                  </Box>
                              ))}
                          </Flex>
                      </MotionBox>
                  )}
              </AnimatePresence>
            </VStack>
            
            <SimpleGrid columns={{ base: 1, sm: 2, md: 3, lg: 4 }} gap={8}>
              {filteredCourses.map((course) => (
                  <Box 
                      key={course.id} 
                      as="button"
                      onClick={() => handleLinkCourse(course)}
                      textAlign="left"
                      transition="transform 0.2s"
                      _hover={{ transform: 'translateY(-4px)' }}
                  >
                      <Image 
                          src={course.image} 
                          alt={course.code} 
                          w="full" 
                          borderRadius="xl" 
                          shadow="md" 
                      />
                  </Box>
              ))}
              {filteredCourses.length === 0 && (
                  <Text color="gray.500" textAlign="center" gridColumn="1 / -1" py={10}>
                      No courses found matching your criteria.
                  </Text>
              )}
            </SimpleGrid>
        </Container>
      </Container>
    </Box>
  )
}

export default App