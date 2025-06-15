from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from fastapi.middleware.cors import CORSMiddleware  # 新增這行

app=FastAPI()

# 添加以下 CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源（正式環境建議指定具體域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)

# 資料庫配置
db_config = {
    "host": "gogotrip.cz0q8ge8ovxl.ap-northeast-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "Aa71933281007",  # 替換為您的實際密碼
    "database": "gogotrip"
}

# 測試連接
try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    if result[0] == 1:
        print("Database connection is successful!")
    cursor.close()
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")



# Pydantic 模型 - 註冊請求
class RegisterRequest(BaseModel):
    username: str
    account: str
    password:str
    gender:bool
    bir: str  # 假設為日期格式，如 "YYYY-MM-DD"
    phonenumber: str
    createtime: datetime = datetime.now()
    isdelete:bool

# Pydantic 模型 - 登入請求
class LoginRequest(BaseModel):
    account: str
    password: str

# 資料庫連線函數
def get_db_connection():
    return pymysql.connect(**db_config)

# 註冊 API
@app.post("/register/")
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

# 登入 API
@app.post("/login/")
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

# 測試用端點
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}