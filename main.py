# body is used to extract data from the body of the request and assign it to a variable
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()
# FastAPI is a class and we are creating an instance of it and storing it in a variable called app
# Post method will  extends BaseModel class


class Post(BaseModel):
    title: str
    teacher: str
    content: str
    rating: str
    graduated: bool = False  # default value is false


@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}


@app.get("/posts")
def get_posts():
    # logic to retrive the posts from the database
    return {"data": "This is your posts"}

# in create post we want to tell front what data we are expecting, we want two string


@app.post("/createposts")
# def create_posts(payload: dict = Body(...)):  # extracting data from the body
def create_posts(post: Post):  # here posr:Post is the object of the class Post that we created for the body of the request to be converted to the object
    print(post)
    print(post.graduated)    # convert the object to dictionary
    return {"data": post}


# inside payload we have email and firstName.
# {
#     "firstname": "aayam",
#     "lastname": "sapkotaaaaaaa"
# }
