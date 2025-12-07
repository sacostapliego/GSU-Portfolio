import { Card, Heading, Text, Stack, Image } from '@chakra-ui/react'
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
        <Stack gap={3} alignItems={'center'}>

          <Heading 
            fontSize={'3xl'}
            fontWeight={'light'}
            >
              {course.code}
          </Heading>

          <Image 
            w={'200px'} 
            h={'100%'} 
            objectFit="cover" 
            src={course.image} 
            alt={course.name} 
            />

          <Text color="gray.600">{course.name}</Text>
        </Stack>
      </Card.Body>
    </Card.Root>
  )
}