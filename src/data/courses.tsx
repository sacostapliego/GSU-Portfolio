import type { Course } from '../types'
import img1301 from '../assets/course-images/1301.png'
import img1302 from '../assets/course-images/1302.png'
import img2510 from '../assets/course-images/2510.png'
import img2720 from '../assets/course-images/2720.png'
import img3020 from '../assets/course-images/3020.png'
import img3210 from '../assets/course-images/3210.png'
import img3320 from '../assets/course-images/3320.png'
import img3350 from '../assets/course-images/3350.png'
import img4320 from '../assets/course-images/4320.png'
import img4370 from '../assets/course-images/4370.png'
import img4520 from '../assets/course-images/4520.png'
import img4760 from '../assets/course-images/4760.png'

export const courses: Course[] = [
  {
    id: 'csc-1301',
    code: 'CSC 1301',
    name: 'Principles of Computer Science I',
    language: 'python',
    path: '1301 - Principles of Computer Science I',
    image: img1301
  },
  {
    id: 'csc-1302',
    code: 'CSC 1302',
    name: 'Principles of Computer Science II',
    language: 'python',
    path: '1302 - Principles of Computer Science II',
    image: img1302
  },
  {
    id: 'csc-2510',
    code: 'CSC 2510',
    name: 'Theory Foundations of Computer Science',
    language: 'python',
    path: '2510 - Principles of Computer Science',
    image: img2510
  },
  {
    id: 'csc-2720',
    code: 'CSC 2720',
    name: 'Data Structures and Algorithms',
    language: 'python',
    path: '2720 - Data Structures and Algorithms',
    image: img2720
  },
  {
    id: 'math-3020',
    code: 'MATH 3020',
    name: 'Probability & Stats for Computer Science',
    language: 'r',
    path: '3020 - Probability & Stats for Computer Science',
    image: img3020
  },
  {
    id: 'csc-3210',
    code: 'CSC 3210',
    name: 'Computer Org & Programming',
    language: 'assembly',
    path: '3210 - Computer Org & Programming',
    image: img3210
  },
  {
    id: 'csc-3320',
    code: 'CSC 3320',
    name: 'System Level Programming',
    language: 'c',
    path: '3320 - System Level Programming',
    image: img3320
  },
  {
    id: 'csc-3350',
    code: 'CSC 3350',
    name: 'Software Development',
    language: 'java',
    path: '3350 - Software Development',
    image: img3350
  },
  {
    id: 'csc-4320',
    code: 'CSC 4320',
    name: 'Operating Systems',
    language: 'java',
    path: '4320 - Operating Systems',
    image: img4320
  },
  {
    id: 'csc-4370',
    code: 'CSC 4370',
    name: 'Web Programming',
    language: 'mixed',
    path: '4370 - Web Programming',
    image: img4370,
    link: './4370 - Web Programming/Assignment1/index.html'
  },
  {
    id: 'csc-4520',
    code: 'CSC 4520',
    name: 'Design & Analysis of Algorithms',
    language: 'mixed',
    path: '4520 - Design & Analysis of Algorithms',
    image: img4520
  },
  {
    id: 'csc-4760',
    code: 'CSC 4760',
    name: 'Big Data Programming',
    language: 'python',
    path: '4760 - Big Data Programming',
    image: img4760
  },
]