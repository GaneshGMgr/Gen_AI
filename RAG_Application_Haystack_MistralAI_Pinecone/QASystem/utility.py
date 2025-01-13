import os
from dotenv import load_dotenv
from haystack.utils import Secret
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def pinecone_config():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    index_name = "default"
    namespace_name = "default"
    existing_indexes = pc.list_indexes()
    
    if index_name not in existing_indexes:  # Check if the index exists
        print(f"Index '{index_name}' not found. Creating new index...")
        try:
            pc.create_index(
                name=index_name,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1",
                ),
            )
        except Exception as e:
            if 'ALREADY_EXISTS' in str(e):
                print(f"Index '{index_name}' already exists, skipping creation.")
            else:
                print(f"Error creating index: {e}")
                raise
    else:
        print(f"Index '{index_name}' already exists. Skipping creation.")

    document_store = PineconeDocumentStore(
        index=index_name,
        namespace=namespace_name,
        dimension=768,
        metric="cosine",
  	    spec={"serverless": {"region": "us-east-1", "cloud": "aws"}}
    )

    return document_store
