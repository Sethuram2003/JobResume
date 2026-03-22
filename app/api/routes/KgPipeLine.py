from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from app.core.neo4j_database.neo4j_service import get_neo4j_service

router = APIRouter(prefix="/kg", tags=["knowledge-graph"])

@router.post("/build")
async def build_knowledge_graph(file: UploadFile = File(...)):
    """
    Build knowledge graph from uploaded PDF file
    """
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        

        from uuid import uuid4

        resumes_dir = os.path.join(os.getcwd(), "resumes")
        os.makedirs(resumes_dir, exist_ok=True)

        filename = f"resume_{uuid4().hex}.pdf"
        saved_path = os.path.join(resumes_dir, filename)

        content = await file.read()
        with open(saved_path, "wb") as out:
            out.write(content)

        neo4j_service = get_neo4j_service()

        await neo4j_service.pipe_line_pdf(
            db_name=os.getenv("NEO4J_DATABASE"),
            pdf_path=os.path.abspath(saved_path)
        )

        return JSONResponse(
            status_code=200,
            content={"message": "Knowledge graph built successfully", "pdf_path": saved_path}
        )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))