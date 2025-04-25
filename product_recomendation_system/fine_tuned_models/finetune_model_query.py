from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from database.db import PyObjectId
from pydantic import BaseModel, Field
from fine_tuned_models.finetune_model import finetune_product_recommendations, retrieve_semantic_recommendations
from database.db import Product
from database.db import UserInteraction
from pymongo import ASCENDING
import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI is not set in the environment variables.")
client = AsyncIOMotorClient(mongo_uri)

db = client.product_recommend

class SearchInput(BaseModel):
    query: str

@router.post("/search/finetune")
async def finetune_search(request: Request, search: SearchInput):
    query = search.query
    user_email = request.session.get("user")

    try:
        recommendations = retrieve_semantic_recommendations(query)
        # print("recommendations data: ", recommendations)

        if not isinstance(recommendations, list):
            if isinstance(recommendations, dict):
                recommendations = [recommendations]
            else:
                recommendations = [{"result": recommendations}]

        save_result = await save_recommended_products(db, recommendations)

        return {
            "query": query,
            "user": user_email,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing finetune search: {str(e)}"
        )
    

# recommendation product save
async def save_recommended_products(db: AsyncIOMotorDatabase, recommendations: list) -> dict:
    saved_products = []

    for recommendation in recommendations:
        products = recommendation.get("products", {})
        product_description = recommendation.get("product_description", {})
        product_brand = recommendation.get("Product_Brand", {})
        product_category = recommendation.get("Product_Category", {})
        product_type = recommendation.get("Product_Type", {})

        for product_id in products:
            try:
                product_data = {
                    "Product_Category": product_category.get(product_id, "Unknown"),
                    "Product_Brand": product_brand.get(product_id, "Unknown"),
                    "Product_Type": product_type.get(product_id, "Unknown"),
                    "products_Name": products.get(product_id, "Unnamed Product"),
                    "product_description": json.dumps(product_description.get(product_id, "No description available"))
                }
                # print("Saving Data: ", product_data)

                # Check if the product already exists with the same combination of fields
                existing_product = await db.products.find_one({
                    "products_Name": product_data["products_Name"],
                    "Product_Category": product_data["Product_Category"],
                    "Product_Brand": product_data["Product_Brand"],
                    "Product_Type": product_data["Product_Type"],
                    "product_description": product_data["product_description"]
                })

                if existing_product:
                    print(f"Product already exists with the same details: {product_data['products_Name']}")
                else:
                    product = Product(**product_data)
                    await db.products.insert_one(product.dict(by_alias=True))
                    saved_products.append(product_data)

            except Exception as e:
                print(f"Failed to insert product {product_id}: {e}")

    return {
        "message": f"{len(saved_products)} product(s) saved successfully.",
        "saved_products": saved_products
    }

# recommendation product fetch
@router.get("/api/get_recommended_products")
async def get_recommended_products():
    try:
        products = await db.products.find().to_list(length=100)  # Fetch first 100 products
        product_list = [{
            "Product_Category": product["Product_Category"],
            "Product_Brand": product["Product_Brand"],
            "Product_Type": product["Product_Type"],
            "products_Name": product["products_Name"],
            "product_description": product["product_description"]
        } for product in products]
        # print("products: ", product_list)

        return {"products": product_list}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


# user interaction save
async def get_user_id_by_email(request: Request):
    user_email = request.session.get("user")
    if not user_email:
        raise HTTPException(status_code=401, detail="User not authenticated")
    user = await db["users"].find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user["_id"]

@router.post("/interact")
async def record_interaction(request: Request, interaction: dict):
    try:
        product_name = interaction.get("product")
        product_category = interaction.get("category")
        product_brand = interaction.get("brand")
        product_type = interaction.get("type")
        product_description = interaction.get("description")
        interaction_type = interaction.get("interaction_type")

        if not all([product_name, product_category, product_brand, product_type, product_description, interaction_type]):
            return JSONResponse(status_code=400, content={"error": "Missing required fields"})

        user_id = await get_user_id_by_email(request)

        # print(f"Incoming data:: name: {product_name}, category: {product_category}, brand: {product_brand}, type: {product_type}, description: {product_description}")

        # Query the database for the product
        quoted_description = f'"{product_description.strip()}"'
        product = await db.products.find_one({
            "products_Name": product_name,
            "Product_Category": product_category,
            "Product_Brand": product_brand,
            "Product_Type": product_type,
            "product_description": quoted_description
        })

        if not product:
            return JSONResponse(status_code=404, content={"error": "Product not found"})

        product_id = product["_id"]

        # Record the interaction
        new_interaction = UserInteraction(
            user_id=user_id,
            product_id=product_id,
            interaction_type=interaction_type
        )
        # print("New interaction to insert:", new_interaction.dict(by_alias=True))

        await db["user_interactions"].insert_one(new_interaction.dict(by_alias=True))

        return {"status": "success", "product_id": str(product_id)}

    except Exception as e:
        print(f"Error during interaction: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


# interaction product fetch
@router.get("/api/get_interaction_products")
async def get_interaction_products():
    try:
        interactions = await db.user_interactions.find().to_list(length=100)

        result = []

        for interaction in interactions:
            user = await db.users.find_one({"_id": interaction["user_id"]})
            product = await db.products.find_one({"_id": interaction["product_id"]})

            # print(f"Interaction: {interaction}")

            if user and product:
                result.append({
                    "user_name": user["email"],
                    "products_Name": product["products_Name"],
                    "Product_Category": product["Product_Category"],
                    "Product_Brand": product["Product_Brand"],
                    "Product_Type": product["Product_Type"],
                    "product_description": product["product_description"],
                    "interaction_type": interaction.get("interaction_type", "N/A")
                })

        return {"products": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching interaction products: {str(e)}")


async def delete_user_and_related_data(user_id: PyObjectId):
    await db.user_interactions.delete_many({"user_id": user_id})
    await db.users.delete_one({"_id": user_id})

async def delete_product_and_related_data(product_id: PyObjectId):
    await db.user_interactions.delete_many({"product_id": product_id})
    await db.products.delete_one({"_id": product_id})
