from langchain.tools import tool
from app.core.LatexModule.LatexTemplate import generate_latex
from app.core.model import ResumeData
from app.core.LatexModule.LatexFunction import render
from app.core.neo4j_database.neo4j_service import get_neo4j_service
import os
import uuid

from dotenv import load_dotenv
load_dotenv()
    
@tool
def context_for_resume(query: str) -> str:
    """
    Query the candidate's resume knowledge base to retrieve specific information.

    IMPORTANT: After receiving a result from this tool, you must continue calling
    this tool for all remaining required data. Do NOT emit any text or JSON until
    ALL of the following have been collected:
        1. Personal details (name, phone, email, LinkedIn, GitHub)
        2. Education (university, degree, GPA, dates, courses)
        3. Work experience (all roles: title, company, location, dates, highlights)
        4. Technical skills (languages, frameworks, tools)
        5. At least 2-3 projects relevant to the job description

    Only after all 5 categories are collected should you stop calling this tool
    and emit the final JSON output.

    Each call must ask about ONE specific topic using a focused natural language query.

    Good query examples:
    - "full name, phone number, email, LinkedIn URL, GitHub URL"
    - "university, degree, GPA, graduation date, relevant coursework"
    - "all work experiences: job title, company, location, dates, bullet highlights"
    - "all technical skills: programming languages, frameworks, libraries, tools"
    - "projects involving machine learning, NLP, or deep learning"
    - "projects involving distributed systems or cloud infrastructure"
    - "experience with Docker, Kubernetes, or CI/CD pipelines"

    Args:
        query: A focused natural language question about one aspect of the candidate's resume.

    Returns:
        A string containing the resume content matching the query.
    """
    pipeline = get_neo4j_service()
    response = pipeline.run_rag_query(
        db_name=os.getenv("NEO4J_DATABASE"),
        query=query
    )
    return response
