from fastapi import FastAPI
# from fastapi. params import Body
# from pydantic import BaseModel
from typing import List
from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models
from .database import engine
# from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .routers import post, user , auth,vote
from pydantic_settings import BaseSettings
from .config import BaseSettings
from fastapi.middleware.cors import CORSMiddleware




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# origins = ["https://www.google.com"]
origins = ["*"]

# models.Base.metadata.create_all(bind=engine) #as we alemebic we no longer need this as this is command
# which told sql achemy to run the create statement when it started up

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






# my_posts = [{"title":"title of post 1","content": " content of post 1", "id": 1},
#             {"title":"favorite foods","content": "I like pizza", "id": 2}]

# def find_post(id):
#     for i in my_posts:
#         if i["id"] == id:
#             return i
        
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if  p['id'] == id:

        
#             print("true")-+
#             return i      

#as the main.py file was getting cluttered we need to seperate it and
# and we have written the code in a different file and we are telling to also go through these files when 
# a request comes        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World1"} 

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
#     post = db.query(models.Post).all() 
#     return {"status": post}
            