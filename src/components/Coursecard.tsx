import { Card, Heading, Text, Badge, Box, Stack } from '@chakra-ui/react'
import type { Course } from '../types'

interface CourseCardProps {
  course: Course
}

export default function CourseCard({ course }: CourseCardProps) {
  return (
    <Card.Root
      _hover={{ transform: 'translateY(-4px)', shadow: 'xl' }}
      transition="all 0.3s"
      cursor="pointer"
    >
      <Card.Body>
        <Stack gap={3}>
          <Box>
            <Badge colorScheme={course.language === 'python' ? 'blue' : course.language === 'java' ? 'red' : 'green'}>
              {course.language.toUpperCase()}
            </Badge>
          </Box>
          <Heading size="md">{course.code}</Heading>
          <Text color="gray.600">{course.name}</Text>
        </Stack>
      </Card.Body>
    </Card.Root>
  )
}