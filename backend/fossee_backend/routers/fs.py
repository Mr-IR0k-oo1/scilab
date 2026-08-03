from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

from ..filesystem import fs_manager
from ..models import FileInfo

router = APIRouter(prefix="/api/fs", tags=["fs"])

class WriteFileRequest(BaseModel):
    path: str
    content: str

class RenameRequest(BaseModel):
    old_path: str
    new_path: str

@router.get("/file")
async def read_text_file(path: str = Query(...)):
    try:
        content = fs_manager.read_text_file(path)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/file")
async def write_text_file(req: WriteFileRequest):
    try:
        fs_manager.write_text_file(req.path, req.content)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[FileInfo])
async def list_directory(path: str = Query(...)):
    try:
        return fs_manager.list_directory(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dir")
async def create_directory(path: str = Query(...)):
    try:
        fs_manager.create_directory(path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/file")
async def remove_file(path: str = Query(...)):
    try:
        fs_manager.remove_file(path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/dir")
async def remove_directory(path: str = Query(...)):
    try:
        fs_manager.remove_directory(path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exists")
async def file_exists(path: str = Query(...)):
    exists = fs_manager.file_exists(path)
    return {"exists": exists}

@router.get("/info", response_model=FileInfo)
async def path_info(path: str = Query(...)):
    try:
        return fs_manager.path_info(path)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/rename")
async def rename_path(req: RenameRequest):
    try:
        fs_manager.rename_path(req.old_path, req.new_path)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
