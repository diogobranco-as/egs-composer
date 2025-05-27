# api/routers/UserRouter.py

import os
import psycopg2
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, UUID4
from typing import Optional
from middleware.AuthMiddleware import verify_token  # <— import the raw verifier

UserRouter = APIRouter(prefix="/v1/users", tags=["users"])
bearer = HTTPBearer()

class UserSync(BaseModel):
    auth0_id: str
    internal_user_id: Optional[UUID4] = None
    user_email: str
    user_name: Optional[str] = None
    email_verified: bool

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

@UserRouter.post("/sync", status_code=200)
async def sync_user(
    request: Request,
    payload: UserSync,
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):
    token = credentials.credentials
    try:
        payload_token = await verify_token(token)
    except HTTPException as e:
        # forward 401 if token invalid
        raise e

    auth0_sub = payload_token["sub"]

    if auth0_sub != payload.auth0_id:
        raise HTTPException(status_code=403, detail="Token does not match payload")

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
          INSERT INTO users (user_id, auth0_id, user_email, user_name, email_verified)
          VALUES (
            gen_random_uuid(),  -- ALWAYS generate new UUID for new users
            %s, %s, %s, %s
          )
          ON CONFLICT (auth0_id) DO UPDATE
            SET user_email = EXCLUDED.user_email,
                user_name = COALESCE(EXCLUDED.user_name, users.user_name),
                email_verified = EXCLUDED.email_verified
          RETURNING user_id;
        """, (
            payload.auth0_id,
            payload.user_email,
            payload.user_name,
            payload.email_verified
        ))
        new_uuid = cur.fetchone()[0]
        conn.commit()
        return {"status": "synced", "user_id": new_uuid}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()
