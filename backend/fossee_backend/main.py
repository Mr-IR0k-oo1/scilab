from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import FOSSEE_BACKEND_PORT, EXTRA_CORS_ORIGINS
from .routers import scilab, fs, projects, charts, widgets

app = FastAPI(title="FOSSEE Backend")

# Default allowed origins + anything in FOSSEE_CORS_ORIGINS
allowed_origins = [
    "http://localhost:1420",
    "http://127.0.0.1:1420",
    "tauri://localhost"
] + EXTRA_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scilab.router)
app.include_router(fs.router)
app.include_router(projects.router)
app.include_router(charts.router)
app.include_router(widgets.router)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
