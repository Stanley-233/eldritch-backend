import uvicorn
from fastapi import FastAPI

from router.auth import auth_router
from router.messenger import messenger_router
from router.user_group import user_group_router
from router.users import users_router
from util.engine import init_db

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(user_group_router)
app.include_router(messenger_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=23353)
