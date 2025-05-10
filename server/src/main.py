from fastapi import FastAPI
from src.routers import auth
from src.routers import profile

app = FastAPI(title="Interior Design API")

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/")
async def welcome():
    return {"message": "Interior Design API"}