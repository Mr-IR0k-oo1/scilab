from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from ..report_generator import report_generator

router = APIRouter(prefix="/api/reports", tags=["reports"])

class GenerateReportRequest(BaseModel):
    title: str
    blocks: List[Dict[str, Any]]
    format: Optional[str] = "html"

@router.post("/generate")
async def generate_report(req: GenerateReportRequest):
    try:
        html_content = report_generator.generate_html(req.title, req.blocks)
        return {
            "title": req.title,
            "format": req.format,
            "html": html_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {e}")

@router.get("/templates")
async def list_report_templates():
    return {
        "templates": [
            {
                "id": "lab-report",
                "name": "Standard Lab Report",
                "blocks": [
                    {"type": "heading", "content": "1. Objective"},
                    {"type": "paragraph", "content": "Describe experiment objective here..."},
                    {"type": "heading", "content": "2. Simulation Code"},
                    {"type": "code", "content": "// Scilab simulation script\nplot(0:0.1:10, sin(0:0.1:10));"},
                    {"type": "heading", "content": "3. Results & Discussion"}
                ]
            },
            {
                "id": "tech-brief",
                "name": "Technical Analysis Brief",
                "blocks": [
                    {"type": "heading", "content": "Executive Summary"},
                    {"type": "paragraph", "content": "Overview of engineering findings..."},
                    {"type": "heading", "content": "Data Summary"}
                ]
            }
        ]
    }
