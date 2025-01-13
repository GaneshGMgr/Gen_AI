import os
from dotenv import load_dotenv

from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceTGIGenerator
from haystack_integrations.components.retrievers.pinecone import PineconeEmbeddingRetriever

from QASystem.ingestion import ingest
from QASystem.utility import pinecone_config
