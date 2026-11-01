from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_url
from analyzer import analyze_sources
import time

# Create our FastAPI application
app = FastAPI(title="Digital Dark Spot API")


# Allow our React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://digital-dark-spot-zeta.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the information our frontend will send
class ResearchRequest(BaseModel):
    topic: str
    sources: list[str]


# Check whether the backend is running
@app.get("/")
def home():
    return {
        "message": "Digital Dark Spot backend is running!"
    }


# Receive a research topic and extract information from its URLs
@app.post("/analyze")
def analyze_research(request: ResearchRequest):

    
    start_time = time.perf_counter()

    extracted_sources = []

    for url in request.sources:
        result = scrape_url(url)
        extracted_sources.append(result)

    scraping_seconds = time.perf_counter() - start_time
    print(f"Scraping took {scraping_seconds:.2f} seconds", flush=True)

    ai_start = time.perf_counter()

    analysis = analyze_sources(request.topic, extracted_sources)

    ai_seconds = time.perf_counter() - ai_start
    print(f"Gemini analysis took {ai_seconds:.2f} seconds", flush=True)


    analysis["source_details"] = [
        {
            "id": f"S{index}",
            "title": source["title"],
            "url": source["url"]
        }
        for index, source in enumerate(
            [s for s in extracted_sources if s["error"] is None and s["text"]],
            start=1
        )
    ]

    return analysis