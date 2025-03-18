from fastapi import APIRouter, Depends, HTTPException, Query
from models.Product import Product
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os

ProductRouter = APIRouter(
    prefix="/v1/products",
    tags=["products"],
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

@ProductRouter.get("/", response_model=List[Product])
async def get_all_products(
    product_type: Optional[str] = Query(None, description="Filter by product type"),
    product_name: Optional[str] = Query(None, description="Filter by product name"),
    limit: int = Query(25, description="Limit the number of results"),
    offset: int = Query(0, description="Offset for pagination")
):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        query = "SELECT * FROM products"
        filters = []
        params = []

        if product_type:
            filters.append("product_type = %s")
            params.append(product_type)

        if product_name:
            filters.append("product_name ILIKE %s")
            params.append(f"%{product_name}%")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        products = cursor.fetchall()

        return products

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@ProductRouter.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()