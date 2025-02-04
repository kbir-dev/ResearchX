from src.fetch_papers import fetch_all_papers, save_to_csv
from src.utils import PaperAnalyzer
from src.word_generator import convert_synopsis_to_word
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get Groq API key from environment
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ Please set GROQ_API_KEY in .env file")
        print("Get your API key from: https://console.groq.com/keys")
        exit(1)

    query = input("Enter research topic: ")  
    papers = fetch_all_papers(query, max_results=10)

    if papers:
        save_to_csv(papers)
        
        # Initialize analyzer and generate synopsis
        analyzer = PaperAnalyzer(api_key)
        synopsis = analyzer.create_synopsis(papers)
        
        # Save the synopsis to markdown
        analyzer.save_synopsis(synopsis)
        
        # Convert to Word
        convert_synopsis_to_word()
        
        print("\n✨ Synopsis generation complete! Check:")
        print("1. data/research_synopsis.md for markdown version")
        print("2. data/research_synopsis.docx for Word version")
    else:
        print("❌ No papers found for the given topic.")