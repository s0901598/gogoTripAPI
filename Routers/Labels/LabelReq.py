# Pydantic 模型 label
from pydantic import BaseModel

class Label(BaseModel):
    labelid:int
    specificname:str