# Architecture Audit — Scilab Studio (Phase 1)

**Date:** 2026-08-10  
**Project:** Scilab Studio / FOSSEE Open-Source Ecosystem  
**Scope:** Frontend inspection, backend infrastructure evaluation, and integration plan  

---

## 1. Executive Summary

This architecture audit details the existing repository state for **Scilab Studio**. The codebase contains a modern React + TypeScript frontend (`apps/desktop`), monorepo TypeScript packages (`packages/`), and a baseline Python backend structure (`backend/`). 

Phase 1 establishes a production-quality, clean FastAPI + SQLAlchemy 2 + Pydantic v2 backend skeleton communicating with the existing React application without breaking frontend functionality or introducing non-supported framework runtime overhead.

---

## 2. Existing Repository Audit Findings

### 2.1 Existing React Structure
- **Location:** `apps/desktop`
- **Framework:** React 18, Next.js (App Router), TypeScript.
- **Entry Points:** `apps/desktop/src/app/layout.tsx`, `apps/desktop/src/app/page.tsx`, `apps/desktop/src/shell/Shell.tsx`.
- **Layout & Views:** Modular container layout (`apps/desktop/src/platform/Platform.tsx`, `Layout.tsx`, `WorkspaceView.tsx`).

### 2.2 Package Manager & Workspace Configuration
- **Package Manager:** `npm` (v10+), supported via Turbo monorepo (`turbo.json`, root `package.json`).
- **Workspaces:** `"apps/*"`, `"packages/*"`.

### 2.3 Existing Routing
- Next.js App Router (`apps/desktop/src/app/page.tsx`).
- In-memory view switching between Workbench modules via `store.ts` (`currentView`, `activeTab`).

### 2.4 Existing State Management
- Pub/Sub reactive store implementation in `apps/desktop/src/store/store.ts`.
- Exports state mutators (`setStore`), session persistence (`localStorage`), and subscriber notifications (`subscribe`).

### 2.5 Existing API Utilities
- **Transport Abstraction:** `apps/desktop/src/lib/api.ts` (`ApiTransport` interface and `FetchTransport` implementation).
- **Domain API Wrappers:** `apps/desktop/src/lib/fs.ts` (file system & project operations), `apps/desktop/src/lib/scilab.ts` (Scilab status and execution).
- Default base URL defaults to environment variable `NEXT_PUBLIC_API_URL` or fallback `http://127.0.0.1:8000/api/v1`.

### 2.6 Existing Environment Configuration
- Environment variables configured via `.env` / `.env.example`.
- Frontend reads `process.env.NEXT_PUBLIC_API_URL`.

### 2.7 Existing UI / Component System
- **Styling:** Vanilla CSS design system with CSS custom properties in `tokens.css` and `styles.css`.
- **Icons:** `lucide-react`.
- **Reusable UI Components:** ActivityRail, Menubar, Sidebar, BottomPanel, RightSidebar, ScriptEditor, CommandPalette, Tabs, Statusbar.

### 2.8 Existing Tests & Build Commands
- **Frontend / Monorepo:** `npm run dev`, `npm run build`, `npm run typecheck`, `npm run lint`, `npm run format`.
- **Tests:** `npm run test` (Turbo execution across packages).

---

## 3. Backend Integration Points & Plan

### 3.1 Recommended Backend Architecture
- **Framework:** Python 3.12+, FastAPI, Uvicorn.
- **ORM & DB:** SQLAlchemy 2.0 (async/sync engine), Alembic migrations, SQLite database (`scilab_studio.db`).
- **Data Validation:** Pydantic v2 schemas (`BaseModel`).
- **Architecture Pattern:** Strict layered architecture: `Route` → `Service` → `Repository` → `Database Model`.

### 3.2 Key Backend Endpoints (v1)
1. `GET /api/v1/health`
2. `GET /api/v1/system/info`
3. `GET /api/v1/workspaces`
4. `POST /api/v1/workspaces`
5. `GET /api/v1/projects`
6. `POST /api/v1/projects`
7. `GET /api/v1/projects/{project_id}`
8. `DELETE /api/v1/projects/{project_id}`

### 3.3 Development Environment (Zed IDE)
- Task configuration defined in `.zed/tasks.json` to manage FastAPI server start (`backend:dev`), pytest execution (`backend:test`), ruff linting (`backend:lint`), next.js dev (`frontend:dev`), and full stack launching (`dev`).

---

## 4. Phase 1 Scope Safeguards

- **NO** Rust runtime dependencies introduced.
- **NO** Replacement of existing React frontend.
- **NO** AI, complex plugin marketplaces, or heavy visualization engine additions during Phase 1 infrastructure setup.
- Preserve 100% compatibility with existing React components while pointing API calls to `http://localhost:8000/api/v1`.
