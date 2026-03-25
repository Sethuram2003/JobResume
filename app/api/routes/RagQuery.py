from fastapi.responses import JSONResponse
from fastapi import FastAPI, Form, APIRouter
from dotenv import load_dotenv
import os

from app.core.neo4j_database.neo4j_service import get_neo4j_service

load_dotenv()

Rag_agent_router = APIRouter(tags=["ChatAgent"])
app = FastAPI()

@Rag_agent_router.post("/RagChat")
async def ragchat(
    query: str = Form(...)
):
    """
    Process a user query using the RAG agent.
    """
    manager = get_neo4j_service()
    response = manager.run_rag_query(
        db_name=os.getenv("NEO4J_DATABASE"),
        query=query
    )

    return JSONResponse(content=response, status_code=200)
