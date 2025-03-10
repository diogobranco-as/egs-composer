from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    email: str
    name: str | None = None