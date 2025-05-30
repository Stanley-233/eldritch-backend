import uvicorn
from fastapi import FastAPI
from util.engine import init_db
from router.auth import auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=23353)
