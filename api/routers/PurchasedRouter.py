from fastapi import APIRouter, HTTPException, Query
from models.Purchased import Purchased
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from uuid import UUID
import os
PurchasedRouter = APIRouter(
    prefix ="/v1/purchased",
    tags=["purchased"],
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

@PurchasedRouter.get("/{user_id}", response_model=List[Purchased])
async def get_purchased_by_user(user_id: UUID):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT p.payment_id, p.product_id, p.user_id,
                   pr.product_name
            FROM purchased p
            JOIN products pr ON p.product_id = pr.product_id
            WHERE p.user_id = %s
        """, (str(user_id),))
        purchased_items = cursor.fetchall()

        if not purchased_items:
            raise HTTPException(status_code=404, detail="Purchased item not found")

        return purchased_items
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()
        
@PurchasedRouter.post("/{user_id}", response_model=Purchased)
async def create_purchased(user_id: UUID, purchased: Purchased):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print (f"Received payment_id: {purchased.payment_id}, product_id: {purchased.product_id}, user_id: {purchased.user_id}")
    try:
        if user_id != purchased.user_id:
            raise HTTPException(status_code=400, detail="User ID mismatch")
            
        cursor.execute(
            "SELECT * FROM purchased WHERE payment_id = %s",
            (purchased.payment_id,)
        )
        existing = cursor.fetchone()
        
        if existing:
            raise HTTPException(status_code=400, detail="Payment already processed")
        
        cursor.execute(
            "INSERT INTO purchased (payment_id, product_id, user_id) VALUES (%s, %s, %s) RETURNING *",
            (purchased.payment_id, str(purchased.product_id), str(user_id))
        )
        new_purchased = cursor.fetchone()
        conn.commit()
        return new_purchased

    except Exception as e:
        print("Error during INSERT:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
