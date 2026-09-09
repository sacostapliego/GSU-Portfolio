import { useCallback, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'

interface DragResizeOptions {
  axis: 'x' | 'y'
  /** Current size in pixels. */
  value: number
  onChange: (next: number) => void
  min: number
  /** Evaluated on every move so the ceiling tracks the container's real size. */
  max: () => number
  /** Set when dragging toward the axis origin should grow the panel. */
  invert?: boolean
  /** Size restored on double-click. */
  defaultValue?: number
}

/**
 * Pointer-driven resizing for a split pane. Uses pointer capture so the drag
 * keeps tracking even when the cursor outruns the 4px handle.
 */
export function useDragResize({
  axis,
  value,
  onChange,
  min,
  max,
  invert = false,
  defaultValue,
}: DragResizeOptions) {
  const [isDragging, setIsDragging] = useState(false)
  const origin = useRef({ pointer: 0, size: 0 })

  const clamp = useCallback(
    (next: number) => Math.min(Math.max(next, min), Math.max(min, max())),
    [min, max],
  )

  const onPointerDown = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      event.preventDefault()
      event.currentTarget.setPointerCapture(event.pointerId)
      origin.current = {
        pointer: axis === 'x' ? event.clientX : event.clientY,
        size: value,
      }
      setIsDragging(true)
    },
    [axis, value],
  )

  const onPointerMove = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      if (!isDragging) return
      const pointer = axis === 'x' ? event.clientX : event.clientY
      const delta = (pointer - origin.current.pointer) * (invert ? -1 : 1)
      onChange(clamp(origin.current.size + delta))
    },
    [axis, clamp, invert, isDragging, onChange],
  )

  const endDrag = useCallback((event: ReactPointerEvent<HTMLDivElement>) => {
    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
      event.currentTarget.releasePointerCapture(event.pointerId)
    }
    setIsDragging(false)
  }, [])

  const onDoubleClick = useCallback(() => {
    if (defaultValue !== undefined) onChange(clamp(defaultValue))
  }, [clamp, defaultValue, onChange])

  return {
    isDragging,
    handleProps: {
      onPointerDown,
      onPointerMove,
      onPointerUp: endDrag,
      onPointerCancel: endDrag,
      onDoubleClick,
      style: {
        cursor: axis === 'x' ? 'col-resize' : 'row-resize',
        touchAction: 'none' as const,
      },
    },
  }
}
