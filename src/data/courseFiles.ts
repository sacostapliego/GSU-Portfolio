// Every file inside the course folders, keyed by its project-root path
// (e.g. "/1302 - Principles of Computer Science II/Labs/Steven_Acosta_Lab1.py").
// Courses with their own page (1301, 3320, 4320, 4370) are skipped, and the other
// exclusions mirror .gitignore plus anything too heavy to ship (venvs, pickles, zips).
// Glob arguments must be literals, so the exclusion list is repeated in both calls.

/** Text files are loaded lazily, one chunk per file, only when opened. */
const textLoaders = import.meta.glob<string>(
  [
    '/[0-9][0-9][0-9][0-9] - */**/*',
    '!/{1301,3320,4320,4370} - */**',
    '!**/{node_modules,venv,output,__pycache__,.ipynb_checkpoints}/**',
    '!**/*.{png,jpg,jpeg,gif,ico,svg,mp3,db,pdf,zip,pkl,jar}',
    '!**/package-lock.json',
    '!**/dockercompose.yml',
  ],
  { query: '?raw', import: 'default' },
)

/** Binary files resolve to a served asset URL. */
const binaryUrls = import.meta.glob<string>(
  [
    '/[0-9][0-9][0-9][0-9] - */**/*.{png,jpg,jpeg,gif,ico,svg,db}',
    // Only the 2510 PDFs are committed; the rest are private assignment handouts.
    '/2510 - */*.pdf',
    '!/{1301,3320,4320,4370} - */**',
    '!**/{node_modules,venv,output,__pycache__,.ipynb_checkpoints}/**',
  ],
  { query: '?url', import: 'default', eager: true },
)

export interface FileNode {
  kind: 'file'
  name: string
  /** Path relative to the course folder, e.g. "Labs/Lab1.py". */
  path: string
  ext: string
  loadText?: () => Promise<string>
  url?: string
}

export interface FolderNode {
  kind: 'folder'
  name: string
  path: string
  children: TreeNode[]
}

export type TreeNode = FileNode | FolderNode

const byName = (a: TreeNode, b: TreeNode) => {
  if (a.kind !== b.kind) return a.kind === 'folder' ? -1 : 1
  // numeric so "Lab 2" sorts before "Lab 10"
  return a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' })
}

function sortTree(folder: FolderNode) {
  folder.children.sort(byName)
  folder.children.forEach((child) => child.kind === 'folder' && sortTree(child))
}

const treeCache = new Map<string, FolderNode>()

/** Builds (and caches) the folder tree for one course folder name. */
export function getCourseTree(courseFolder: string): FolderNode {
  const cached = treeCache.get(courseFolder)
  if (cached) return cached

  const root: FolderNode = { kind: 'folder', name: courseFolder, path: '', children: [] }
  const prefix = `/${courseFolder}/`

  const addFile = (fullPath: string, file: Omit<FileNode, 'kind' | 'name' | 'path' | 'ext'>) => {
    if (!fullPath.startsWith(prefix)) return
    const segments = fullPath.slice(prefix.length).split('/')
    const fileName = segments.pop()!

    let folder = root
    for (const segment of segments) {
      let next = folder.children.find(
        (child): child is FolderNode => child.kind === 'folder' && child.name === segment,
      )
      if (!next) {
        next = {
          kind: 'folder',
          name: segment,
          path: folder.path ? `${folder.path}/${segment}` : segment,
          children: [],
        }
        folder.children.push(next)
      }
      folder = next
    }

    const dot = fileName.lastIndexOf('.')
    folder.children.push({
      kind: 'file',
      name: fileName,
      path: folder.path ? `${folder.path}/${fileName}` : fileName,
      ext: dot > 0 ? fileName.slice(dot + 1).toLowerCase() : '',
      ...file,
    })
  }

  for (const [fullPath, load] of Object.entries(textLoaders)) addFile(fullPath, { loadText: load })
  for (const [fullPath, url] of Object.entries(binaryUrls)) addFile(fullPath, { url })

  sortTree(root)
  treeCache.set(courseFolder, root)
  return root
}

/** Finds the node at a course-relative path, or null if it doesn't exist. */
export function findNode(root: FolderNode, path: string): TreeNode | null {
  if (!path) return root
  let node: TreeNode = root
  for (const segment of path.split('/')) {
    if (node.kind !== 'folder') return null
    const next: TreeNode | undefined = node.children.find((child) => child.name === segment)
    if (!next) return null
    node = next
  }
  return node
}
