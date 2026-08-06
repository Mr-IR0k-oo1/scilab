from fastapi import APIRouter
from ..learning_content import EXAMPLES, TUTORIALS, REFERENCE

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.get("/examples")
async def get_examples():
    return {"examples": EXAMPLES}

@router.get("/tutorials")
async def get_tutorials():
    return {"tutorials": TUTORIALS}

@router.get("/reference")
async def get_reference():
    return {"reference": REFERENCE}
