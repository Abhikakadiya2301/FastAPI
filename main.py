import random

import psycopg2
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
import pyscopyg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

try:
    conn = psycopg2.connect(host="localhost",database="Personal Data",user="postgres",password="123p45")
class Post(BaseModel):
    name : str
    gender : str
    married: bool = True
    age : Optional[int] = None

personal_data = [{"name" : "Abhsihek","gender" : "Male", "id" : 1},{"name" : "Jyoti" , "gender" : "female","id" : 2} ]

def find_id(id):
    for p in personal_data:
        if p["id"] == id:
            return p

def find_index(id):
    for i,p in enumerate(personal_data):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"message": "Hello World!!!"}

@app.get("/posts")
def get_post():
    return {"Data": personal_data}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(0,100000)
    personal_data.append(post_dict)
    return {"Data" : post_dict}

@app.get("/posts/latest")
def get_latest_postr():
    post = personal_data[len(personal_data) - 1]
    return {"Latest Post" : post}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    post = find_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
    return {"ID" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exixts.")
    personal_data.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post : Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_dict = post.dict()
    post_dict['id'] = id
    personal_data[index] = post_dict
    return {"Data" : post_dict}