# Themes

## Dark Theme (Default)

```
Background:  #1e1e1e (primary), #252526 (secondary), #2d2d3d (tertiary)
Text:        #e0e0e0 (primary), #a0a0a0 (secondary), #666666 (muted)
Accent:      #4a9eff
Border:      #404040
Error:       #f44336
Warning:     #ff9800
Success:     #4caf50
Info:        #2196f3
```

## Light Theme

```
Background:  #ffffff (primary), #f5f5f5 (secondary), #e8e8e8 (tertiary)
Text:        #333333 (primary), #666666 (secondary), #999999 (muted)
Accent:      #2196f3
Border:      #e0e0e0
Error:       #d32f2f
Warning:     #f57c00
Success:     #388e3c
Info:        #1976d2
```

## High Contrast Theme

```
Background:  #000000 (primary), #1a1a1a (secondary)
Text:        #ffffff (primary), #cccccc (secondary)
Accent:      #00ffff
Border:      #ffffff
Error:       #ff0000
Warning:     #ffff00
Success:     #00ff00
Info:        #00ffff
```

## Chart Colors

### Dark
```json
["#4a9eff", "#ff6384", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#e91e63", "#8bc34a"]
```

### Light
```json
["#2196f3", "#e91e63", "#4caf50", "#ff9800", "#9c27b0", "#00bcd4", "#f44336", "#8bc34a"]
```

## Rules

- All colors use CSS custom properties.
- Never hard-code colors in components.
- Charts inherit theme colors automatically.
- System theme follows OS preference.
- High contrast mode meets WCAG AAA.
