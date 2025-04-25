
# Product Recommendation System

## Overview

This is a product recommendation system that uses semantic search and fine-tuned language models to provide intelligent product recommendations. It includes both authenticated and unauthenticated dashboards with different feature sets.

## Features

- **Semantic Search**: Allows users to perform a quick search based on query semantics.
- **Semantic Search Filtered by Model**: Enhances semantic search with fine-tuned model filtering based on the user's query.
- **Recommended Products Table**
- **Interaction Products Table**

## Model and Fine-tuning

- **Base Model**: [Ollama](https://ollama.com/) using `mistral`.
- **Fine-tuning**: Done using `llama3` on a custom dataset with 4-bit quantization.
  - Fine-tuning code is available inside `experiments/finetune_model.ipynb` (runs perfectly on Google Colab).
  - For local GPU-based execution, use the code from `finetune_model_gpu.py` and paste it into `finetune_model.py`.

## Dataset

- Retail data from Kaggle is used, located in the `data/` folder.

## Search Bar Visibility

| Authentication | Semantic Search | Semantic Search Filter by Model |
|----------------|------------------|----------------------------------|
| Without Auth   | ✅ Visible       | ✅ Visible                        |
| With Auth      | ✅ Visible       | ✅ Hidden by default              |

> To enable filtered search after authentication, replace the function call `retrieve_semantic_recommendations()` with `finetune_product_recommendations()` in the code fine_tuned_models/finetune_model_query.py.

## Authentication Details

- Email: `test@gmail.com`
- Password: `test12`
- You can also sign up with your own account.

## Performance

- **Semantic Search**: Fast
- **Filtered Search (Model-based)**: Performance depends on the device. On low-spec machines, it can take 2-5 minutes.

## Installation

1. Make sure you have `mongodb==2.3.8` installed.
2. Install the Python dependencies:

```
pip install -r requirements.txt
```

## Run the System

Navigate to the `product_recommendation_system/` directory and run:

```
uvicorn main:app --reload
```

Ensure MongoDB is running before launching the server.

---

