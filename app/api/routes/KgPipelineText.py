from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from app.core.neo4j_database.neo4j_service import get_neo4j_service

router = APIRouter(prefix="/kg", tags=["knowledge-graph"])

@router.put("/buildFromText")
async def build_knowledge_graph(text: str = File(...)):
    """
    Build knowledge graph from uploaded text
    """
    neo4j_service = get_neo4j_service()

    await neo4j_service.pipe_line_text(
        db_name=os.getenv("NEO4J_DATABASE"),
        text=text
        )

    return JSONResponse(
        status_code=200,
        content={"message": "Knowledge graph built successfully"}
    )
            
