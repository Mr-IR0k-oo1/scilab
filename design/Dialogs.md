# Dialogs

## Modal Dialog

```
┌─────────────────────────────────────┐
│ Dialog Title                   [×]  │
├─────────────────────────────────────┤
│                                     │
│  Dialog content goes here.          │
│  Can include text, forms, lists.    │
│                                     │
├─────────────────────────────────────┤
│           [Cancel]  [Confirm]       │
└─────────────────────────────────────┘
```

### Behavior
- Centers on screen.
- Backdrop: semi-transparent black (0.5 opacity).
- Focus trapped inside dialog.
- Escape closes dialog.
- Click outside closes dialog (if not required).
- Enter confirms (if confirm button is focused).

### Dialog Sizes
| Size | Width | Use |
|------|-------|-----|
| `sm` | 320px | Simple confirmations |
| `md` | 480px | Forms, settings |
| `lg` | 640px | Complex content |
| `xl` | 800px | Preview, large forms |

## Confirmation Dialog

```
┌─────────────────────────────────────┐
│ [!] Delete File                     │
├─────────────────────────────────────┤
│                                     │
│  Are you sure you want to delete    │
│  "main.sce"? This cannot be undone. │
│                                     │
├─────────────────────────────────────┤
│        [Cancel]  [Delete]           │
└─────────────────────────────────────┘
```

- Destructive action button is red (`--ss-error`).
- Clear, specific message.
- No ambiguous language.

## Input Dialog

```
┌─────────────────────────────────────┐
│ New File Name                       │
├─────────────────────────────────────┤
│                                     │
│  Enter the file name:               │
│  ┌─────────────────────────────┐    │
│  │ untitled.sce                │    │
│  └─────────────────────────────┘    │
│                                     │
├─────────────────────────────────────┤
│           [Cancel]  [Create]        │
└─────────────────────────────────────┘
```

- Auto-focus the input field.
- Pre-fill with default value.
- Validate on submit.

## Toast Notifications

```
┌─────────────────────────────────────┐
│ [✓] File saved successfully    [×]  │
└─────────────────────────────────────┘
```

### Behavior
- Position: bottom-right corner.
- Auto-dismiss: 5s (info), 10s (error).
- Stack vertically (max 5 visible).
- Slide in from right.
- Click to dismiss.
- Action button optional.

### Toast Types
| Type | Icon | Color |
|------|------|-------|
| Info | `info` | `--ss-info` |
| Success | `check-circle` | `--ss-success` |
| Warning | `alert-triangle` | `--ss-warning` |
| Error | `x-circle` | `--ss-error` |

## Rules

- One modal dialog at a time.
- Dialogs have clear, specific titles.
- Destructive actions require confirmation.
- Keyboard: Escape to cancel, Enter to confirm.
- Focus is trapped inside modal dialogs.
- Backdrop click closes non-required dialogs.
