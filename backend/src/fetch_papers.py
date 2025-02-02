import os
import time
import random
import pandas as pd
from typing import List, Dict
from scholarly import scholarly
from dotenv import load_dotenv

load_dotenv()

def fetch_all_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from Google Scholar"""
    papers = []
    
    try:
        print(f"🔍 Fetching research papers for query: {query}")
        
        # Search Google Scholar
        search_query = scholarly.search_pubs(query)
        count = 0
        
        while count < max_results:
            try:
                paper = next(search_query)
                
                # Extract paper info
                paper_info = {
                    'Title': paper.get('bib', {}).get('title', 'N/A'),
                    'Abstract': paper.get('bib', {}).get('abstract', 'N/A'),
                    'Authors': ', '.join(paper.get('bib', {}).get('author', [])),
                    'Year': paper.get('bib', {}).get('pub_year', 'N/A'),
                    'Venue': paper.get('bib', {}).get('venue', 'N/A'),
                    'URL': paper.get('pub_url', 'N/A')
                }
                
                # Only add papers with abstracts
                if paper_info['Abstract'] != 'N/A':
                    papers.append(paper_info)
                    count += 1
                    print(f"✅ Found paper {count}/{max_results}")
                    
                # Increase the random delay between requests to avoid blocking
                time.sleep(random.uniform(5, 10))  # Increased delay
                
            except StopIteration:
                print("⚠️ No more papers found")
                break
            except Exception as e:
                print(f"⚠️ Error processing paper: {str(e)}")
                time.sleep(random.uniform(5, 10))  # Longer delay on error
                continue
        
        print(f"✅ Successfully found {len(papers)} papers on Google Scholar")
        
    except Exception as e:
        print(f"❌ Error fetching papers: {str(e)}")
    
    return papers

def save_to_csv(papers: List[Dict], filename: str = "data/research_papers.csv"):
    """Save papers to CSV file"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"✅ Research papers saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")
