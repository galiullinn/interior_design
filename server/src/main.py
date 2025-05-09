from fastapi import FastAPI
from src.routers import auth

app = FastAPI(title="Interior Design API")

app.include_router(auth.router)

@app.get("/")
async def welcome():
    return {"message": "Interior Design API"}