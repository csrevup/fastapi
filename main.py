from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from api_functions import get_query,piece_sku
from typing import Union, List
import os

app = FastAPI()
token_api=os.environ.get('access_token')
security = HTTPBearer()

class CarPartRequest(BaseModel):
    piece_name: str
    car_brand: str
    car_model: str
    car_year: str


class Part(BaseModel):
    sku: str
    piece_name: str

class Message(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    error: str


##Function token validation
def verify_token(credentials: HTTPAuthorizationCredentials):
    if credentials:
        token = credentials.credentials
        if token == token_api:  # Replace with your method of validating the token
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization required"
    )


@app.get("/car_part_details")
async def submit_car_part(piece_details: CarPartRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return piece_sku(piece_details.piece_name,piece_details.car_brand,piece_details.car_model,piece_details.car_year)



