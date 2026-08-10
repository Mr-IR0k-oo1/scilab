import sys
import platform
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.system import SystemInfoResponse

router = APIRouter()


@router.get("/system/info", response_model=SystemInfoResponse)
def get_system_info():
    return SystemInfoResponse(
        app_name=settings.APP_NAME,
        version="0.1.0",
        python_version=sys.version,
        platform=f"{platform.system()} {platform.release()}",
        database_status="connected",
    )
