import pymysql

db_config = {
    "host": "gogotrip.cz0q8ge8ovxl.ap-northeast-1.rds.amazonaws.com",
    "port": 3306,
    "user": "admin",
    "password": "Aa71933281007",
    "database": "gogotrip"
}

def get_db_connection():
    return pymysql.connect(**db_config)