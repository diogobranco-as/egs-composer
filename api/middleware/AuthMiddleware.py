import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
import httpx

security = HTTPBearer()

async def verify_token(token: str) -> dict:
    try:
        auth0_domain = os.getenv("AUTH0_DOMAIN")
        auth0_audience = os.getenv("AUTH0_AUDIENCE")
        
        jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            jwks_response = await client.get(jwks_url)
            jwks = jwks_response.json()
        
        # Get the key from the JWKS
        header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break
        
        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header"
            )

        # Verify and decode the JWT
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=auth0_audience,
            issuer=f"https://{auth0_domain}/"
        )
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    
    try:
        payload = await verify_token(token)
        
        # Extract the UUID part from the Auth0 user ID
        auth0_user_id = payload["sub"]
        user_uuid = auth0_user_id.split("|")[-1]  # Takes everything after "auth0|"
        
        db_params = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT", "5432"),
            "connect_timeout": 5,
        }
                
        try:
            conn = psycopg2.connect(**db_params)
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(
                "SELECT user_id, user_name, user_email FROM users WHERE user_id = %s",
                (user_uuid,) 
            )
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found in database"
                )
                
            return {
                "user_id": user["user_id"],
                "user_name": user["user_name"],
                "user_email": user["user_email"]
            }
            
        except psycopg2.OperationalError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable"
            )
        finally:
            if 'conn' in locals():
                conn.close()
                
    except Exception as e:
        raise