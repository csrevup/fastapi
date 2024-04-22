from fastapi import FastAPI

app = FastAPI()

@app.get("/first_test")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}