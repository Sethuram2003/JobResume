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
    this tool until ALL of the following categories have been collected. Do NOT
    emit any text or output until every category below has been retrieved:

        1. Personal details — full name, phone number, email, LinkedIn URL, GitHub URL,
                              city, state, country.
        2. Education — ALL degrees (bachelor's, master's, etc.) with university,
                       degree name, major, GPA, graduation date, relevant coursework.
                       **Use a query like: "What are all the candidate's education details?"
                       to retrieve multiple degrees. Do not stop after one result.**
        3. Work experience — all roles with job title, company, location, dates,
                             and bullet highlights.
        4. Technical skills — programming languages, frameworks, libraries, and tools.
        5. Projects — all projects, including name, description, technologies used,
                      and outcomes.

    Each call must target ONE specific category using a focused natural language query.
    Examples of effective queries:

        - "What are the candidate's personal details?"
        - "Show all education details, including bachelor's and master's degrees."
        - "List all work experience with bullet points."
        - "What technical skills does the candidate have?"
        - "Give me all projects with descriptions and technologies."

    Only after all 5 categories are fully collected should you stop calling this tool
    and produce the final resume output.

    Args:
        query: A focused natural language question about one specific category
               from the candidate's resume.

    Returns:
        A string containing the resume content matching the query.
    """
    pipeline = get_neo4j_service()
    response = pipeline.run_rag_query(
        db_name=os.getenv("NEO4J_DATABASE"),
        query=query
    )
    return response