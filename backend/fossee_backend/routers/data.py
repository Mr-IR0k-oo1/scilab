from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..data_importer import data_importer

router = APIRouter(prefix="/api/data", tags=["data"])

class ParseDataRequest(BaseModel):
    content: str
    format: Optional[str] = "csv"  # "csv", "json", "tsv"
    filename: Optional[str] = None

@router.post("/parse")
async def parse_data(req: ParseDataRequest):
    try:
        is_json = req.format == "json" or (req.filename and req.filename.endswith(".json"))
        
        if is_json:
            columns, rows = data_importer.parse_json(req.content)
        else:
            columns, rows = data_importer.parse_csv(req.content)
            
        return {
            "name": req.filename or "Imported Data",
            "columns": columns,
            "rows": rows,
            "total_rows": len(rows)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse data: {e}")

@router.get("/types")
async def get_supported_import_types():
    return {
        "formats": [
            {"ext": "csv", "name": "Comma Separated Values"},
            {"ext": "json", "name": "JSON Array / Objects"},
            {"ext": "tsv", "name": "Tab Separated Values"}
        ]
    }
