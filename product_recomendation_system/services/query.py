from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from .model import get_product_recommendations, retrieve_semantic_recommendations
from .utils import create_empty_recommendation

router = APIRouter()

class SearchInput(BaseModel):
    query: str
    type: str  # "normal" or "semantic"



@router.post("/search")
async def search_products(request: Request, search: SearchInput):
    try:
        recommendations = (
            retrieve_semantic_recommendations(search.query)
            if search.type == "semantic"
            else get_product_recommendations(search.query)
        )

        return {
            "query": search.query,
            "type": search.type,
            "user": request.session.get("user"),
            "recommendations": [recommendations]
        }
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        return {
            "query": search.query,
            "type": search.type,
            "user": request.session.get("user"),
            "recommendations": [create_empty_recommendation()]
        }





# query = "wireless bluetooth earphones" ""Lenovo Tab
# refined_recommendations = get_product_recommendations(query)
# # sementic_recommendations = retrieve_semantic_recommendations(query)
# if not refined_recommendations.empty:
#     print(refined_recommendations.to_string(index=False))
# else:
#     print("No recommendations found.")

# query = "i want Comfortable running shorts for men under the price 806.707815, can you please provide me 2 options?  if you not find any products then you can provide me closely related other products also?"
# refined_recommendations = get_product_recommendations(query)
# refined_recommendations