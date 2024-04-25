from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from api_functions import get_query
import os

app = FastAPI()
token_api=os.environ.get('access_token')
security = HTTPBearer()

class Name(BaseModel):
    name: str

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

@app.get("/person_description")
async def root(name: str, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)  # Verify token before processing
    return {"response": get_query(name)}

@app.get("/testing")
async def return_description(name: Name, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)  # Verify token before processing
    return {"description": get_query(name.name)}


@app.get("/piece_details")
async def return_description(name: Name, token: HTTPAuthorizationCredentials = Depends(security)):
    verify_token(token)  # Verify token before processing
    return {"description": get_query(name.name)}