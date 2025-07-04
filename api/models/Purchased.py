from typing import Optional
from pydantic import BaseModel, UUID4

class Purchased(BaseModel):
    payment_id: str 
    product_id: UUID4
    user_id: str  
    product_name: Optional[str] = None