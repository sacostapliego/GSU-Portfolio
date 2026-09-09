import { useCallback, useEffect, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'

export interface WindowRect {
  x: number
  y: number
  width: number
  height: number
}

/** Compass directions, matching the eight resize handles of a desktop window. */
export type ResizeEdge = 'n' | 's' | 'e' | 'w' | 'ne' | 'nw' | 'se' | 'sw'

const CURSORS: Record<ResizeEdge, string> = {
  n: 'ns-resize',
  s: 'ns-resize',
  e: 'ew-resize',
  w: 'ew-resize',
  ne: 'nesw-resize',
  sw: 'nesw-resize',
  nw: 'nwse-resize',
  se: 'nwse-resize',
}

interface WindowFrameOptions {
  rect: WindowRect
  onChange: (rect: WindowRect) => void
  minWidth?: number
  minHeight?: number
  /** Space reserved at the bottom for the dock. */
  bottomInset?: number
  /** Set while maximized, so the window can't be dragged or resized. */
  disabled?: boolean
}

/** Keeps enough of the title bar on screen that the window is always grabbable. */
const KEEP_VISIBLE = 140

function clampPosition(rect: WindowRect): WindowRect {
  const maxX = window.innerWidth - KEEP_VISIBLE
  const minX = KEEP_VISIBLE - rect.width
  const maxY = window.innerHeight - 44

  return {
    ...rect,
    x: Math.min(Math.max(rect.x, minX), maxX),
    y: Math.min(Math.max(rect.y, 0), maxY),
  }
}

/**
 * Desktop-window behaviour for an absolutely positioned element: drag to move,
 * eight-way resize, and re-clamping when the viewport changes.
 */
export function useWindowFrame({
  rect,
  onChange,
  minWidth = 460,
  minHeight = 320,
  bottomInset = 0,
  disabled = false,
}: WindowFrameOptions) {
  const [isMoving, setIsMoving] = useState(false)
  const [isResizing, setIsResizing] = useState(false)
  const origin = useRef({ pointerX: 0, pointerY: 0, rect })

  const begin = useCallback(
    (event: ReactPointerEvent<HTMLElement>) => {
      event.currentTarget.setPointerCapture(event.pointerId)
      origin.current = { pointerX: event.clientX, pointerY: event.clientY, rect }
    },
    [rect],
  )

  const end = useCallback((event: ReactPointerEvent<HTMLElement>) => {
    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId)
    }
    setIsMoving(false)
    setIsResizing(false)
  }, [])

  const onMovePointerDown = useCallback(
    (event: ReactPointerEvent<HTMLElement>) => {
      if (disabled) return
      // Let the traffic lights handle their own clicks.
      if ((event.target as HTMLElement).closest('button')) return

      event.preventDefault()
      begin(event)
      setIsMoving(true)
    },
    [begin, disabled],
  )

  const onMovePointerMove = useCallback(
    (event: ReactPointerEvent<HTMLElement>) => {
      if (!isMoving) return
      const start = origin.current
      onChange(
        clampPosition({
          ...start.rect,
          x: start.rect.x + (event.clientX - start.pointerX),
          y: start.rect.y + (event.clientY - start.pointerY),
        }),
      )
    },
    [isMoving, onChange],
  )

  const getResizeHandleProps = useCallback(
    (edge: ResizeEdge) => ({
      onPointerDown: (event: ReactPointerEvent<HTMLElement>) => {
        if (disabled) return
        event.preventDefault()
        event.stopPropagation()
        begin(event)
        setIsResizing(true)
      },
      onPointerMove: (event: ReactPointerEvent<HTMLElement>) => {
        if (!isResizing) return

        const start = origin.current
        const deltaX = event.clientX - start.pointerX
        const deltaY = event.clientY - start.pointerY
        let { x, y, width, height } = start.rect

        if (edge.includes('e')) {
          width = Math.max(minWidth, start.rect.width + deltaX)
        }
        if (edge.includes('w')) {
          // Dragging the left edge moves the origin as the width changes.
          width = Math.max(minWidth, start.rect.width - deltaX)
          x = start.rect.x + (start.rect.width - width)
        }
        if (edge.includes('s')) {
          const maxHeight = window.innerHeight - bottomInset - start.rect.y
          height = Math.min(Math.max(minHeight, start.rect.height + deltaY), Math.max(minHeight, maxHeight))
        }
        if (edge.includes('n')) {
          height = Math.max(minHeight, start.rect.height - deltaY)
          y = Math.max(0, start.rect.y + (start.rect.height - height))
          // Clamping y at the top must not let the window keep growing.
          height = start.rect.y + start.rect.height - y
        }

        onChange({ x, y, width, height })
      },
      onPointerUp: end,
      onPointerCancel: end,
      style: { cursor: CURSORS[edge], touchAction: 'none' as const },
    }),
    [begin, bottomInset, disabled, end, isResizing, minHeight, minWidth, onChange],
  )

  // A shrinking viewport must not strand the window off screen.
  useEffect(() => {
    const handleResize = () => onChange(clampPosition(rect))
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [onChange, rect])

  return {
    isMoving,
    isResizing,
    getResizeHandleProps,
    moveHandleProps: {
      onPointerDown: onMovePointerDown,
      onPointerMove: onMovePointerMove,
      onPointerUp: end,
      onPointerCancel: end,
      style: { cursor: isMoving ? 'grabbing' : 'default', touchAction: 'none' as const },
    },
  }
}

/** Centred starting geometry, sized like the old responsive window. */
export function createInitialRect(bottomInset: number): WindowRect {
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight

  const width = Math.min(Math.max(viewportWidth * (viewportWidth < 768 ? 0.95 : 0.72), 460), viewportWidth - 32)
  const height = Math.min(viewportHeight * 0.8, viewportHeight - bottomInset - 32)

  return {
    x: Math.max(16, (viewportWidth - width) / 2),
    y: Math.max(16, (viewportHeight - bottomInset - height) / 2),
    width,
    height,
  }
}
