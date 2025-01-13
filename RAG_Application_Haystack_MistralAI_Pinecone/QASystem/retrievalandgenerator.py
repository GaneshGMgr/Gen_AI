import os
from dotenv import load_dotenv

from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
# from haystack.components.generators import HuggingFaceTGIGenerator
from haystack_integrations.components.retrievers.pinecone import PineconeEmbeddingRetriever
from QASystem.ingestion import ingest
from QASystem.utility import pinecone_config

load_dotenv()
hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

prompt_template = """Answer the following query based on the provided context. If the context does
                     not include an answer, reply with 'I don't know'.\n
                     Query: {{query}}
                     Documents:
                     {% for doc in documents %}
                        {{ doc.content }}
                     {% endfor %}
                     Answer: 
                  """
 
def get_result(query):                  
    query_pipeline = Pipeline()
    generator = pinecone_config()

    query_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder())
    query_pipeline.add_component("retriever", PineconeEmbeddingRetriever(document_store=generator))
    query_pipeline.add_component("prompt_builder", PromptBuilder(template=prompt_template))
    # query_pipeline.add_component("llm", HuggingFaceTGIGenerator(model="mistralai/Mistral-7B-v0.1", token=Secret.from_token(hf_api_token)))
    query_pipeline.add_component("llm", HuggingFaceAPIGenerator(api_type="serverless_inference_api", api_params={"model": "mistralai/Mistral-7B-v0.1"}, token=Secret.from_token(hf_api_token)))


    query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    query_pipeline.connect("retriever.documents", "prompt_builder.documents")
    query_pipeline.connect("prompt_builder", "llm")


    results = query_pipeline.run(
        {
            "text_embedder": {"text": query}, #  feeds the user's query (query) into the text embedder component.
            "prompt_builder": {"query": query}, # passes the user's query (query) to the prompt builder component
        }
    )

    return results['llm']['replies'][0]

if __name__ == '__main__':
    result=get_result("what is rag?")
    print(result)