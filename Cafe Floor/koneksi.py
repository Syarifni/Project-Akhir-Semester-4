import mysql.connector

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cafe_floor"
        )
        return conn
    except mysql.connector.Error as err:
        raise err