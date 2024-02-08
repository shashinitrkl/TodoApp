from fastapi import FastAPI
from database import Base, engine
from routers import auth, todos

app = FastAPI()

# Create all models in db
Base.metadata.create_all(bind=engine)

# Connect routers
app.include_router(auth.router)
app.include_router(todos.router)


