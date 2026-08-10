from fastapi import APIRouter
from app.core.config import settings
from app.schemas.system import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        version="0.1.0",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
    )
