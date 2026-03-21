from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.health_check import health_check_router
from app.api.routes.GenerateResume import generate_resume_router
from app.api.routes.chat import chat_agent_router
from app.core.mysql_database.mysql_service import get_mysql_service, close_mysql_service

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    get_mysql_service()
    print("MySQL connection Initiated")

    yield

    close_mysql_service()
    print("Closing mysql connection")
    
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
