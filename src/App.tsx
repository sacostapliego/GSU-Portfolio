import { Box, Container, Heading, SimpleGrid } from '@chakra-ui/react'
import CourseCard from './components/Coursecard'
import { courses } from './data/courses'

function App() {
  return (
    <Box minH="100vh" minW={"100vw"} bg="#0071CE" py={10}>
      <Container maxW="container.xl">
        <Heading as="h1" size="2xl" mb={8} textAlign="center">
          GSU Computer Science Portfolio
        </Heading>
        <Heading as="h2" size="lg" mb={6} textAlign="center">
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