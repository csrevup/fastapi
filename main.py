from fastapi import FastAPI
from api_functions import *


app = FastAPI()

@app.get("/person_description")
async def root(name: str):
    return {"response": get_query(name)}

@app.get("/testing")
async def root(request_body: dict = Body(...)):
    return request_body
