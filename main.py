from fastapi import FastAPI
from api_functions import *
import uvicorn


app = FastAPI()

@app.get("/person_description")
async def root(name: str):
    return {"response": {name}}

