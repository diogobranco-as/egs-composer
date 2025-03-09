import os
from dotenv import load_dotenv
from fastapi import APIRouter
from models.User import User

AuthRouter = APIRouter(
    prefix = "/auth",
    tags = ["auth"],
)
load_dotenv()