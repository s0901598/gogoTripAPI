
# Pydantic 模型 - 登入請求
from pydantic import BaseModel

class LoginRequest(BaseModel):
    account: str
    password: str