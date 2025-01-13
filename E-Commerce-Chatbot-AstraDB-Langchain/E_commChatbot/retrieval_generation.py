from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from E_commChatbot.ingest import ingestdata
from exception import CustomException
from logger import logging

# Product recommendation chatbot prompt
PRODUCT_BOT_TEMPLATE = """
You are an expert ecommerce bot that assists customers with product-related queries and recommendations. 
You analyze product details, reviews, and ratings to provide accurate and helpful responses.

Your responses should focus on the following:
1. **Product Title**: The name of the product.
2. **Product Rating**: General user satisfaction with the product.
3. **Product Summary**: Brief overview of the product's main features or key selling points.
4. **Product Reviews**: Insights from customer feedback on the product.

Ensure your answers are concise, informative, and directly related to the context provided. Avoid generic responses and focus on the specific product details from the context.

CONTEXT:
{context}

QUESTION: {question}

YOUR ANSWER:
"""

def generate_chain(vstore):
    """Generates the chain for product recommendation based on the retriever and prompt."""
    try:
        logging.info("Creating retriever...")
        retriever = vstore.as_retriever(search_kwargs={"k": 3})
        logging.info("Retriever created successfully.")
    except Exception as e:
        logging.error(f"Error while creating retriever: {str(e)}")
        raise CustomException(f"Error while creating retriever: {str(e)}")

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    try:
        logging.info("Initializing the LLM...")
        llm = ChatOpenAI()
        logging.info("LLM initialized successfully.")
    except Exception as e:
        logging.error(f"Error while initializing the LLM: {str(e)}")
        raise CustomException(f"Error while initializing the LLM: {str(e)}")

    # Build the chain: retrieve, prompt, model, and output parser
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

def main():
    """Main entry point for generating product recommendations."""
    try:
        logging.info("Starting the process of product recommendation...")
        vstore = ingestdata("done")  # Get the vector store
        logging.info("Data ingestion completed.")
        
        chain = generate_chain(vstore)  # Generate the chain for Q&A
        logging.info("Chain generation successful.")
        
        result = chain.invoke("Can you tell me the best Bluetooth buds?")
        logging.info(f"Result: {result}")
        
        print(f"Answer: {result}")
    except CustomException as e:
        logging.error(f"CustomException occurred: {e}")
        print(f"CustomException occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
