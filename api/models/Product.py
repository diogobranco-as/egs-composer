from pydantic import BaseModel, UUID4
from typing import List, Optional

class Product(BaseModel):
    product_id: UUID4
    product_type: str
    product_name: str
    product_price: float
    product_seller: Optional[str] = None
    reviews: Optional[List[UUID4]] = None