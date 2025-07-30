# 🧠 Research Paper Summarizer & Analyzer

An AI-powered virtual research assistant that fetches academic papers from **ArXiv** and **Google Scholar**, summarizes them using local or hosted LLMs, and highlights each paper’s **advantages** and **disadvantages**. Built using `AutoGen`, `Streamlit`, and Groq/Ollama for fast local model inference.

## 🚀 Features

- 📥 Fetches top papers from ArXiv & Google Scholar.
- 🧠 Summarizes research papers using an LLM agent.
- ✅ Analyzes pros and cons of each paper.
- 🔎 Suggests related research topics using AI.
- 🖥️ Interactive UI built with Streamlit.
- ⚙️ Supports local LLMs (via Ollama) or cloud models (via Groq API).

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🔧 Setup

1. Set your API key in a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

> Or switch to a local Ollama model by updating `agents.py` config (see commented lines).

2. (Optional) Start Ollama server if using local LLMs:
```bash
ollama serve
```

## 🧪 Run the App

```bash
streamlit run app.py
```

Then open your browser at:  
`http://localhost:8501`

---

