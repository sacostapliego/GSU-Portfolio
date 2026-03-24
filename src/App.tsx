import { Box, Container, Heading, SimpleGrid } from '@chakra-ui/react'
import { useEffect, useState } from 'react'
import CourseCard from './components/Coursecard'
import { courses } from './data/courses'
import Csc1301Page from './pages/Csc1301Page'

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
    return <Csc1301Page onBack={() => (window.location.hash = '')} />
  }

  return (
    <Box minH="100vh" minW={"90w"} bg="#fff" py={10}>
      <Container color={'black'} maxW="container.xl">
        <Heading size="5xl" mb={8} fontWeight={'light'} textAlign="center">
          GSU Computer Science Portfolio
        </Heading>
        <Heading size="2xl" mb={6} fontWeight={'light'} textAlign="center">
          Steven Acosta-Pliego
        </Heading>
        
        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6} mt={10}>
          {courses.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </SimpleGrid>
      </Container>
    </Box>
  )
}

export default App