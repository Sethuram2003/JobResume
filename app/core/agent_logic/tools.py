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
def generate_resume(resume_data: ResumeData) -> str:
    """ Tool to generate a resume PDF from structured data. Returns the file path of the generated PDF.
    """
    latex_content = generate_latex(resume_data)
    unique_id = uuid.uuid4().hex
    base_filename = f"resume_{unique_id}"
    try:
        pdf_path = render(latex_content, filename=base_filename)
        return pdf_path
    except Exception as e:
        return str(e)
    
@tool
def context_for_resume(query: str) -> str:
    """ Tool to query the Neo4j knowledge graph using RAG and return the answer. from the chat history. """

    pipeline = get_neo4j_service()
    response = pipeline.run_rag_query(
        db_name=os.getenv("NEO4J_DATABASE"),
        query=query
    )

    return response
