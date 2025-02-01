from scholarly import scholarly
import pandas as pd
from typing import List, Dict
import time

def fetch_all_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch papers from Google Scholar"""
    papers = []
    
    try:
        print(f"🔍 Fetching Google Scholar papers for query: {query}")
        
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
                    
                time.sleep(2)  # Be nice to Google Scholar
                
            except StopIteration:
                break
            except Exception as e:
                print(f"⚠️ Error processing paper: {str(e)}")
                continue
        
        print(f"✅ Found {len(papers)} papers on Google Scholar")
        
    except Exception as e:
        print(f"❌ Error fetching papers: {str(e)}")
    
    return papers

def save_to_csv(papers: List[Dict], filename: str = "data/research_papers.csv"):
    """Save papers to CSV file"""
    try:
        df = pd.DataFrame(papers)
        df.to_csv(filename, index=False)
        print(f"✅ Research papers saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving to CSV: {str(e)}")
