from fastapi import FastAPI
from api_functions import *
from pydantic import BaseModel

class Name(BaseModel):
    name: str

app = FastAPI()

@app.get("/person_description")
async def root(name: str):
    return {"response": get_query(name)}

@app.get("/testing")
async def return_description(name: Name):
    return name.name
