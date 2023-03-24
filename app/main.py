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


@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    post = db.query(models.Post).all()
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(course, teacher, rating, take_again) VALUES(%s, %s, %s,%s) RETURNING *""",
    #                (post.course, post.teacher, post.rating, post.take_again))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(course=post.course, teacher=post.teacher,
    #                        rating=post.rating, take_again=post.take_again)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    # convert the object to dictionary, retriving posts from the database


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post not found with id {id}")

    return post


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id =%s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET course = %s, teacher = %s, rating = %s, take_again = %s WHERE id = %s RETURNING *""", (post.course, post.teacher, post.rating, post.take_again, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashed the password
    # hashed_password = pwd_context.hash(user.password)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found with id {id}")
    return user
