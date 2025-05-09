from fastapi import FastAPI

app = FastAPI(title="Interior Design API")

@app.get("/")
async def welcome():
    return {"message": "Interior Design API"}