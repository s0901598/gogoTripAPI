#標籤新增
from fastapi import APIRouter, HTTPException
import pymysql
from Database.DataBase import get_db_connection
from .LabelReq import Label

router=APIRouter(prefix="/label")

@router.post('/addlabel/')
async def addlabel(request:Label):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `specific` (labelid,specificname,iconname)VALUES(%s,%s,%s)" 
            cursor.execute(sql, (request.labelid, request.specificname,request.iconname))
            connection.commit()
            connection.close()
            return {"message": "LabalCreate successful", "memberid": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# 標籤刪除 API
@router.delete('/deletelabel/{labelid}')
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
@router.get("/getlabel/")
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

