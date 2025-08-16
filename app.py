from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routers.Auth.Login import LoginController
from Routers.Auth.Register import RegisterController
from Routers.Labels import LabelController
from Routers.Room import RoomController
from Routers.User import UserController

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含各模組的路由
app.include_router(LoginController.router)
app.include_router(RegisterController.router)
app.include_router(UserController.router)
app.include_router(LabelController.router)
app.include_router(RoomController.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}