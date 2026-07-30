# Success Criteria

Measurable, testable criteria for each capability.

## Core Platform

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| Cold start | Time to ready | < 2 seconds | Manual timing |
| Warm start | Time to ready | < 500ms | Manual timing |
| Project open | Time to loaded | < 1 second | Automated test |
| Project save | Time to saved | < 500ms | Automated test |
| Auto-save | Time to saved | < 1 second | Automated test |

## GUI Builder

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| GUI creation | Time to build | < 15 minutes | User testing |
| Component drag | Responsiveness | < 16ms | Automated test |
| Property update | Responsiveness | < 5ms | Automated test |
| Code generation | Time to generate | < 100ms | Automated test |
| Preview mode | Time to preview | < 500ms | Automated test |

## Visualization

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| Chart render (1k) | Time to render | < 16ms | Automated test |
| Chart render (10k) | Time to render | < 100ms | Automated test |
| Chart render (100k) | Time to render | < 500ms | Automated test |
| Chart export (PNG) | Time to export | < 1 second | Automated test |
| Chart export (PDF) | Time to export | < 3 seconds | Automated test |

## Data Studio

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| CSV import (10 MB) | Time to import | < 2 seconds | Automated test |
| CSV import (100 MB) | Time to import | < 10 seconds | Automated test |
| Excel import (10 MB) | Time to import | < 3 seconds | Automated test |
| Data preview | Time to display | < 500ms | Automated test |
| Column stats | Time to compute | < 1 second | Automated test |

## Report Generator

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| Report creation | Time to create | < 5 minutes | User testing |
| PDF export (10 pages) | Time to export | < 5 seconds | Automated test |
| HTML export | Time to export | < 2 seconds | Automated test |
| Chart embedding | Quality | Pixel-perfect | Visual test |

## Plugin System

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| Plugin load | Time to load | < 500ms | Automated test |
| Plugin activation | Time to activate | < 100ms | Automated test |
| Plugin isolation | Error containment | 100% | Failure test |
| New widget (no core changes) | Feasibility | Yes | SDK test |

## Scilab Integration

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| Scilab startup | Time to ready | < 3 seconds | Automated test |
| Command execution | Latency | < 100ms | Automated test |
| Crash recovery | Time to recover | < 2 seconds | Failure test |
| Multi-version support | Compatibility | 7.0+ | Test matrix |

## Accessibility

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| WCAG 2.1 AA | Compliance | 100% | Automated + manual |
| Keyboard navigation | Coverage | 100% | Manual test |
| Screen reader | Compatibility | NVDA, VoiceOver | Manual test |
| Contrast ratio | Minimum | 4.5:1 | Automated test |

## User Experience

| Criterion | Metric | Target | Test Method |
|-----------|--------|--------|-------------|
| First-use clarity | Time to first success | < 5 minutes | User testing |
| Learning curve | Time to proficiency | < 1 hour | User testing |
| Error recovery | User understanding | Clear messages | User testing |
| Documentation coverage | API coverage | 100% | Audit |
