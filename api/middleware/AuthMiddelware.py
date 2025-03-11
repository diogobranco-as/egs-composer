# middleware/AuthMiddleware.py
import os
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from models.User import User

security = HTTPBearer()

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, os.getenv("AUTH0_SECRET"), algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_jwt(token)
    
    user_id = payload.get("sub")
    user_email = payload.get("email")
    user_name = payload.get("name") or user_email

    return User(user_id=user_id, user_email=user_email, user_name=user_name)