## 🧠 Paper2Podcast: Workflow Overview

> **⚠️ Note:** This project is currently **incomplete** due to some reason. The architecture and pipeline are designed and partially implemented.

This project converts PDF documents into dramatized podcast-style audio using a series of Generative AI models. The full pipeline consists of the following four steps:

---

### 🔹 Step 1: Pre-process PDF
- **Model:** [`Llama-3.2-1B-Instruct`](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)
- **Task:** Extract and clean text from a PDF.
- **Output:** A plain text `.txt` file containing the pre-processed content.

---

### 🔹 Step 2: Transcript Writer
- **Model:** [`Llama-3.1-70B-Instruct`](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct)
- **Task:** Generate a structured podcast transcript from the cleaned text.
- **Output:** A coherent and informative podcast-style script.

---

### 🔹 Step 3: Dramatic Re-Writer
- **Model:** [`Llama-3.1-8B-Instruct`](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)
- **Task:** Enhance the transcript with dramatic tone, emotional cues, and storytelling flair.
- **Output:** A revised, expressive version of the transcript ready for audio synthesis.

---

### 🔹 Step 4: Text-To-Speech Workflow
- **Models:**
  - [`parler-tts/parler-tts-mini-v1`](https://huggingface.co/parler-tts/parler-tts-mini-v1) (Speaker 1)
  - [`suno/bark`](https://huggingface.co/suno/bark) (Speaker 2)
- **Task:** Convert the dramatized transcript into spoken audio using expressive TTS models.
- **Output:** A fully narrated podcast in `.mp3` format, with multi-speaker conversation.

---

## 📚 Resources for Further Learning

Here are some helpful links to understand and explore the technologies used in this project:

- 🔎 [Text-to-Audio Generation with Bark – Clearly Explained](https://betterprogramming.pub/text-to-audio-generation-with-bark-clearly-explained-4ee300a3713a)
- 📔 [Colab: Bark Audio Generation Notebook 1](https://colab.research.google.com/drive/1dWWkZzvu7L9Bunq9zvD-W02RFUXoW-Pd?usp=sharing)
- 📔 [Colab: Bark Audio Generation Notebook 2](https://colab.research.google.com/drive/1eJfA2XUa-mXwdMy7DoYKVYHI1iTd9Vkt?usp=sharing#scrollTo=NyYQ--3YksJY)
- ⚙️ [Replicate: Bark Prediction Example](https://replicate.com/suno-ai/bark?prediction=zh8j6yddxxrge0cjp9asgzd534)
- 🧾 [Suno AI Bark Documentation (Notion)](https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c)
