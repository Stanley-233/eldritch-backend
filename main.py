import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoginRequest(BaseModel):
    username : str = None
    password : str = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(request: LoginRequest):
    return request

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
