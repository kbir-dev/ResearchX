from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.fetch_papers import fetch_all_papers, save_to_csv
from src.utils import PaperAnalyzer
from src.database import get_db, Research
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this after creating the FastAPI app
app.mount("/data", StaticFiles(directory="data"), name="data")

class PaperRequest(BaseModel):
    query: str
    max_results: int = 10

@app.post("/fetch-papers/")
async def fetch_papers(request: PaperRequest, db: Session = Depends(get_db)):
    """Fetch research papers based on a query."""
    # Check if we have cached results
    cached_research = db.query(Research).filter(Research.query == request.query).first()
    
    if cached_research:
        return {"papers": cached_research.papers}
    
    # If not cached, fetch new papers
    papers = fetch_all_papers(request.query, max_results=request.max_results)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the given topic.")
    
    # Save papers to CSV
    csv_path = save_to_csv(papers)
    
    # Create new research entry
    new_research = Research(
        query=request.query,
        papers=papers,
        csv_path=csv_path
    )
    db.add(new_research)
    db.commit()
    
    return {"papers": papers}

@app.post("/analyze-papers/")
async def analyze_papers(request: PaperRequest, db: Session = Depends(get_db)):
    """Analyze research papers and generate a synopsis."""
    # Check if we have cached results
    cached_research = db.query(Research).filter(Research.query == request.query).first()
    
    if cached_research and cached_research.synopsis:
        return {"synopsis": cached_research.synopsis}
    
    # If not cached or no synopsis, generate new synopsis
    papers = cached_research.papers if cached_research else fetch_all_papers(request.query, max_results=request.max_results)
    
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the given topic.")
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set in environment variables.")
    
    analyzer = PaperAnalyzer(api_key)
    synopsis = analyzer.create_synopsis(papers)
    
    # Save synopsis to database
    if cached_research:
        cached_research.synopsis = synopsis
        cached_research.docx_path = analyzer.save_synopsis_as_docx(synopsis)
        db.commit()
    else:
        new_research = Research(
            query=request.query,
            papers=papers,
            synopsis=synopsis,
            docx_path=analyzer.save_synopsis_as_docx(synopsis)
        )
        db.add(new_research)
        db.commit()
    
    return {"synopsis": synopsis}

@app.get("/download/{file_type}/{query}")
async def get_download_path(file_type: str, query: str, db: Session = Depends(get_db)):
    """Get the download path for CSV or DOCX file."""
    research = db.query(Research).filter(Research.query == query).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    
    if file_type == "csv":
        if not research.csv_path:
            raise HTTPException(status_code=404, detail="CSV file not found")
        return {"path": research.csv_path}
    
    elif file_type == "docx":
        if not research.docx_path:
            raise HTTPException(status_code=404, detail="DOCX file not found")
        return {"path": research.docx_path}
    
    raise HTTPException(status_code=400, detail="Invalid file type") 