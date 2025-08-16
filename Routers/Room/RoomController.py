

from typing import List
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from typing import Annotated

from Database.DataBase import get_db_connection
from Routers.Room.RoomReq import Room


router = APIRouter(prefix="/room")
    

@router.post('/addroom/')
async def addlabel(files: Annotated[UploadFile, File()],
    roomid: Annotated[int, Form()],
    roomname: Annotated[str, Form()],
    # roomstatement:str= Form(...),
    # roomprice:int= Form(...),
    # roomstatus:bool= Form(...),
    #labelid: List[int] = Form([])
    ):
    connection = None
    try:
        print(files)
        print(roomid)
        # connection = get_db_connection()
        # with connection.cursor() as cursor:
        #     # 插入 room 表
        #     sql_room = "INSERT INTO `room` (roomid, roomname, roomstatement, roomprice, roomstatus) VALUES (%s, %s, %s, %s, %s)"
        #     cursor.execute(sql_room, (request.roomid, request.roomname, request.roomstatement, request.roomprice, request.roomstatus))
            
        #     # 獲取插入的 roomid（如果 roomid 是自增主鍵，則使用 cursor.lastrowid）
        #     inserted_roomid = request.roomid if request.roomid else cursor.lastrowid
            
        #     # 插入 roomspecific 表
            
        #     if hasattr(request, 'labelid'):
        #         for labelid in request.labelid:
        #             sql_specific = "INSERT INTO `roomspecific` (labelid,roomid) VALUES ( %s, %s)"
        #             cursor.execute(sql_specific, ( labelid,inserted_roomid))
            
        #     connection.commit()
        return {
            "message": "roomCreate successful",
            "roomid": 0
        }
            
    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        if connection:
            connection.close()

