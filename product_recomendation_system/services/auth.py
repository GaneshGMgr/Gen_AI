from fastapi import APIRouter, HTTPException, status, Request, Response, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()

router = APIRouter()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.product_recommend
users_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/signup")
async def signup(user: SignupRequest):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = {
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "created_at": datetime.now(timezone.utc)
    }

    result = await users_collection.insert_one(new_user)

    if result.inserted_id:
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user")


@router.post("/login")
async def login(request: Request, response: Response, credentials: LoginRequest):
    user = await users_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    request.session["user"] = credentials.email

    response.set_cookie(
        key="session_token",
        value=str(user["_id"]),
        httponly=True,
        max_age=3600,
        secure=False,
        samesite="lax"
    )

    return {"message": "Login successful"}


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="session_token")
    return response


async def get_current_user(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        user = await users_collection.find_one({"_id": ObjectId(session_token)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid session token")


@router.get("/me")
async def read_current_user(request: Request):
    user_email = request.session.get("user")
    if not user_email:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    return {"email": user_email}
