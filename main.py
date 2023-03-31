import time
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="12345", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection successful!!!")
        break

    except Exception as error:
        print("Connection Failed!!")
        print("Error:",error)
        time.sleep(2)

class respo_data(BaseModel):
    id : int
    name : str
    gender : str
    class Config:
        orm_model = True
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
    cursor.execute("""SELECT * FROM data""")
    post = cursor.fetchall()
    return {"Data": post}

@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_post(post: Post):
    '''post_dict = post.dict()
    post_dict['id'] = random.randrange(0,100000)
    personal_data.append(post_dict)'''
    cursor.execute("""INSERT INTO data (name,gender,married,age) VALUES (%s,%s,%s,%s) RETURNING *""",(post.name,post.gender,post.married,post.age))
    new_data = cursor.fetchone()
    conn.commit()
    return {"Data" : new_data}

@app.get("/posts/latest")
def get_latest_postr():
    post = personal_data[len(personal_data) - 1]
    return {"Latest Post" : post}

@app.get("/posts/{id}")
def get_post(id : int, response : Response):
    cursor.execute("""SELECT * FROM data WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} not found")
    #post = find_id(id)
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