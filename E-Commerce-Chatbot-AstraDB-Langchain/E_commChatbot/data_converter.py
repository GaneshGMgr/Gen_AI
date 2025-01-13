import pandas as pd
from langchain_core.documents import Document
import os
from logger import logging
from exception import CustomException
def dataconveter():
    try:
        logging.info("Loading product data from CSV...")
        file_path = os.path.join(os.getcwd(), "../data/flipkart_product_review.csv")
        product_data = pd.read_csv(file_path)
        logging.info("CSV loaded successfully.")

        required_columns = ["product_title", "rating", "summary", "review"]
        if not all(col in product_data.columns for col in required_columns):
            logging.error(f"Missing required columns in the CSV: {required_columns}")
            raise ValueError(f"Missing required columns in the CSV: {required_columns}")

        data = product_data[required_columns]
        
        product_list = []
        for index, row in data.iterrows():
            obj = {
                'product_name': row['product_title'],
                'rating': row['rating'],
                'summary': row['summary'],
                'review': row['review']
            }
            product_list.append(obj)
        
        docs = []
        for entry in product_list:
            metadata = {
                "product_name": entry['product_name'],
                "rating": entry.get('rating', 'N/A'),
                "summary": entry.get('summary', 'No summary available')
            }
        
            doc = Document(page_content=entry['review'], metadata=metadata)
            docs.append(doc)
        
        logging.info(f"Converted {len(docs)} documents successfully.")
        return docs

    except Exception as e:
        logging.error(f"Error in data conversion: {e}")
        raise CustomException(f"Error in data conversion: {e}")
