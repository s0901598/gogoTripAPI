from datetime import date, datetime
from typing import List, Optional
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

# Pydantic 模型 - 封禁請求
class isdelete(BaseModel):
    memberid: int
    isdelete: bool    

## Pydantic 模型 label
class Label(BaseModel):
    labelid:int
    specificname:str


# Pydantic 模型 - Uers 回應請求
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

class SearchData(BaseModel):
    username: Optional[str] = ""
    phonenumber: Optional[str] = ""
    isdelete: Optional[bool] = None

class GetUsersResponse(BaseModel):
    message: str
    users: List[User]

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
#取得使用者
@app.post("/getusers/", response_model=GetUsersResponse)
async def getusers(search: SearchData):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 基礎 SQL 查詢
            sql = """
            SELECT memberid, username, account, password, gender, 
                   NULLIF(bir, '0000-00-00') AS bir, 
                   phonenumber, createtime, isdelete 
            FROM member
            WHERE 1=1
            """
            params = []

            # 動態添加查詢條件
            if search.username:
                sql += " AND username LIKE %s"
                params.append(f"%{search.username}%")
            if search.phonenumber:
                sql += " AND phonenumber LIKE %s"
                params.append(f"%{search.phonenumber}%")
            if search.isdelete is not None:
                sql += " AND isdelete = %s"
                params.append(search.isdelete)

            cursor.execute(sql,params)
            columns = [col[0] for col in cursor.description]  # 獲取欄位名稱
            users = cursor.fetchall()
            if users:
                user_list = [User(**dict(zip(columns, user))) for user in users]
                print(user_list)
                return {"message": "getuser successful", "users": user_list}
            else:
                return {"message": "getuser successful", "users": []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()
#標籤新增
@app.post('/addlabel/')
async def addlabel(request: Label):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `specific` (labelid,specificname)VALUES(%s,%s)" 
            cursor.execute(sql, (request.labelid, request.specificname))
            connection.commit()
            connection.close()
            return {"message": "LabalCreate successful", "memberid": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 標籤刪除 API
@app.delete('/deletelabel/{labelid}')
async def deletelabel(labelid: int):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 檢查標籤是否存在
            check_sql = "SELECT labelid FROM `specific` WHERE labelid = %s"
            cursor.execute(check_sql, (labelid,))
            existing_label = cursor.fetchone()

            if not existing_label:
                connection.close()
                raise HTTPException(status_code=404, detail="標籤不存在")

            # 執行刪除操作
            delete_sql = "DELETE FROM `specific` WHERE labelid = %s"
            cursor.execute(delete_sql, (labelid,))
            connection.commit()
            connection.close()

            return {"message": "標籤刪除成功"}
    except pymysql.Error as e:
        connection.close()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail="服務器錯誤，請稍後再試")

#標籤查詢
@app.get("/getlabel/")
async def label():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * from `specific`"  
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]  # 獲取欄位名稱
            labels = cursor.fetchall()
            if labels:
                labels_list = [Label(**dict(zip(columns, label))) for label in labels]
                print(labels_list)
                return {"message": "getlabels successful", "labels": labels_list}
            else:
                raise HTTPException(status_code=401, detail="Invalid account or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        connection.close()

# 更新 isdelete 狀態的 API
@app.put('/updateuserstatus')
async def update_user_status(request:isdelete):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 檢查用戶是否存在
            check_sql = "SELECT memberid FROM member WHERE memberid = %s"
            cursor.execute(check_sql, (request.memberid))
            existing_user = cursor.fetchone()

            if not existing_user:
                connection.close()
                raise HTTPException(status_code=404, detail="用戶不存在")

            # 更新 isdelete 狀態
            update_sql = "UPDATE member SET isdelete = %s WHERE memberid = %s"
            cursor.execute(update_sql, (request.isdelete, request.memberid))
            connection.commit()
            connection.close()

            return {"message": "用戶狀態更新成功", "memberid": request.memberid, "isdelete": request.isdelete}
    except pymysql.Error as e:
        connection.close()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        connection.close()
        raise HTTPException(status_code=500, detail="服務器錯誤，請稍後再試")

# 測試用端點
@app.get("/")
async def root():
    return {"message": "Welcome to the API"}