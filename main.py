import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.auth import auth_router
from router.messenger import messenger_router
from router.user_group import user_group_router
from router.users import users_router
from util.engine import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(user_group_router)
app.include_router(messenger_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=23353)
