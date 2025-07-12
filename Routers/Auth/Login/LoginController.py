from fastapi import APIRouter, HTTPException
from .LoginReq import LoginRequest
from Database.DataBase import get_db_connection

router = APIRouter(prefix="/auth")

# 登入 API
@router.post("/login/") # domain/auth/login
async def login(request: LoginRequest):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM member WHERE account = %s AND password = %s"  # 使用 phonenumber 作為 password 的比對
            cursor.execute(sql, (request.account, request.password))
            user = cursor.fetchone()
            if user:
                return {"message": "Login successful", "user": user}
            else:
                raise HTTPException(status_code=401, detail="Invalid account or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()