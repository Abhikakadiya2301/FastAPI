from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import model
from database import *
from routers import posts,users,auth

model.Base.metadata.create_all(bind=engine)
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

@app.get("/")
def root():
    return {"message" : "Hello World!!"}

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i

def find_post_indexx(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
