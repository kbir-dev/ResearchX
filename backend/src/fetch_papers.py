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
        print(f"🔍 Starting search for: {query}")
        
        # Search Google Scholar with timeout and retries
        search_query = scholarly.search_pubs(query)
        count = 0
        retries = 3
        
        while count < max_results and retries > 0:
            try:
                paper = next(search_query)
                print(f"📄 Processing paper {count + 1}")
                
                # Extract paper info with error checking
                paper_info = {
                    'Title': paper.get('bib', {}).get('title', 'N/A'),
                    'Abstract': paper.get('bib', {}).get('abstract', 'N/A'),
                    'Authors': ', '.join(paper.get('bib', {}).get('author', [])),
                    'Year': paper.get('bib', {}).get('pub_year', 'N/A'),
                    'Venue': paper.get('bib', {}).get('venue', 'N/A'),
                    'URL': paper.get('pub_url', 'N/A')
                }
                
                if paper_info['Abstract'] != 'N/A':
                    papers.append(paper_info)
                    count += 1
                    print(f"✅ Added paper {count}/{max_results}")
                
                time.sleep(random.uniform(2, 4))  # Random delay
                
            except StopIteration:
                print("⚠️ No more papers available")
                break
            except Exception as e:
                print(f"⚠️ Error processing paper: {str(e)}")
                retries -= 1
                time.sleep(5)  # Longer delay on error
                if retries == 0:
                    print("❌ Max retries reached")
                    break
        
        if papers:
            print(f"✅ Successfully found {len(papers)} papers")
        else:
            print("❌ No papers found")
        
    except Exception as e:
        print(f"❌ Fatal error in fetch_papers: {str(e)}")
    
    return papers

def save_to_csv(papers: List[Dict], filename: str = "data/research_papers.csv"):
    """Save papers to CSV file"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"✅ Research papers saved to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")
        return None
