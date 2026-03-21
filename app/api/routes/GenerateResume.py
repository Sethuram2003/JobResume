import uuid
from fastapi import FastAPI, APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from app.core.LatexModule.LatexTemplate import generate_latex
from app.core.model import ResumeData
from app.core.LatexModule.LatexFunction import render

generate_resume_router = APIRouter(tags=["generate_resume"])
app = FastAPI()

@generate_resume_router.post("/generate_resume")
def generate_resume(resume_data: ResumeData):
    latex_code = generate_latex(resume_data)
    
    unique_id = uuid.uuid4().hex
    base_filename = f"resume_{unique_id}"
    
    try:
        pdf_path = render(latex_code, filename=base_filename)
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="resume.pdf"
        )
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return JSONResponse(
            {'error': str(e)},
            status_code=500
        )