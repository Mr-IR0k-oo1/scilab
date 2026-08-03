from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Any, List, Optional

from .. import widgets as widgets_manager
from ..models import WidgetInstance, WidgetType, WidgetProperties

router = APIRouter(prefix="/api/widgets", tags=["widgets"])

class CreateWidgetRequest(BaseModel):
    type_id: str
    properties: Optional[WidgetProperties] = None

class PropertyRequest(BaseModel):
    name: str
    value: Any

class BindRequest(BaseModel):
    name: str
    expression: str

class UnbindRequest(BaseModel):
    name: str

@router.get("/types/{id}", response_model=WidgetType)
async def get_widget_type(id: str):
    wt = widgets_manager.get_widget_type(id)
    if not wt:
        raise HTTPException(status_code=404, detail="Widget type not found")
    return wt

@router.get("/types", response_model=List[WidgetType])
async def get_all_widget_types():
    return widgets_manager.get_all_widget_types()

@router.get("/types/category/{category}", response_model=List[WidgetType])
async def get_widget_types_by_category(category: str):
    return widgets_manager.get_widget_types_by_category(category)

@router.post("", response_model=WidgetInstance)
async def create_widget(req: CreateWidgetRequest):
    try:
        return widgets_manager.create_widget(req.type_id, req.properties)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", response_model=WidgetInstance)
async def get_widget(id: str):
    w = widgets_manager.get_widget(id)
    if not w:
        raise HTTPException(status_code=404, detail="Widget not found")
    return w

@router.delete("/{id}")
async def destroy_widget(id: str):
    success = widgets_manager.destroy_widget(id)
    if not success:
        raise HTTPException(status_code=404, detail="Widget not found")
    return {"success": True}

@router.patch("/{id}/property")
async def set_property(id: str, req: PropertyRequest):
    success = widgets_manager.set_property(id, req.name, req.value)
    if not success:
        raise HTTPException(status_code=404, detail="Widget or property not found")
    return {"success": True}

@router.post("/{id}/bind")
async def bind_property(id: str, req: BindRequest):
    # Mock binding
    success = widgets_manager.set_property(id, req.name, req.expression)
    if not success:
        raise HTTPException(status_code=404, detail="Widget or property not found")
    return {"success": True}

@router.post("/{id}/unbind")
async def unbind_property(id: str, req: UnbindRequest):
    success = widgets_manager.set_property(id, req.name, None)
    if not success:
        raise HTTPException(status_code=404, detail="Widget or property not found")
    return {"success": True}

@router.get("/{id}/serialize")
async def serialize_widget(id: str):
    data = widgets_manager.serialize_widget(id)
    if not data:
        raise HTTPException(status_code=404, detail="Widget not found")
    return {"json": data}

@router.post("/deserialize")
async def deserialize_widget(json_data: dict):
    try:
        w = widgets_manager.deserialize_widget(json_data)
        return {"widget": w}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
