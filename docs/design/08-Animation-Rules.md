# Animation Rules

## Duration

| Token | Value | Use |
|-------|-------|-----|
| fast | 100ms | Button press, toggle |
| normal | 200ms | Panel resize, tab switch |
| slow | 300ms | Modal open/close, notification slide |

## Easing

| Token | Value | Use |
|-------|-------|-----|
| default | ease-out | Most transitions |
| in | ease-in | Exiting elements |
| in-out | ease-in-out | Resizing, layout changes |

## Reduced Motion

All animations respect `prefers-reduced-motion: reduce`. When enabled:
- All durations set to 0ms.
- Chart animations disabled.
- Transitions are instant.

## Animations

### Panel Resize
- Duration: normal.
- Easing: in-out.
- Smooth width/height change.

### Tab Switch
- Duration: fast.
- Easing: default.
- Content fades in (opacity 0 → 1).

### Modal Open
- Duration: slow.
- Easing: default.
- Background fades in (opacity 0 → 1).
- Modal scales in (transform: scale(0.95) → scale(1)).

### Modal Close
- Duration: fast.
- Easing: in.
- Reverse of open.

### Notification Slide
- Duration: slow.
- Easing: default.
- Slides in from right (translateX(100%) → translateX(0)).

### Toast Dismiss
- Duration: fast.
- Easing: in.
- Slides out and fades.

### Chart Animation
- Duration: 300ms.
- Easing: default.
- Line drawing, point fade-in, bar growth.
- Disabled when `prefers-reduced-motion: reduce`.

### Button Press
- Duration: fast.
- Easing: default.
- Scale: 1 → 0.98 → 1.

## Rules

- Never animate for more than 300ms.
- Never animate layout properties (width, height) on frequently-updating elements.
- Prefer opacity and transform for smooth animations.
- Test all animations with reduced motion enabled.
