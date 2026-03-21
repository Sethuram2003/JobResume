import subprocess
from pathlib import Path
import shutil

def render(latex_code: str, filename: str = "output", compiler: str = "pdflatex") -> str:
    if not shutil.which(compiler):
        raise FileNotFoundError(f"{compiler} not found. Please install LaTeX.")
    
    base_dir = Path("resumes")
    base_dir.mkdir(exist_ok=True)
    
    tex_file = base_dir / f"{filename}.tex"
    pdf_file = base_dir / f"{filename}.pdf"
    
    try:
        tex_file.write_text(latex_code, encoding='utf-8')
        
        cmd = [compiler, "-interaction=nonstopmode", "-halt-on-error", f"{filename}.tex"]
        for run in range(2):
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
            if result.returncode != 0:
                raise RuntimeError(f"Compilation failed (run {run+1}):\n{result.stderr}")
        
        if not pdf_file.exists():
            raise RuntimeError(f"PDF not generated. stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            
    except Exception:
        if tex_file.exists():
            tex_file.unlink()
        raise
    
    for ext in [".aux", ".log", ".out", ".toc", ".synctex.gz"]:
        aux = base_dir / f"{filename}{ext}"
        if aux.exists():
            aux.unlink()
    
    return str(pdf_file.absolute())