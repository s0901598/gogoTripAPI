# Pydantic 模型 label
from typing import List
from pydantic import BaseModel


class Room(BaseModel):
    roomid:int
    roomname:str
    roomstatement:str
    roomprice:int
    roomstatus:bool
    roompic:List[str]
    labelid:List[int]


