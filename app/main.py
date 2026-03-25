from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health_check import health_check_router
from app.api.routes.GenerateResume import generate_resume_router
from app.api.routes.chat import chat_agent_router
from app.api.routes.KgPipeLine import router as kg_pipeline_router
from app.api.routes.KgPipelineText import router as kg_pipeline_text_router
from app.api.routes.JobScraping import router as job_scraping_router
from app.api.routes.RagQuery import Rag_agent_router
from app.core.mysql_database.mysql_service import get_mysql_service, close_mysql_service
from app.core.neo4j_database.neo4j_service import get_neo4j_service, close_neo4j_service
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    get_mysql_service()
    print("MySQL connection Initiated")

    get_neo4j_service()
    print("Neo4j connection Initiated")

    yield

    close_mysql_service()
    print("Closing mysql connection")

    close_neo4j_service()
    print("Closing neo4j connection")
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
app.include_router(generate_resume_router)
app.include_router(chat_agent_router)
app.include_router(kg_pipeline_router)
app.include_router(kg_pipeline_text_router)
app.include_router(job_scraping_router)
app.include_router(Rag_agent_router)

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_chat_interface():
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Memory-GPT API is running. Place index.html in static folder."}
