from fastapi import APIRouter, Depends, HTTPException
from models.User import User
from middleware.AuthMiddelware import get_current_user

import psycopg2
from psycopg2.extras import RealDictCursor
import os

AuthRouter = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn