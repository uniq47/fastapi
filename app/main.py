# body is used to extract data from the body of the request and assign it to a variable
import time
from typing import Optional, List
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from random import randrange
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# FastAPI is a class and we are creating an instance of it and storing it in a variable called app
# Post method will  extends BaseModel class


new_post = [{"class": "CECS 229", "teacher": "gurg", "content": "", "rating": 4, "takeTheClassAgain": True, "id": 1},
            {"class": "CECS 274", "teacher": "sapkota", "content": "", "rating": 4, "takeTheClassAgain": True, "id": 2},]

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='rate_your_professor',
                                user='postgres', password='12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("connected to database")
        break
    except Exception as error:
        print("error connecting to database")
        print(error)
        time.sleep(5)


def find_item(id):
    for p in new_post:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(new_post):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}
