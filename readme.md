# 🚀 ResearchX - AI-Powered Research Assistant

<div align="center">
  
  [![Made with AI](https://img.shields.io/badge/Made%20with-AI-blueviolet?style=for-the-badge)](https://github.com/Devansh-365/researchx)
  [![Built with Groq](https://img.shields.io/badge/Built%20with-Groq-indigo?style=for-the-badge)](https://groq.com)
  [![Powered by FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688?style=for-the-badge)](https://fastapi.tiangolo.com)
  [![Made with React](https://img.shields.io/badge/Made%20with-React-61DAFB?style=for-the-badge&logo=react)](https://reactjs.org)
</div>

## 🌟 Overview

ResearchX is an AI-powered research assistant that helps researchers, students, and academics explore research papers and generate comprehensive research synopses. Built entirely using AI tools (Claude, Cursor, V0), this project demonstrates the power of AI-assisted development in creating sophisticated applications.

### ✨ Key Features

- 🔍 Smart paper search and analysis
- 📝 AI-generated research synopses
- 📊 Downloadable CSV reports
- 📄 Word document generation
- 🎨 Beautiful, responsive UI
- ⚡ Real-time processing feedback

## 🛠️ Tech Stack

### Frontend
- React + Vite
- TailwindCSS
- Lucide Icons
- Typography Plugin

### Backend
- FastAPI
- SQLite + SQLAlchemy
- Groq AI
- Python-docx
- Pandas

## 🎯 AI Development Tools Used

This project was built entirely using AI assistance:

- **Claude (Anthropic)**: Primary development assistant for code generation and problem-solving
- **Cursor**: AI-powered code editor for intelligent code completion
- **V0**: AI pair programming assistant
- **Groq**: Large Language Model for research paper analysis

## 🚀 Getting Started

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Groq API Key

### Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/researchx.git
cd researchx
```

2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```
3. Configure Environment Variables

GROQ_API_KEY=your_groq_api_key

4. Setup Frontend

```bash
cd frontend
npm install
```

5. Start Application

```bash
Terminal 1 - Backend
cd backend
python -m uvicorn app:app --reload
Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🎨 Features in Detail

### Paper Search and Analysis
- Intelligent paper fetching based on user queries
- Real-time loading states with step-by-step feedback
- Smart paper relevance sorting

### AI Synopsis Generation
- Comprehensive research synopsis generation
- Structured format with sections:
  - Introduction
  - Rationale
  - Objectives
  - Literature Review
  - Feasibility Study
  - Methodology
  - Required Facilities
  - Expected Outcomes

### Export Options
- CSV export of research papers
- Word document export of complete synopsis
- Cached results for quick access

## 🎉 AI-Assisted Development

This project showcases the power of AI-assisted development:

- **Code Generation**: Large portions of the codebase were generated through interactions with Claude
- **Problem Solving**: AI assistants helped debug issues and suggest optimizations
- **UI Design**: AI tools helped create the beautiful, responsive interface
- **Documentation**: This README was crafted with AI assistance

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to Anthropic's Claude for being an incredible development partner
- Groq team for providing the powerful LLM API
- The amazing open-source community for the tools and libraries used

---

<div align="center">
  Made with 💜 and AI
  
  [Report Bug](https://github.com/your-username/researchx/issues) · [Request Feature](https://github.com/your-username/researchx/issues)
</div>