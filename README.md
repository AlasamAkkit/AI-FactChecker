# 🛡️ FactCheck AI - AI-Powered Misinformation Detector

FactCheck AI is a web application that uses **Natural Language Processing (NLP)** to detect **false claims** and combat misinformation.  
It employs a **Zero-Shot Classification Model (Facebook BART-Large MNLI)** to verify the truthfulness of user-input claims.  

---

## ✨ Features
✅ **AI-Powered Fact-Checking** - Uses **LLM (Large Language Models)** to analyze claims  
✅ **Confidence Score Analysis** - Provides multiple verdicts with confidence percentages  
✅ **Real-time Processing** - Instant results with a user-friendly interface  
✅ **FastAPI Backend** - Lightweight and high-performance backend  
✅ **Next.js Frontend** - Modern UI with React-based framework  

---

## 📌 Tech Stack
- **Frontend:** Next.js, React, TailwindCSS  
- **Backend:** FastAPI (Python), Transformers (HuggingFace)  
- **ML Model:** `facebook/bart-large-mnli` (Zero-Shot Classification) 

---

## 🚀 Getting Started

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/factcheck-ai.git
cd factcheck-ai

Backend Setup (FastAPI)
🔹 Create a Python Virtual Environment
cd factcheck-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
1️⃣ Enter a claim or statement (e.g., "The Earth is flat.").
2️⃣ Click "Fact Check" to analyze the claim.
3️⃣ View the AI Verdict with confidence scores.

