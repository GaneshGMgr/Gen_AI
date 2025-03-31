from llama_index.llms.openai import OpenAI
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex
import llama_index
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# print(hf_token)

def main(url: str) -> None:
    document = SimpleWebPageReader(html_to_text=True).load_data(urls=[url])
    # print("Document WebPageReader: ", document)
    index = VectorStoreIndex.from_documents(documents=document)
    query_engine = index.as_query_engine()
    response = query_engine.query("What are Agents?")
    print("Response:", response)

if __name__ == "__main__":
    main(url="https://docs.llamaindex.ai/en/stable/")
