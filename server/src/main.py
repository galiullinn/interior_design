from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth
from src.routers import profile
from src.routers import project

app = FastAPI(title="Interior Design API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(project.router, prefix="/api")

@app.get("/")
async def welcome():
    return {"message": "Interior Design API"}