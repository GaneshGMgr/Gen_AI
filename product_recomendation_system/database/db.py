from pydantic import BaseModel, Field, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic_core import core_schema
from typing import Optional
from enum import Enum
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, _info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler):
        return {"type": "string"}

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Product(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    Product_Category: str
    Product_Brand: str
    Product_Type: str
    products_Name: str
    product_description: str

class InteractionType(str, Enum):
    click = "click"
    like = "like"
    dislike = "dislike"

class UserInteraction(BaseModel):
    user_id: PyObjectId
    product_id: PyObjectId
    interaction_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

async def create_collections():
    # Connect with authentication
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client.product_recommend

    collections = ["users", "products", "user_interactions"]
    for collection in collections:
        try:
            await db.create_collection(collection)
        except Exception:
            pass  # Collection already exists

    await db.users.create_index("email", unique=True)
    await db.user_interactions.create_index([("user_id", 1), ("product_id", 1)])

async def main():
    await create_collections()

if __name__ == "__main__":
    asyncio.run(main())