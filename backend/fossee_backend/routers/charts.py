from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

from .. import charts as charts_manager
from ..models import Chart, DataDescriptor, ChartOptions

router = APIRouter(prefix="/api/charts", tags=["charts"])

class CreateChartRequest(BaseModel):
    type: str
    data: DataDescriptor
    options: ChartOptions

@router.post("", response_model=Chart)
async def create_chart(req: CreateChartRequest):
    return charts_manager.create_chart(req.type, req.data, req.options)

@router.get("/{id}", response_model=Chart)
async def get_chart(id: str):
    chart = charts_manager.get_chart(id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    return chart

@router.patch("/{id}")
async def update_chart(id: str, options: ChartOptions):
    success = charts_manager.update_chart(id, options)
    if not success:
        raise HTTPException(status_code=404, detail="Chart not found")
    return {"success": True}

@router.put("/{id}/data")
async def update_chart_data(id: str, data: DataDescriptor):
    success = charts_manager.update_chart_data(id, data)
    if not success:
        raise HTTPException(status_code=404, detail="Chart not found")
    return {"success": True}

@router.delete("/{id}")
async def destroy_chart(id: str):
    success = charts_manager.destroy_chart(id)
    if not success:
        raise HTTPException(status_code=404, detail="Chart not found")
    return {"success": True}

@router.get("/{id}/export")
async def export_chart(id: str, format: str = Query("png")):
    chart = charts_manager.get_chart(id)
    if not chart:
        raise HTTPException(status_code=404, detail="Chart not found")
    
    mime_type = {
        "png": "image/png",
        "svg": "image/svg+xml",
        "pdf": "application/pdf"
    }.get(format, "application/octet-stream")
    
    placeholder_data = list(f"Placeholder chart data for chart {id}".encode('utf-8'))
    return {"data": placeholder_data, "mime_type": mime_type}

@router.get("/types")
async def get_supported_types():
    return {"types": charts_manager.get_supported_types()}
