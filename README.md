# Digital Dark Spot

## 🌐 Live Demo

🚀 **Try Digital Dark Spot here:**

https://digital-dark-spot-zeta.vercel.app/

**GitHub Repository:** https://github.com/SrinisthaD/digital-dark-spot

### AI-Assisted Information Gap Detection Platform

Digital Dark Spot is an AI-powered web application that helps users identify potential information gaps, conflicting claims, outdated information, and unanswered questions across multiple online sources.

Instead of simply summarizing information, the platform helps users understand **what may be missing, what needs verification, and where further research is required**.

## Problem Statement

When researching a topic online, information is often scattered across different websites. Some sources may provide incomplete explanations, outdated details, or claims that appear inconsistent.

Manually comparing multiple sources can be time-consuming.

Digital Dark Spot aims to make this process easier using AI-assisted analysis.

## Key Features

- **Multi-Source Analysis:** Analyze multiple webpage URLs for a research topic.
- **AI-Powered Summaries:** Generate a concise overview of the collected information.
- **Information Gap Detection:** Identify topics or details that may not be adequately covered.
- **Potential Conflict Detection:** Highlight claims that appear inconsistent across sources.
- **Outdated Information Signals:** Flag details that may require updated verification.
- **Unanswered Questions:** Suggest questions for further investigation.
- **Evidence References:** Show source IDs, supporting text, and AI confidence labels.
- **Prioritized Verification Checklist:** Organize follow-up tasks into High, Medium, and Low priority.
- **Downloadable Reports:** Export the analysis as a JSON file.

## Technology Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Requests
- BeautifulSoup

**AI Integration**
- Google Gemini API

**Version Control**
- Git and GitHub

## How It Works

1. The user enters a research topic and one or more webpage URLs.
2. The Python backend retrieves and extracts text from the webpages.
3. The extracted content is sent to Gemini for analysis.
4. Gemini generates a structured report identifying potential gaps, conflicts, outdated signals, and unanswered questions.
5. The frontend displays the results alongside source references and a prioritized verification checklist.
6. The user can download the analysis as a JSON report.

## Running the Project Locally

### Prerequisites

- Python
- Node.js and npm
- A Google Gemini API key

### Backend Setup

Open a terminal in the `backend` folder.

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi uvicorn requests beautifulsoup4 python-dotenv google-genai
```

Create a `.env` file inside `backend`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

### Frontend Setup

Open a second terminal in the `frontend` folder.

Install dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

Frontend URL: `http://localhost:5173`

## Responsible AI Disclaimer

Digital Dark Spot identifies **potential** information gaps and inconsistencies. Its findings are AI-generated suggestions, not verified facts.

Missing information in extracted webpage content does not necessarily mean the original source lacks that information. Users should consult the original sources and independently verify important claims.

## Current Limitations

- Some websites may block automated content extraction.
- Webpage navigation elements may appear in extracted text.
- Long webpages may be truncated during processing.
- AI-generated findings may be incomplete or inaccurate.
- The application currently runs locally and requires a configured Gemini API key.

## Future Improvements

- Improved article-content extraction
- PDF document analysis
- PDF report downloads
- Better conflict comparison and evidence verification
- Public web deployment

## Project Repository

https://github.com/SrinisthaD/digital-dark-spot

---

**Digital Dark Spot — Discover what the information might be missing.**