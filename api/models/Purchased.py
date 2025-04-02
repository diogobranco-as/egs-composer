from pydantic import BaseModel, UUID4

class Purchased(BaseModel):
    payment_id: UUID4 
    product_id: UUID4
    user_id   : UUID4  