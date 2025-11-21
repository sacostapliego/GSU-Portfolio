import { Box, Container, Heading, SimpleGrid } from '@chakra-ui/react'
import CourseCard from './components/Coursecard'
import { courses } from './data/courses'

function App() {
  return (
    <Box minH="100vh" minW={"90w"} bg="#0071CE" py={10}>
      <Container color={'white'} maxW="container.xl">
        <Heading size="5xl" mb={8} textAlign="center">
          GSU Computer Science Portfolio
        </Heading>
        <Heading size="2xl" mb={6} textAlign="center">
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