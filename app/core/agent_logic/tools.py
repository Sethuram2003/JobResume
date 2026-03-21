from langchain.tools import tool
from app.core.LatexModule.LatexTemplate import generate_latex
from app.core.model import ResumeData
from app.core.LatexModule.LatexFunction import render
import uuid

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
