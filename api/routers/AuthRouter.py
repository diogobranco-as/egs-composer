import os
from dotenv import load_dotenv
from fastapi import APIRouter
from models.User import User
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

AuthRouter = APIRouter(
    prefix = "/auth",
    tags = ["auth"],
)

#Database connection
def get_db_connection():
    con = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return con

@AuthRouter.get("/users")
async def get_users():
    try:
        #connect to db
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()

        #commit and close connection
        conn.commit()
        cur.close()
        conn.close()

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@AuthRouter.post("/signup")
async def signup(user: User):
    try:
        #connect to db
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

         # Check if the user already exists
        cur.execute('SELECT * FROM users WHERE user_id = %s;', (user.user_id,))
        existing_user = cur.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        #Insert user to db
        cur.execute("INSERT INTO users (user_id, user_name, user_email) VALUES (%s, %s, %s) RETURNING *;",
                    (user.user_id, user.user_name, user.user_email)
        )
        user_data = cur.fetchone()

        #commit and close connection
        conn.commit()
        cur.close()
        conn.close()

        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))