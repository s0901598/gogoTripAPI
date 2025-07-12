# Pydantic 模型 - Uers 回應請求
from datetime import date, datetime
from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    memberid: int  # 假設 member 表有 id 欄位
    username: str  # 假設 member 表有 name 欄位
    account:str
    password:str
    gender:bool
    bir:date
    phonenumber:str
    createtime:datetime
    isdelete:bool
    # 根據你的 member 表結構新增其他欄位
    class Config:
        from_attributes = True  # 支援從 ORM 或字典轉換

class GetUsersResponse(BaseModel):
    message: str
    users: List[User]

class SearchData(BaseModel):
    username: Optional[str] = ""
    phonenumber: Optional[str] = ""
    isdelete: Optional[bool] = None


# Pydantic 模型 - 封禁請求
class isdelete(BaseModel):
    memberid: int
    isdelete: bool    