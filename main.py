from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from api_functions import *
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


class SkuRequest(BaseModel):
    sku_number: str

class ImageUrl(BaseModel):
    image_name: str

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


@app.get("/car_part_sku_exact")
async def submit_car_part(piece_details: CarPartRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return car_part_sku_exact(piece_details.piece_name,piece_details.car_brand,piece_details.car_model,piece_details.car_year)

@app.post("/car_part_sku_similar")
async def submit_car_part(piece_details: CarPartRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return car_part_sku_similar(piece_details.piece_name,piece_details.car_brand,piece_details.car_model,piece_details.car_year)


@app.post("/sku_details")
async def submit_car_part(sku: SkuRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return sku_details(sku.sku_number)

@app.post("/image_url")
async def get_url(image: ImageUrl, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    return get_image_url(image.image_name)



