# 📚 Semantic Book Recommendation System

A smart book recommender system powered by **vector search**, **emotion detection**, and **Gradio UI**. Given a brief description, category, and emotional tone, it suggests books using semantic similarity and emotional metadata.

## 🧠 Features

- ✨ Recommend books using **semantic search** (FAISS + embeddings).
- 🧾 Filter by book category (e.g., Romance, Fiction, History).
- 🎭 Select emotion tones (e.g., Happy, Sad, Suspenseful).
- 📊 Uses `books_with_emotions.csv` with pre-tagged emotional scores.
- 💡 Clean Gradio dashboard for easy interaction.

## 📦 Installation

```bash
pip install -r requirements.txt
```

## ⚙️ Setup

Make sure the paths in `gradio_dashboard.py` point to:
- `books_with_emotions.csv`
- `tagged_description.txt`

You can adjust these in the `path` and `path1` variables near the top of the script.

## ▶️ Run the App

```bash
python gradio_dashboard.py
```

The app will launch in your browser automatically on:  
`http://localhost:7860`
