from fastapi import APIRouter, Depends, Query, Path, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated

from database import SessionLocal
from schema import CreateUserRequest
from models import Users

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/users', status_code=status.HTTP_200_OK)
async def get_all_users(db : db_dependency):
    
    active_users = []
    users = db.query(Users).all()

    for user in users:
        if user.is_active == True:
            active_users.append(user)

    return active_users

@router.get('/deleted-users',status_code=status.HTTP_200_OK)
async def get_deleted_users(db : db_dependency):
    deleted_users = db.query(Users).filter(Users.is_deleted==True).all()
    return deleted_users

@router.get('/user', status_code=status.HTTP_200_OK)
async def get_user_by_id(db : db_dependency, 
                         user_id : int = Query(gt=0)):
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    elif user.is_deleted == True:
        return {'message' : 'User is not active anymore'}
    return user

@router.post('/user', status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, 
                      user_request : CreateUserRequest):
    
    new_user = Users(email = user_request.email,
                     username = user_request.username,
                     first_name = user_request.first_name,
                     last_name = user_request.last_name,
                     hashed_password = user_request.password,
                     role = user_request.role,
                     is_active = True,
                     is_deleted = False
                     )
    
    db.add(new_user)
    db.commit()

@router.put('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db : db_dependency, 
                      user_request : CreateUserRequest, 
                      user_id : int = Path(gt=0)):
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    user.username = user_request.username
    user.first_name = user_request.first_name
    user.last_name = user_request.last_name
    user.role = user_request.role
    user.hashed_password = user_request.password

    db.add(user)
    db.commit()

@router.delete('/user/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db : db_dependency,
                      user_id : int = Path(gt=0)):
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    user.is_active = False
    user.is_deleted = True

    db.add(user)
    db.commit()


