from fastapi import APIRouter, HTTPException, Query
from models.Purchased import Purchased
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
PurchasedRouter = APIRouter(
    previx ="/v1/purchased",
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

@PurchasedRouter.get("/", response_model=List[Purchased])
async def get_all_purchased(
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    limit: int = Query(25, description="Limit the number of results"),
    offset: int = Query(0, description="Offset for pagination")
):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        query = "SELECT * FROM purchased"
        filters = []
        params = []

        if product_id:
            filters.append("product_id = %s")
            params.append(product_id)

        if user_id:
            filters.append("user_id = %s")
            params.append(user_id)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        purchased_items = cursor.fetchall()

        return purchased_items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
        
        
@PurchasedRouter.post("/", response_model=Purchased)
async def create_purchased(purchased: Purchased):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            "INSERT INTO purchased (payment_id, product_id, user_id) VALUES (%s, %s, %s) RETURNING *",
            (purchased.payment_id, purchased.product_id, purchased.user_id)
        )
        new_purchased = cursor.fetchone()
        conn.commit()
        return new_purchased

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
        
#delete a purchase id
@PurchasedRouter.delete("/{purchase_id}", response_model=Purchased)
async def delete_purchased(purchase_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("DELETE FROM purchased WHERE purchase_id = %s RETURNING *", (purchase_id,))
        deleted_purchased = cursor.fetchone()
        conn.commit()

        if not deleted_purchased:
            raise HTTPException(status_code=404, detail="Purchased item not found")

        return deleted_purchased

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()