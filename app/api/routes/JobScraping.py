from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from app.core.LinkedinModule.LinkedinFunction import scrape_linkedin_jobs

router = APIRouter(tags=["JobScraper"])

@router.post("/LinkedinScrape")
async def linkedin_scrape(keyword: str, location: str, max_jobs: int = 10):
    """
    Scrape LinkedIn jobs for a given keyword and location.
    """
    try:
        jobs = scrape_linkedin_jobs(keyword, location, max_jobs)
        return JSONResponse(status_code=200, content={"jobs": jobs})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    