# api/init_db.py
from database import Base, engine
import models  

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created or already exist.")
