# body is used to extract data from the body of the request and assign it to a variable
import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# FastAPI is a class and we are creating an instance of it and storing it in a variable called app
# Post method will  extends BaseModel class


class Post(BaseModel):
    course: str
    teacher: str
    rating: Optional[int] = None  # default value is none,
    take_again: Optional[bool] = None


new_post = []

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


@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}


@app.get("/sqlAlchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts(course, teacher, rating, take_again) VALUES(%s, %s, %s,%s) RETURNING *""",
                   (post.course, post.teacher, post.rating, post.take_again))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

    # convert the object to dictionary, retriving posts from the database


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(
        """SELECT * from posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post not found with id {id}")

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET course = %s, teacher = %s, rating = %s, take_again = %s WHERE id = %s RETURNING *""", (post.course, post.teacher, post.rating, post.take_again, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")

    return {"data": updated_post}
