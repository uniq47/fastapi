from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to the world of computer science"}

# A BUNCH OF SOCIAL MEDIA POSTS FRO OUR APPLICAOTIN


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createposts")
# payload is my retrive the body data, assign a var to it ours is payload
# type dict , ... helps us to get the body data from the request and assign it to payload
# extract all the fields fro mthe body and covert it tothe dictornary  and store it inside a variable named pauyload
def create_posts(payload: dict = Body(...)): #extracting data from the body 
    # print(payload)
    return {"new_post": f"email {payload['email']} firstName: {payload['firstName']}"}
