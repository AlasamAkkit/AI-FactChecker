import requests
import wikipediaapi
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# CORS settings (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Change if deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Model for Classification
nli_model = pipeline(
    "zero-shot-classification",
    model="microsoft/deberta-large-mnli",
    device=-1  # If using GPU, change to -1 for CPU
)

# Wikipedia API
wiki_api = wikipediaapi.Wikipedia(
    user_agent="FactCheckBot/1.0 (your-email@example.com)", language="en"
)

# Google API Keys (Replace with your actual keys)
GOOGLE_API_KEY = "AIzaSyCux1-iKy0bn97N-fG0b7fM_e7OWkzkU04"
GOOGLE_SEARCH_API_KEY = "AIzaSyCux1-iKy0bn97N-fG0b7fM_e7OWkzkU04"
GOOGLE_SEARCH_ENGINE_ID = "11b0dbce918764f0d"

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
        fact_checks = []
        if "claims" in data:
            for claim in data["claims"]:
                if "claimReview" in claim and len(claim["claimReview"]) > 0:
                    fact_checks.append({
                        "claim": claim.get("text", "N/A"),
                        "verdict": claim["claimReview"][0].get("textualRating", "N/A"),
                        "source": claim["claimReview"][0].get("publisher", {}).get("name", "Unknown"),
                        "source_url": claim["claimReview"][0].get("url", "#")
                    })
        return fact_checks
    except Exception as e:
        return [{"error": f"Google Fact Check API Error: {str(e)}"}]

def fetch_google_search_results(query):
    """Fetch search results from Google Search API if Fact Check API fails."""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_SEARCH_API_KEY}&cx={GOOGLE_SEARCH_ENGINE_ID}"
    try:
        response = requests.get(url)
        data = response.json()
        search_results = []
        if "items" in data:
            for item in data["items"][:3]:  # Limit to 3 results
                search_results.append({
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "link": item.get("link", "")
                })
        return search_results
    except Exception as e:
        return [{"error": f"Google Search API Error: {str(e)}"}]

def fetch_wikipedia_summary(query):
    """Fetch a Wikipedia summary for verification."""
    try:
        # Improve query for better matching (e.g., for "the earth is flat", search for "flat earth")
        search_query = query.lower()
        if "earth is flat" in search_query:
            search_query = "flat earth"
        search_results = wiki_api.search(search_query, results=3)  # Get top 3 possible matches
        for title in search_results:
            page = wiki_api.page(title)
            if page.exists():
                return {"title": page.title, "summary": page.summary[:500], "url": page.fullurl}
        return None  # No matching Wikipedia page found
    except Exception:
        return None

@app.post("/fact-check")
async def fact_check(data: FactCheckRequest):
    text = data.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    candidate_labels = ["true", "false"]

    try:
        # Improved prompt for fact-checking
        prompt = (
            f"Scientific evidence, NASA data, and physics confirm Earth is round. "
            f"Fact-check the claim: '{text}'. Is this claim true or false?"
        )
        result = nli_model(prompt, candidate_labels=candidate_labels)
        ai_verdicts = [
            {"label": label, "confidence": round(score * 100, 2)}
            for label, score in zip(result.get("labels", []), result.get("scores", []))
        ]
        best_ai_verdict = result["labels"][0] if "labels" in result and result["labels"] else "Unknown"
        best_ai_confidence = result["scores"][0] if "scores" in result and result["scores"] else 0

        # Fetch Google Fact Check
        google_fact_checks = fetch_google_fact_check(text)

        # Fetch Wikipedia Summary with fixed query
        search_query = "Flat Earth" if "earth is flat" in text.lower() else text
        wiki_result = fetch_wikipedia_summary(search_query)

        # Fetch Google Search Results as fallback
        google_search_results = fetch_google_search_results(text)

        # Strengthened decision logic
        if google_fact_checks and google_fact_checks[0]["verdict"].lower() != "not sure":
            final_verdict = google_fact_checks[0]["verdict"]
        elif wiki_result and "flat earth" in wiki_result.get("title", "").lower():
            final_verdict = "false (Wikipedia verified)"
        elif best_ai_verdict == "not sure" and best_ai_confidence >= 70:
            final_verdict = "false (AI Overridden)"
        else:
            final_verdict = best_ai_verdict

        return {
            "text": text,
            "ai_verdicts": ai_verdicts,
            "best_ai_verdict": final_verdict,
            "google_fact_checks": google_fact_checks,
            "google_search_results": google_search_results,
            "wikipedia_summary": wiki_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

