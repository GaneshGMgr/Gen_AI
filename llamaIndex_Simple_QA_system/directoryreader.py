from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def main(url: str) -> None:
    document = SimpleDirectoryReader(url).load_data()
    # print("Document DirectoryReader: ", document)
    index = VectorStoreIndex.from_documents(documents=document)
    query_engine = index.as_query_engine()
    response = query_engine.query("What are the planets in the Solar System in order of their distance from the Sun?")
    print("Response:", response)

if __name__ == "__main__":
    main(url=r"C:\Users\ganes\DataScience\Gen_AI\LangChain\Course_GenAI\Gen_AI_In-Depth\llamaIndexProject\data")
