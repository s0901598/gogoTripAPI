# Pydantic 模型 - 註冊請求
from datetime import date,datetime
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    account: str
    password:str
    gender:bool
    bir: str  # 假設為日期格式，如 "YYYY-MM-DD"
    phonenumber: str
    createtime: datetime = datetime.now()
    isdelete:bool