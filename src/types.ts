export interface Course {
  id: string
  code: string
  name: string
  language: 'python' | 'java' | 'c' | 'r' | 'assembly' | 'mixed'
  path: string
  image?: string
  link?: string
}

export interface Project {
  id: string
  title: string
  courseId: string
  type: 'lab' | 'homework' | 'project'
  language: string
  files: ProjectFile[]
}

export interface ProjectFile {
  name: string
  path: string
  content: string
}