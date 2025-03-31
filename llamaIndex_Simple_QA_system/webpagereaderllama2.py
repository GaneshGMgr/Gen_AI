# from llama_index.llms.openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# print(hf_token)

def main(url: str) -> None:
    document = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    # print("Documents: ", document)

    embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

    index = VectorStoreIndex.from_documents(documents=document, embed_model=embed_model)

    # Hugging Face Llama 2 model
    model_name = "meta-llama/Llama-2-7b-hf"
    model_name1 = "meta-llama/Llama-2-7b"
    model_name2 = "meta-llama/Llama-2-7b-chat"

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
    # tokenizer = LlamaTokenizer.from_pretrained(model_name, token=hf_token) # if not use model_name but use model_name1
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        token=hf_token,  # API token for authentication
        device_map="auto",  # Automatically either GPU or CPU
    )

    print("Model:", model)

    # Use the Hugging Face model with LlamaIndex
    llama_model = HuggingFaceLLM(model=model, tokenizer=tokenizer)
    print("llama_model: ", llama_model)
    query_engine = index.as_query_engine(llm=llama_model)

    response = query_engine.query("What are agents?")
    print(response)

if __name__ == "__main__":
    main(url="https://docs.llamaindex.ai/en/stable/")