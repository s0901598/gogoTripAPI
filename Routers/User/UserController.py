#取得使用者
from fastapi import APIRouter, HTTPException
import pymysql
from Database.DataBase import get_db_connection
from Routers.User.UserReq import GetUsersResponse, SearchData, User, isdelete

router = APIRouter(prefix="/user")

#用戶查詢
@router.post("/getusers/", response_model=GetUsersResponse)
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




# 更新 isdelete 狀態的 API
@router.put('/updateuserstatus')
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