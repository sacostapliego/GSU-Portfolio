# Spinfinity Slots — Pure CSS Motion UI

An interactive, motion-first slot machine built using only HTML and CSS (no JavaScript). Demonstrates transforms, transitions, and keyframe animations with responsive layout, theme toggle, and accessibility considerations.

## Core Features
- Reel Spin: `@keyframes` vertically scrolls symbols in an infinite loop.
- Staggered Stop: `animation-delay` creates sequential stopping.
- Win-Line Highlight: flashing border using `animation: alternate`.
- Theme Toggle: Light/Dark via CSS variables and `prefers-color-scheme` with a pure CSS checkbox.

### UI Additions
- Message Bar (CSS-only): Shows  Spinning → Lose → Lose → Win based on two fail html pages and one win html page.
- Click Stop to view results. Click Spin Again to try again.

## Stretch Goals
- 3D Reel Illusion with `transform: rotateX()` and `perspective`.
- Blur During Spin using `filter: blur()`.
- Confetti Animation using `@keyframes` and layered gradients.

### Visual polish
- Payline band sheen across the center row to anchor the win-line.
- Reel sheen animation while spinning; softened when stopped.
- Slightly varied per-reel spin speeds for more organic motion.
- Smoother stop curve with a micro-bounce into place.
- Deeper win glow and inset highlight for premium feel.

## How it works (CSS-only interactions)
- A hidden checkbox `#spinToggle` toggles the spinning/stop states via sibling selectors.
- Another checkbox `#themeSwitch` toggles CSS variables scoped to the `.page` wrapper.
- No inline styles or JS; everything is expressed in the stylesheet.
- Message Bar text visibility changes via CSS sibling selectors; there is no DOM manipulation.
- Confetti and win-line trigger only when stopped and `#winToggle` is checked (demo).

## Accessibility
- Semantic landmarks: header, main, aside, footer.
- Skip link for keyboard users.
- Reduced motion respect via `prefers-reduced-motion`.
- Labels used for both toggles so they are keyboard-activatable.

## Responsive design
- CSS Grid and Flexbox adapt layout; reels scale fluidly.
- Uses clamps and columns for readable content.

### Customize quickly
- Colors: edit `--accent`, `--accent-2`, `--bg`, `--surface`, `--text` in `assets/css/styles.css`.
- Motion: `--reel-speed`, `--reel-delay`, `--win-pulse`, `--easing-snap`.
- Symbol row height: `--symbol-row-h` for alignment with the center payline.

## Motion storyboard (concept)
1. Idle: Reels are still; subtle background gradient and depth.
2. Spin: Press "Spin / Stop"; reels blur slightly and rotateX adds cylindrical feel.
3. Stop: Reels decelerate in sequence (left to right). Win-line flashes to draw attention.
4. Celebrate: Confetti falls briefly at stop.

## Run locally by clicking on index.html or upload it ro Codd and view
 - Additional link: https://saquib-ahmed-saad.github.io/Spinfinity-Slots/index.html

## Notes
- Feature selectors use `:has()` where available, but fallbacks are provided.
- If your linter reports unknown properties, ensure a modern CSS syntax plugin is enabled.
- Tested in latest Chrome and Firefox; `:has()` enhancements gracefully degrade.

## Validation
- HTML: Passes basic checks (W3C HTML validator).
- CSS: No errors in modern syntax; vendor-specific differences are minimal.

## Reflection
- Motion is purposeful: blur and tilt communicate speed; staggered stop communicates sequence and anticipation.
- Color and light/dark themes support context and comfort.
- Everything is achievable with pure CSS, showcasing state-driven UI via simple HTML controls.
>>>>>>> 316136c (feat: initial Spinfinity Slots HTML+CSS with separated animation.css; theme toggle, reels, overlays, confetti, and centered message bar)




