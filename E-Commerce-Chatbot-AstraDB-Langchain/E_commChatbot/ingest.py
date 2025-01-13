from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import pandas as pd
from E_commChatbot.data_converter import dataconveter
from exception import CustomException
from logger import logging 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def ingestdata(status):
    try:
        logging.info("Initializing AstraDBVectorStore...")
        vstore = AstraDBVectorStore(
            embedding=embedding,
            collection_name="chatbotECommerce",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
        logging.info("AstraDBVectorStore initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing AstraDBVectorStore: {e}")
        raise CustomException(f"Error initializing AstraDBVectorStore: {e}")

    storage = status

    if storage is None:
        try:
            logging.info("Converting data using dataconveter...")
            docs = dataconveter()
            logging.info(f"Converting data successful, inserting {len(docs)} documents.")
            inserted_ids = vstore.add_documents(docs)
            logging.info(f"{len(inserted_ids)} documents inserted successfully.")
        except Exception as e:
            logging.error(f"Error converting or inserting data: {e}")
            raise CustomException(f"Error converting or inserting data: {e}")
    else:
        logging.info("Returning existing vector store.")
        return vstore

    return vstore, inserted_ids

if __name__ == '__main__':
    try:
        logging.info("Starting the process of ingesting data into AstraDB...")
        vstore, inserted_ids = ingestdata(None)
        logging.info(f"Inserted {len(inserted_ids)} documents.")
        
        logging.info("Performing similarity search...")
        results = vstore.similarity_search("can you tell me the low budget sound basshead.")
        
        logging.info("Displaying search results:")
        for res in results:
            logging.info(f"Result: {res.page_content} [{res.metadata}]")
            print(f"* {res.page_content} [{res.metadata}]")
    except CustomException as ce:
        logging.error(f"CustomException: {ce}")
        print(f"CustomException: {ce}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
