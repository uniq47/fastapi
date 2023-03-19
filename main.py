# body is used to extract data from the body of the request and assign it to a variable
import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()
# FastAPI is a class and we are creating an instance of it and storing it in a variable called app
# Post method will  extends BaseModel class


class Post(BaseModel):
    course: str
    teacher: str
    rating: Optional[int] = None  # default value is none,


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


new_post = [{"class": "CECS 229", "teacher": "gurg", "content": "", "rating": 4, "takeTheClassAgain": True, "id": 1},
            {"class": "CECS 274", "teacher": "sapkota", "content": "", "rating": 4, "takeTheClassAgain": True, "id": 2},]


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


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    new_post.append(post_dict)
    return {"data": new_post}

    # convert the object to dictionary, retriving posts from the database


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_item(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post not found with id {id}")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")
    new_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found with id {id}")
    post_dict = post.dict()
    post_dict["id"] = id
    new_post[index] = post_dict
    return {"data": new_post[index]}
