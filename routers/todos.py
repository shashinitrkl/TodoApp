from fastapi import APIRouter, Depends, Query, Path, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from typing import Annotated

from database import SessionLocal
from schema import CreateTodoRequest
from models import Todos, Users

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/todos', status_code=status.HTTP_200_OK)
async def get_all_todos(db : db_dependency):

    todos = db.query(Todos).all()
    return todos

@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(db : db_dependency, 
                         todo_id : int = Path(gt=0)):
    
    response = db.query(Todos).filter(Todos.id == todo_id).first()
    if response is not None:
        return response
    raise HTTPException(status_code=404, detail='todo not found')

@router.get('/todos/{user_id}', status_code=status.HTTP_200_OK)
async def get_todos_by_user(db : db_dependency, 
                            user_id : int = Path(gt=0)):
    
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None or user.is_deleted == True:
        raise HTTPException(status_code=404, detail='user not found')
    user_todos = db.query(Todos).filter(Todos.owner_id == user_id).all()
    return user_todos

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db : db_dependency,
                      todo_request : CreateTodoRequest):
    
    new_todo = Todos(**todo_request.model_dump())
    db.add(new_todo)
    db.commit()

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db : db_dependency,
                      todo_request : CreateTodoRequest, 
                      todo_id : int = Path(ge=0)):
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='todo not found')
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete
    todo.owner_id = todo_request.owner_id

    db.add(todo)
    db.commit()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db : db_dependency,
                      todo_id : int = Path(gt=-1)):
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='todo not found')
    # db.query(Todos).filter(Todos.id==todo_id).delete()
    db.delete(todo)
    db.commit()