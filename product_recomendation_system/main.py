from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path
import os
from services.auth import router as auth_router
from services.query import router as search_router
from fine_tuned_models.finetune_model_query import router as finetune_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/public"), name="static")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "secret"))

app.include_router(auth_router)
app.include_router(search_router)
app.include_router(finetune_router)

@app.get("/")
async def root():
    index_path = Path("frontend/public/index.html")
    return FileResponse(index_path)


# uvicorn main:app --reload