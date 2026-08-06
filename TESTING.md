# Scilab Studio Testing Guide

This document outlines the testing strategy, commands, and procedures for verifying all 4 layers of Scilab Studio.

## Test Suites Overview

| Layer | Test Location | Framework / Command | Coverage |
|-------|---------------|---------------------|----------|
| **Backend** | `backend/tests/` | `PYTHONPATH=backend backend/venv/bin/python -m unittest discover -s backend/tests` | FastAPI Routers, Data Importer, Report Generator, Learning Content |
| **PySide6 App** | `scilab-studio/tests/` | `PYTHONPATH=scilab-studio python3 -m unittest discover -s scilab-studio/tests` | Core Runtime, EventBus, Lifecycle, ServiceRegistry, Workspace, UI Console |
| **Desktop App Store & Widgets** | `apps/desktop/src/store/` & `packages/widgets/` | `bun test apps/desktop/src/store/store.test.ts packages/widgets/src/index.test.ts` | State Management, Tabs, Widget Definitions |
| **Desktop App Frontend** | `apps/desktop/` | `bun run --cwd apps/desktop typecheck` | Next.js / TypeScript static verification |
| **Website** | `frontend/` | `bun run --cwd frontend build` | Website build and asset bundling |

---

## Running Tests

### 1. Backend Unit Tests
```bash
PYTHONPATH=backend backend/venv/bin/python -m unittest discover -s backend/tests
```

### 2. PySide6 Desktop App Tests
```bash
PYTHONPATH=scilab-studio python3 -m unittest discover -s scilab-studio/tests
```

### 3. Frontend & Widget Bun Unit Tests
```bash
bun test packages/widgets/src/index.test.ts apps/desktop/src/store/store.test.ts
```

### 4. Type Checking & Production Build Verification
```bash
# Desktop app TypeScript check
bun run --cwd apps/desktop typecheck

# Website build verification
bun run --cwd frontend build
```

---

## Complete Test Execution Script

Run all test suites end-to-end with:

```bash
#!/usr/bin/env bash
set -e

echo "=== 1. Backend Unit Tests ==="
PYTHONPATH=backend backend/venv/bin/python -m unittest discover -s backend/tests

echo "=== 2. PySide6 Desktop App Tests ==="
PYTHONPATH=scilab-studio python3 -m unittest discover -s scilab-studio/tests

echo "=== 3. Bun Unit Tests ==="
bun test packages/widgets/src/index.test.ts apps/desktop/src/store/store.test.ts

echo "=== 4. TypeScript & Build Checks ==="
bun run --cwd apps/desktop typecheck
bun run --cwd frontend build

echo "✅ All tests passed successfully!"
```
