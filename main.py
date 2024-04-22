from fastapi import FastAPI
from api_functions import *


app = FastAPI()

@app.get("/first_test_api")
async def root():
    return {"greeting": test(), "message": "Welcome to FastAPI!"}