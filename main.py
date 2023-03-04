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


new_post = [{"title": "CECS 229", "teacher": "chag", "content": "", "rating": 4, "graduated": True},
            {"title": "CECS 274", "teacher": "sapkota", "content": "", "rating": 4, "graduated": True},]


@app.get("/")
async def root():  # async that takes certain amount of time to execute and we dont want to wait for it to execute
    return {"message": "welcome to the world of computer science"}


@app.get("/posts")
def get_posts():
    # logic to retrive the posts from the database
    return {"data": "This is your posts"}

# in create post we want to tell front what data we are expecting, we want two string


@app.post("/posts")
# def create_posts(payload: dict = Body(...)):  # extracting data from the body
# here posr:Post is the object of the class Post that we created for the body of the request to be converted to the object
def create_posts(new_post: Post):
    # convert the object to dictionary
    return {"data": new_post}


# inside payload we have email and firstName.
# response
# {
#     "data": [
#         {
#             "title": "CECS 229",
#             "teacher": "chag",
#             "content": "",
#             "rating": 4,
#             "graduated": true
#         },
#         {
#             "title": "CECS 274",
#             "teacher": "sapkota",
#             "content": "",
#             "rating": 4,
#             "graduated": true
#         }
#     ]
# }
