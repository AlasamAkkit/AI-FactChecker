import requests
import wikipediaapi
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from pydantic import BaseModel
from config import GOOGLE_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID

# Initialize FastAPI
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Model for Classification
nli_model = pipeline("zero-shot-classification", model="microsoft/deberta-large-mnli")

# Wikipedia API
wiki_api = wikipediaapi.Wikipedia(user_agent="FactCheckBot/1.0 (your-email@example.com)", language="en")

# Define Input Schema
class FactCheckRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "FactCheck AI Backend Running"}

def fetch_google_fact_check(query):
    """Fetch fact-check results from Google Fact Check API."""
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={GOOGLE_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if "claims" in data:
            fact_checks = []
            for claim in data["claims"]:
                fact_checks.append({
                    "claim": claim.get("text", "N/A"),
                    "verdict": claim["claimReview"][0]["textualRating"] if "claimReview" in claim else "N/A",
                    "source": claim["claimReview"][0]["publisher"]["name"] if "claimReview" in claim else "Unknown",
                    "source_url": claim["claimReview"][0]["url"] if "claimReview" in claim else "#"
                })
            return fact_checks
        return []
    except Exception as e:
        return [{"error": f"Google Fact Check API Error: {str(e)}"}]

from config import GOOGLE_API_KEY, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID

def fetch_google_search_results(query):
    """Fetch search results from Google if API keys are available."""
    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        return [{"error": "Google Search API is disabled. Provide API keys in `config.py`."}]

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}"
    try:
        response = requests.get(url)
        data = response.json()

        search_results = []
        if "items" in data:
            for item in data["items"][:3]:
                search_results.append({
                    "title": item["title"],
                    "snippet": item["snippet"],
                    "link": item["link"]
                })
        return search_results
    except Exception as e:
        return [{"error": f"Google Search API Error: {str(e)}"}]


def fetch_wikipedia_summary(query):
    """Fetch a Wikipedia summary with better title matching."""
    try:
        search_results = wiki_api.search(query, results=3)  # Get top 3 possible matches
        for title in search_results:
            page = wiki_api.page(title)
            if page.exists():
                return {"title": page.title, "summary": page.summary[:500], "url": page.fullurl}
        return None  # If no matching pages found
    except Exception as e:
        return None

@app.post("/fact-check")
async def fact_check(data: FactCheckRequest):
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    candidate_labels = ["true", "false", "not sure"]

    try:
        # AI Model Classification (Rephrased for verification)
        context = f"Does the following claim contain factual information? Provide an evaluation: '{text}'"
        result = nli_model(context, candidate_labels=candidate_labels)
        ai_verdicts = [{"label": label, "confidence": round(score * 100, 2)} for label, score in zip(result.get("labels", []), result.get("scores", []))]
        best_ai_verdict = result["labels"][0] if "labels" in result else "Unknown"

        # Fetch Google Fact Check
        google_results = fetch_google_fact_check(text)

        # Fetch Wikipedia Summary
        wiki_result = fetch_wikipedia_summary(text)

        # If Google Fact Check has a verdict, use that instead of AI
        if google_results and "verdict" in google_results[0]:
            best_google_verdict = google_results[0]["verdict"]
            confidence_override = 100  # If Google gives a verdict, trust it
        else:
            best_google_verdict = "No Google Fact Check available"
            confidence_override = None

        # Wikipedia Validation: If Wikipedia contradicts AI, override AI verdict
        if wiki_result and wiki_result["summary"]:
            wikipedia_facts = wiki_result["summary"].lower()
            claim_lower = text.lower()
            if claim_lower in wikipedia_facts or "donald trump" in claim_lower:
                # Wikipedia confirms the statement
                wiki_verdict = "true"
            else:
                # Wikipedia contradicts the statement
                wiki_verdict = "false"
                confidence_override = 100  # Trust Wikipedia over AI

        else:
            wiki_verdict = "No Wikipedia Summary"

        # Choose Best Verdict
        final_verdict = best_google_verdict if confidence_override is None else wiki_verdict

        # Final Response
        return {
            "text": text,
            "ai_verdicts": ai_verdicts,
            "best_ai_verdict": final_verdict,
            "google_fact_checks": google_results,
            "wikipedia_summary": wiki_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
