from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    name : str
    gender : str
    married: bool = True
    age : Optional[int] = None

@app.get("/")
def read_root():
    return {"message": "Hello World!!!"}

@app.get("/posts")
def get_post():
    return {"Data": "This is your post"}

@app.post("/createposts")
def create_post(new_post: Post):
    print(new_post.dict())
    return {"Data" : new_post}