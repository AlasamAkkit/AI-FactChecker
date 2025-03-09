# 🛡️ AI FactChecker - Combating Misinformation with AI

AI FactChecker is an **AI-powered misinformation detection platform** that analyzes **claims, news, and online content** to verify their accuracy. Using **Natural Language Processing (NLP) and fact-checking APIs**, the platform provides **real-time fact verification** for users.

---

## ✨ Features
✅ **AI-Powered Claim Verification** - Uses **zero-shot classification models**  
✅ **Google Fact Check API Integration** - Cross-checks claims with trusted fact-checking sources  
✅ **Wikipedia Verification** - Fetches summaries for evidence-backed analysis  
✅ **Google Search Backup** - Retrieves **real-time news articles** if fact-checking is unavailable  
✅ **FastAPI Backend + Next.js Frontend** - High-performance, scalable infrastructure  

---

## 🛠 Tech Stack
- **Frontend:** Next.js (React), TailwindCSS  
- **Backend:** FastAPI, Hugging Face Transformers, Wikipedia API, Google APIs  
- **ML Model:** `microsoft/deberta-large-mnli` (Zero-Shot Classification)  
- **APIs Used:**
  - Google **Fact Check API** (for claim verification)
  - Google **Custom Search API** (for retrieving news articles)
  - Wikipedia **API** (for knowledge-based verification)

---

## 🚀 Getting Started

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/AI-FactChecker.git
cd AI-FactChecker
2️⃣ Backend Setup (FastAPI)
🔹 Create a Python Virtual Environment
python -m venv venv
source venv/bin/activate  

🔹 Install Dependencies
pip install -r requirements.txt

🔹 Run the Backend Server
uvicorn main:app --reload
✅ API should now be running at: http://127.0.0.1:8000/

3️⃣ Frontend Setup (Next.js)
🔹 Navigate to the Frontend Directory

cd factcheck-client
🔹 Install Dependencies

npm install
🔹 Run the Frontend
npm run dev
✅ Frontend should be available at: http://localhost:3000/

🎯 How to Use
1️⃣ Enter a claim (e.g., "The Earth is flat.").
2️⃣ Click "Fact Check" to analyze the claim.
3️⃣ View AI Verdict, Google Fact Checks, Wikipedia Summary, and Search Results.