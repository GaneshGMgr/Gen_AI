# import pandas as pd
# import re
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from services.prompt import ProductRecommendationPrompt
# import yaml
# import os
# from dotenv import load_dotenv

# load_dotenv()
# HF_TOKEN = os.getenv("HF_TOKEN")


# products_path = r"C:\Users\ganes\DataScience\Gen_AI\LangChain\Course_GenAI\Gen_AI_In-Depth\product_recomendation_system\experiments\filtered_products.csv"
# faiss_path = r"C:\Users\ganes\DataScience\Gen_AI\LangChain\Course_GenAI\Gen_AI_In-Depth\product_recomendation_system\experiments\faiss_index_dir"
# finetune_model_path = r"C:\Users\ganes\DataScience\Gen_AI\LangChain\Course_GenAI\Gen_AI_In-Depth\product_recomendation_system\fine_tuned_models\llama2_finetuned"

# product_data = pd.read_csv(products_path)

# # Load model
# model = AutoModelForCausalLM.from_pretrained(
#     finetune_model_path,
#     device_map="auto",
#     low_cpu_mem_usage=True
# )

# tokenizer = AutoTokenizer.from_pretrained(finetune_model_path, use_auth_token=HF_TOKEN)
# tokenizer.pad_token = tokenizer.eos_token

# llm_pipeline = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=256
# )

# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"  # Smaller/faster model
# )

# db_products = FAISS.load_local(
#     faiss_path,
#     embeddings=embedding_model,
#     allow_dangerous_deserialization=True
# )

# prompt = ChatPromptTemplate.from_template(ProductRecommendationPrompt.PRODUCT_RECOMMENDATION_PROMPT)


# def retrieve_semantic_recommendations(query: str, top_k: int = 7) -> dict:
#     """Returns results in standardized nested format"""
#     results = db_products.similarity_search(query, k=top_k)
#     indices = [doc.metadata["index"] for doc in results]
#     df = product_data.iloc[indices]

#     recommendations = {
#         "products": {},
#         "product_description": {},
#         "Product_Brand": {},
#         "Product_Category": {},
#         "Product_Type": {},
#         "Ratings": {},
#         "Feedback": {},
#         "Amount": {},
#         "enhanced_description": {}
#     }
    
#     for idx, row in df.iterrows():
#         pid = str(idx)
#         recommendations["products"][pid] = row.get("products", "")
#         recommendations["product_description"][pid] = row.get("product_description", "")
#         recommendations["Product_Brand"][pid] = row.get("Product_Brand", "")
#         recommendations["Product_Category"][pid] = row.get("Product_Category", "")
#         recommendations["Product_Type"][pid] = row.get("Product_Type", "")
#         recommendations["Ratings"][pid] = row.get("Ratings", "")
#         recommendations["Feedback"][pid] = row.get("Feedback", "")
#         recommendations["Amount"][pid] = row.get("Amount", "")
#         recommendations["enhanced_description"][pid] = row.get("enhanced_description", "")
    
#     return recommendations

# def finetune_product_recommendations(query: str, top_k: int = 5) -> pd.DataFrame:
#     recommendations = retrieve_semantic_recommendations(query, top_k=top_k)

#     products_text = ""
#     for _, row in recommendations.iterrows():
#         products_text += f"""
# - product_description: {row['product_description']}
#   enhanced_description: {row['enhanced_description']}
#   Product_Category: {row['Product_Category']}
#   Product_Brand: {row['Product_Brand']}
#   Product_Type: {row['Product_Type']}
#   Feedback: {row['Feedback']}
#   Ratings: {row['Ratings']}
#   products: {row['products']}
#   Amount: {row['Amount']}
# """
#     response = llm_pipeline(
#         ProductRecommendationPrompt.PRODUCT_RECOMMENDATION_PROMPT.format(
#             query=query,
#             products=products_text
#         ),
#         max_new_tokens=128
#     )
#     response_content = getattr(response, "content", response)


#     lines = response_content.split("\n")
#     structured_lines = [
#         line for line in lines
#         if line.strip().startswith("- product_id:") or line.strip().startswith((
#             "product_id:", "Product:", "Customer feedback:", "Products:", "Amount:",
#             "product_description:", "Product_Brand:", "Product_Category:",
#             "Product_Type:", "Ratings:", "Feedback:", "enhanced_description:"
#         ))
#     ]

#     final_yaml = ""
#     current_block = []
#     for line in structured_lines:
#         if line.strip().startswith("- product_id:"):
#             if current_block:
#                 final_yaml += "\n".join(current_block) + "\n"
#             current_block = [line]
#         else:
#             current_block.append("  " + line.strip())
#     if current_block:
#         final_yaml += "\n".join(current_block)

#     # print("structured YAML to parse:\n", final_yaml)

#     def quote_yaml_values(line: str) -> str:
#         match = re.match(r"^( *)([^:]+):(.*)$", line)
#         if match:
#             indent, key, value = match.groups()
#             value = value.strip()
#             if (":" in value or '"' in value or "'" in value or not value.replace('.', '', 1).isdigit()):
#                 value = f'"{value}"'
#             return f"{indent}{key}: {value}"
#         return line

#     final_yaml_quoted = "\n".join([quote_yaml_values(line) for line in final_yaml.split("\n")])

#     try:
#         parsed_response = yaml.safe_load(final_yaml_quoted)
#     except yaml.YAMLError as e:
#         print("YAML parsing error:", e)
#         parsed_response = []

#     if not parsed_response:
#         print("Parsed response is empty. Returning default empty structure.")
#         return {}

#     recommendations = {
#         "products": {},
#         "product_description": {},
#         "Product_Brand": {},
#         "Product_Category": {},
#         "Product_Type": {},
#         "Ratings": {},
#         "Feedback": {},
#         "Amount": {},
#         "enhanced_description": {}
#     }

#     for item in parsed_response:
#         pid = str(item.get("product_id", ""))
#         recommendations["products"][pid] = item.get("products", "")
#         recommendations["product_description"][pid] = item.get("product_description", "")
#         recommendations["Product_Brand"][pid] = item.get("Product_Brand", "")
#         recommendations["Product_Category"][pid] = item.get("Product_Category", "")
#         recommendations["Product_Type"][pid] = item.get("Product_Type", "")
#         recommendations["Ratings"][pid] = item.get("Ratings", "")
#         recommendations["Feedback"][pid] = item.get("Feedback", "")
#         recommendations["Amount"][pid] = item.get("Amount", "")
#         recommendations["enhanced_description"][pid] = item.get("enhanced_description", "")

#     # print("return product: ", recommendations)
#     return recommendations