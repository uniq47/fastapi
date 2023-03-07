# body is used to extract data from the body of the request and assign it to a variable
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from  random  import randrange

app = FastAPI()
# FastAPI is a class and we are creating an instance of it and storing it in a variable called app
# Post method will  extends BaseModel class


class Post(BaseModel):
    title: str
    teacher: str
    content: str
    rating: Optional[int] = None  # default value is none, 
    takeTheClassAgain: bool = False  # default value is false


new_post = [{"title": "CECS 229", "teacher": "gurg", "content": "", "rating": 4, "takeTheClassAgain": True, "id":1},
            {"title": "CECS 274", "teacher": "sapkota", "content": "", "rating": 4, "takeTheClassAgain": True, "id":2},]


def find_item(id):
    for p in new_post:
        if p["id"] == id:
            return p 

@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}


@app.get("/posts")
def get_posts():
    return {"data": new_post}




@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    new_post.append(post_dict)
    return {"data": new_post}

    # convert the object to dictionary, retriving posts from the database

@app.get("/posts/{id}")
def get_post(id: int):
    item = find_item(id)
    print("This is the item" , item)
    return {"data": item}

