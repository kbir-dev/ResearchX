from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.fetch_papers import fetch_all_papers, save_to_csv
from src.utils import PaperAnalyzer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaperRequest(BaseModel):
    query: str
    max_results: int = 10

@app.post("/fetch-papers/")
async def fetch_papers(request: PaperRequest):
    """Fetch research papers based on a query."""
    papers = fetch_all_papers(request.query, max_results=request.max_results)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the given topic.")
    return {"papers": papers}

@app.post("/analyze-papers/")
async def analyze_papers(request: PaperRequest):
    """Analyze research papers and generate a synopsis."""
    papers = fetch_all_papers(request.query, max_results=request.max_results)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the given topic.")
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set in environment variables.")
    
    analyzer = PaperAnalyzer(api_key)
    synopsis = analyzer.create_synopsis(papers)
    
    return {"synopsis": synopsis}

@app.post("/save-papers/")
async def save_papers(request: PaperRequest):
    """Save fetched papers to a CSV file."""
    papers = fetch_all_papers(request.query, max_results=request.max_results)
    if not papers:
        raise HTTPException(status_code=404, detail="No papers found for the given topic.")
    
    save_to_csv(papers)
    return {"message": "Papers saved to CSV successfully."} 