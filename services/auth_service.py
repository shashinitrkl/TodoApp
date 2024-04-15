from typing import Annotated

from fastapi import Depends

from database import SessionLocal
from models import Users


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[SessionLocal, Depends(get_db)]

class AuthService:
    
    def all_users(db):
        active_users = []
        users = db.query(Users).all()

        for user in users:
            if user.is_active == True:
                active_users.append(user)    
        
        return active_users



