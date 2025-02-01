from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import time
import json
from groq import Groq

class PaperAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize with Groq API"""
        self.client = Groq(api_key=api_key)
        print("✅ Connected to Groq API")
        
    def fetch_paper_content(self, url: str) -> str:
        """Fetch content from paper URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unnecessary elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
                
            return soup.get_text(strip=True)
        except Exception as e:
            print(f"⚠️ Error fetching content from {url}: {str(e)}")
            return ""

    def generate_response(self, prompt: str) -> str:
        """Generate response using Llama 3 through Groq"""
        try:
            # Using Llama 3 model through Groq
            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",  # Fast and powerful model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a research assistant skilled in academic writing and analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            return completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            return "Error generating synopsis. Please try again."

    def analyze_papers(self, papers: List[Dict]) -> List[Dict]:
        """Analyze papers and return structured analysis"""
        print("🔍 Starting paper analysis...")
        
        # Sort and select most relevant papers
        query = papers[0]['Title'].lower()
        papers_sorted = sorted(papers, 
            key=lambda x: sum(word in x['Title'].lower() for word in query.split()))
        relevant_papers = papers_sorted[-3:]
        print(f"📚 Selected {len(relevant_papers)} most relevant papers for analysis")

        # Store papers for references
        self.paper_analyses = relevant_papers
        return relevant_papers

    def create_synopsis(self, papers: List[Dict]) -> Dict[str, str]:
        """Create a structured synopsis from the analyzed papers"""
        print("📝 Generating Research Synopsis...")
        
        # Analyze papers once and store result
        self.paper_analyses = self.analyze_papers(papers)
        research_topic = papers[0]['Title'].lower()
        sections = {}
        
        # Generate title
        print("📄 Generating Title...")
        title_prompt = f"Generate a formal academic title for a research synopsis about {research_topic}."
        sections['title'] = self.generate_response(title_prompt)
        
        # Generate introduction
        print("📄 Generating Introduction...")
        intro_prompt = (
            f"Write a comprehensive introduction paragraph (approximately 150 words) about {research_topic}. "
            "Focus on: current challenges, limitations of existing methods, and the need "
            "for better approaches. Keep it formal and academic."
        )
        sections['introduction'] = self.generate_response(intro_prompt)
        
        # Generate rationale
        print("📄 Generating Rationale...")
        rationale_prompt = (
            f"Write a single focused paragraph (approximately 120 words) explaining why this research on {research_topic} "
            "is important. Emphasize the advantages and potential impact of the proposed approach. "
            "Keep it concise and well-structured."
        )
        sections['rationale'] = self.generate_response(rationale_prompt)
        
        # Generate objectives
        print("📄 Generating Objectives...")
        objectives_prompt = (
            f"List exactly 3 specific, measurable objectives for the research on {research_topic}. "
            "Format as numbered list (1. 2. 3.). Each objective should start with 'To' and include specific "
            "metrics or targets. Make them detailed and achievable."
        )
        sections['objectives'] = self.generate_response(objectives_prompt)
        
        # Generate literature review
        print("📄 Generating Literature Review...")
        lit_review_prompt = (
            f"Write a comprehensive literature review (approximately 250 words) about {research_topic}. "
            "Cover current approaches, methods being used, challenges, and recent advancements. "
            "Write in flowing paragraphs without points or headings. Keep it academic and concise."
        )
        sections['literature_review'] = self.generate_response(lit_review_prompt)
        
        # Generate methodology
        print("📄 Generating Methodology...")
        method_prompt = (
            f"Write a detailed methodology section for {research_topic} with these components:\n"
            "1. Data Collection (numbered points)\n"
            "2. Data Preprocessing (numbered points)\n"
            "3. Feature Extraction (numbered points)\n"
            "4. Model Selection (numbered points)\n"
            "5. Evaluation Methods (numbered points)\n"
            "Make it technical and specific to the research topic."
        )
        sections['methodology'] = self.generate_response(method_prompt)
        
        # Generate feasibility study
        print("📄 Generating Feasibility Study...")
        feasibility_prompt = (
            f"Write a detailed feasibility analysis (approximately 300 words) for {research_topic} covering:\n"
            "1. Technical feasibility (available technologies and tools)\n"
            "2. Operational feasibility (implementation and deployment)\n"
            "3. Economic feasibility (cost-benefit analysis)\n"
            "4. Schedule feasibility (time requirements)\n"
            "Make it specific to the proposed research."
        )
        sections['feasibility'] = self.generate_response(feasibility_prompt)
        
        # Generate facilities required
        print("📄 Generating Facilities Required...")
        facilities_prompt = (
            f"List all required facilities and resources for the {research_topic} project, including:\n"
            "1. Hardware requirements\n"
            "2. Software requirements\n"
            "3. Data storage and processing facilities\n"
            "4. Development and testing environment\n"
            "5. Any specialized equipment or resources\n"
            "Make it comprehensive and specific to the research requirements."
        )
        sections['facilities'] = self.generate_response(facilities_prompt)
        
        # Generate expected outcomes
        print("📄 Generating Outcomes...")
        outcomes_prompt = (
            f"Write a single comprehensive paragraph (approximately 150 words) describing the expected outcomes "
            f"of the {research_topic} research. Include empirical results, practical applications, and potential "
            "impact. Keep it specific and measurable. Do not use any special formatting or bullet points."
        )
        sections['outcomes'] = self.generate_response(outcomes_prompt)
        
        return sections

    def save_synopsis(self, synopsis: Dict[str, str], filename: str = "data/research_synopsis.md"):
        """Save the synopsis to a markdown file"""
        print("💾 Saving Research Synopsis...")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Title
                f.write("# " + synopsis.get('title', '') + "\n\n")
                f.write("---\n\n")
                
                # Introduction with sections
                f.write("# Introduction\n\n")
                intro_text = synopsis.get('introduction', '')
                paragraphs = intro_text.split('\n\n')
                
                # First paragraph is the introduction
                if paragraphs:
                    f.write(paragraphs[0] + "\n\n")
                
                # Add Rationale heading and content
                f.write("## Rationale\n\n")
                if len(paragraphs) > 1:
                    f.write(paragraphs[1] + "\n\n")
                
                # Add Objectives with heading
                f.write("## Objectives\n\n")
                f.write(synopsis.get('objectives', '') + "\n\n")
                
                # Main Sections
                main_sections = {
                    'Literature Review': synopsis.get('literature_review', ''),
                    'Feasibility Study': synopsis.get('feasibility', ''),
                    'Methodology/Planning of Project': synopsis.get('methodology', ''),
                    'Facilities Required for Proposed Work': synopsis.get('facilities', ''),
                    'Expected Outcomes': synopsis.get('outcomes', '')
                }
                
                for title, content in main_sections.items():
                    f.write(f"# {title}\n")
                    f.write(content + "\n\n")
                
                # References at the end
                f.write("# References\n\n")
                for paper in self.paper_analyses:
                    title = paper['Title']  # Note the capital T
                    authors = paper.get('Authors', '')
                    year = paper.get('Year', '')
                    url = paper.get('URL', '')
                    
                    ref = f"{authors} ({year}). {title}."
                    if url and url != 'N/A':
                        ref += f" Retrieved from {url}"
                    
                    f.write(f"{ref}\n\n")
            
            print(f"✅ Synopsis saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving synopsis: {str(e)}")
            raise  # Re-raise the exception to see the full error
