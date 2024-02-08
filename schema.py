from typing import Optional
from pydantic import BaseModel, Field

class CreateTodoRequest(BaseModel):
    '''
    pydantic model for validation of request data for creating a todo
    '''
    title : str = Field(min_length=3, max_length=50)
    description : str = Field(max_length=100)
    priority : int = Field(gt=0, lt=6, default=3)
    complete :bool = Field(default=False)
    owner_id : Optional[int] = 1


class CreateUserRequest(BaseModel):
    '''
    pydantic model for validation of request data for creating a user
    '''
    email : str
    username : str
    first_name : str
    last_name : str
    password : str
    role :str



