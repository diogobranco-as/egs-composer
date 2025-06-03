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

@PurchasedRouter.get("/{auth0_id}", response_model=List[Purchased])
async def get_purchased_by_user(auth0_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT p.payment_id, p.product_id, p.user_id,
                   pr.product_name
            FROM purchased p
            JOIN products pr ON p.product_id = pr.product_id
            WHERE p.user_id = %s
        """, (auth0_id,))
        purchased_items = cursor.fetchall()

        if not purchased_items:
            raise HTTPException(status_code=404, detail="Purchased item not found")

        return purchased_items
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
@PurchasedRouter.post("/{auth0_id}", response_model=Purchased)
async def create_purchased(auth0_id: str, purchased: Purchased):
    print("Received purchased data:", purchased)
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        if auth0_id != purchased.user_id:
            raise HTTPException(status_code=400, detail="Auth0 ID mismatch")

        cursor.execute(
            "SELECT * FROM purchased WHERE payment_id = %s",
            (purchased.payment_id,)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Payment exists")

        cursor.execute(
            "SELECT product_name FROM products WHERE product_id = %s",
            (str(purchased.product_id),)
        )
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute(
            """INSERT INTO purchased (payment_id, product_id, user_id) 
               VALUES (%s, %s, %s) RETURNING *""",
            (purchased.payment_id, str(purchased.product_id), auth0_id)
        )
        new_purchased = cursor.fetchone()
        conn.commit()

        new_purchased['product_name'] = product['product_name']
        
        return new_purchased
    
    except HTTPException as e:
        raise e
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
        
