from fastapi import FastAPI
from src.routers import auth
from src.routers import profile
from src.routers import project

app = FastAPI(title="Interior Design API")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(project.router)

@app.get("/")
async def welcome():
    return {"message": "Interior Design API"}