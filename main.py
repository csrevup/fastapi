from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from api_functions import get_query,piece_sku
import os

app = FastAPI()
token_api=os.environ.get('access_token')
security = HTTPBearer()

class Name(BaseModel):
    name: str

class CarPartRequest(BaseModel):
    piece_name: str
    car_brand: str
    car_model: str
    car_year: str


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




##API endpoints
@app.get("/person_description")
async def root(name: str, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)  # Verify token before processing
    return {"response": get_query(name)}

@app.get("/testing")
async def return_description(name: Name, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)  # Verify token before processing
    return {"description": get_query(name.name)}


@app.get("/car_part_details")
async def submit_car_part(piece_details: CarPartRequest, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)
    ##return {piece_sku(piece_details.piece_name,piece_details.car_brand,piece_details.car_model,piece_details.car_year)}


    ##test_var = "select DAI FROM vehicle_parts WHERE brand_idf = "+piece_details.car_brand+" and model_idf="+piece_details.car_model+" and year=2021 and line="+piece_details.piece_name
    return {"hola":piece_sku(piece_details.piece_name,piece_details.car_brand,piece_details.car_model,piece_details.car_year)}
    ##return {"hola":test_var}



