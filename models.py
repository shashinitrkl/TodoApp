'''
Models are a way of sqlalchemy to understand what kind of tables we are going to create in the database in future.
'''

from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

class Users(Base):
    '''
    users table
    '''

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    role = Column(String)

class Todos(Base):
    '''
    todos table 
    '''
    
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))
