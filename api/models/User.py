from pydantic import BaseModel, UUID4
from typing import Optional

class User(BaseModel):
    user_id: UUID4 
    user_name: Optional[str] = None  
    user_email: str  