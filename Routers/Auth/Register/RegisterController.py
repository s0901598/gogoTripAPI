# 註冊 API
from fastapi import APIRouter, HTTPException
from Database.DataBase import get_db_connection
from Routers.Auth.Register.RegisterReq import RegisterRequest

router = APIRouter(prefix="/auth")

@router.post("/register/")
async def register(request: RegisterRequest):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO member (username, account,password,gender,bir, phonenumber, createtime,isdelete)
                VALUES (%s, %s, %s, %s, %s,%s,%s,%s)
            """
            cursor.execute(sql, (request.username, request.account,request.password,request.gender, request.bir,request.phonenumber, request.createtime,request.isdelete))
            connection.commit()
        connection.close()
        return {"message": "Registration successful", "memberid": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))