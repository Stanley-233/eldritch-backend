import uvicorn
from fastapi import FastAPI
from util.engine import init_db

from router.users import users_router
from router.auth import auth_router
from router.user_group import user_group_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(user_group_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=23353)
