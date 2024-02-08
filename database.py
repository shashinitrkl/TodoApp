'''
Create the url string which will connect our fastApi application to our new database.
SQLAlchemy is an ORM used to write SQL queries for the database. For CRUD operations.
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres:@localhost:5432/TodoApplicationDatabase"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()