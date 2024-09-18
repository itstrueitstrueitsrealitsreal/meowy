from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")  # Include your API routes
