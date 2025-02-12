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
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Development
        "https://research-3xhvgilgw-kbir-devs-projects.vercel.app",  # Production
        "https://research-f9q1hz88e-kbir-devs-projects.vercel.app",  # Also allow this domain
        "https://researchx.vercel.app",  # Main domain
        "*"  # Allow all origins temporarily for debugging
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this after creating the FastAPI app
app.mount("/data", StaticFiles(directory="data"), name="data")

class PaperRequest(BaseModel):
    query: str
    max_results: int = 10

@app.post("/api/fetch-papers/")
async def fetch_papers(request: PaperRequest, db: Session = Depends(get_db)):
    """Fetch research papers based on a query."""
    try:
        # Check cache first
        cached_research = db.query(Research).filter(Research.query == request.query).first()
        
        if cached_research and cached_research.papers:
            print(f"✅ Found cached results for: {request.query}")
            return {"papers": cached_research.papers}
        
        # Fetch new papers
        print(f"🔍 Fetching new papers for: {request.query}")
        papers = fetch_all_papers(request.query, max_results=request.max_results)
        
        if not papers or len(papers) == 0:
            raise HTTPException(status_code=404, detail="No papers found for the given topic. Please try a different search query.")
        
        # Save to database
        csv_path = save_to_csv(papers)
        if csv_path:
            new_research = Research(
                query=request.query,
                papers=papers,
                csv_path=csv_path
            )
            db.add(new_research)
            db.commit()
        
        return {"papers": papers}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"❌ Error in fetch_papers endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while fetching papers. Please try again later."
        )

@app.post("/api/analyze-papers/")
async def analyze_papers(request: PaperRequest, db: Session = Depends(get_db)):
    """Analyze research papers and generate a synopsis."""
    try:
        # Get papers from cache or fetch new ones
        cached_research = db.query(Research).filter(Research.query == request.query).first()
        papers = cached_research.papers if cached_research else fetch_all_papers(request.query, max_results=request.max_results)
        
        if not papers:
            raise HTTPException(status_code=404, detail="No papers found for the given topic.")
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not set in environment variables.")
        
        # Always generate new synopsis
        analyzer = PaperAnalyzer(api_key)
        synopsis = analyzer.create_synopsis(papers)
        
        # Update or create database entry with new synopsis
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
    except Exception as e:
        print(f"❌ Error in analyze_papers endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while analyzing papers: {str(e)}"
        )

@app.get("/api/download/{file_type}/{query}")
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True) 