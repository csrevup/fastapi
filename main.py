from fastapi import FastAPI
from api_functions import *


app = FastAPI()

@app.get("/person_description")
async def root(name: str):
    return {"response": get_query(name)}

