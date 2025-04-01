from fastapi import APIRouter, Depends, HTTPException
from grpc import Status
from middleware.AuthMiddleware import get_current_user
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from uuid import UUID
from pydantic import BaseModel
from typing import Optional
import logging


logging.basicConfig(level=logging.DEBUG)

class ReviewTrackRequest(BaseModel):
    review_id: str
    product_id: str

ReviewComposerRouter = APIRouter(
    prefix="/v1/review-composer",
    tags=["review-composer"],
)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return conn

@ReviewComposerRouter.post("/")
async def track_review(
    request: ReviewTrackRequest,
    user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Validate UUIDs
        try:
            review_uuid = UUID(request.review_id)
            product_uuid = UUID(request.product_id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid UUID format")

        cursor.execute(
            """INSERT INTO reviews (review_id, user_id, product_id)
               VALUES (%s, %s, %s)""",
            (str(review_uuid), user["user_id"], str(product_uuid))
        )
        conn.commit()
        return {"status": "success"}
    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise HTTPException(400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Remove one of these duplicate endpoints - keep the debug version
@ReviewComposerRouter.get("/product/{product_id}")
async def get_review_references(product_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        print(f"\n[DEBUG] Fetching review references for product: {product_id}")
        cursor.execute(
            "SELECT review_id, user_id FROM reviews WHERE product_id = %s",
            (str(product_id),)
        )
        references = cursor.fetchall()
        print(f"[DEBUG] Found {len(references)} review references")
        return references
    except Exception as e:
        print(f"[ERROR] Error fetching review references: {str(e)}")
        raise HTTPException(500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@ReviewComposerRouter.delete("/{review_id}")
async def delete_review_reference(
    review_id: UUID,
    user: dict = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # First verify the review exists and get its user_id
        print(f"\n[DEBUG] Deleting review reference: {review_id}")
        cursor.execute(
            "SELECT user_id FROM reviews WHERE review_id = %s",
            (str(review_id),)
        )
        review_record = cursor.fetchone()
        print(f"[DEBUG] Found review: {review_record}")
        
        if not review_record:
            raise HTTPException(404, detail="Review not found")
            
        # Extract the user_id from the record
        review_user_id = review_record[0]  # Access first column of result
        current_user_id = user["user_id"]
        
        print(f"[DEBUG] Current user ID: {current_user_id}")
        print(f"[DEBUG] Review user ID: {review_user_id}")
        
        # Compare the review's user_id with current user's ID
        if review_user_id != current_user_id:
            raise HTTPException(
                status_code=403,  # Using direct status code instead of Status.HTTP_403_FORBIDDEN
                detail="Cannot delete other users' reviews"
            )
        
        # Delete the review reference
        print(f"[DEBUG] Proceeding with deletion of review: {review_id}")
        cursor.execute(
            "DELETE FROM reviews WHERE review_id = %s",
            (str(review_id),)
        )
        conn.commit()
        
        return {"status": "deleted"}
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Delete failed: {str(e)}")
        raise HTTPException(500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
@ReviewComposerRouter.get("/users/{user_id}")
async def get_user_info(user_id: str):
    
    try:
        # Just try the simplest possible query first
        with psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT user_id::text, user_name FROM users LIMIT 1"
                )
                test = cursor.fetchone()
                print(f"[DEBUG] Test query result: {test}", flush=True)
                
                cursor.execute(
                    "SELECT user_id::text, user_name FROM users WHERE user_id::text = %s",
                    (user_id,)
                )
                user = cursor.fetchone()
                print(f"[DEBUG] User query result: {user}", flush=True)
                
                if not user:
                    raise HTTPException(404, detail="User not found")
                return user
    except Exception as e:
        print(f"[ERROR] {str(e)}", flush=True)
        raise HTTPException(500, detail="Database error")