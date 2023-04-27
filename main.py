from fastapi import FastAPI,HTTPException,Response,status
from pydantic import BaseModel
from typing import Optional
from random import randrange
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

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_posts = [{"title" : "title 1", "content" : "Content of post 1","id" : 1},{"title" : "title 1","content" : "post 2","id" : 2}]
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
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    print(all_posts)
    return {"post": all_posts}
@app.post("/posts",status_code = status.HTTP_201_CREATED)
def create_posts(post : Post):
    """post_dict = post.dict()
    post_dict['id'] = randrange(0,10000)
    my_posts.append(post_dict)"""
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
    return {"data" : new_post}

@app.get("/posts/{id}",status_code = status.HTTP_404_NOT_FOUND)
def get_post(id : int):
    #post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    print(post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Does not exist")
    return {"post" : post}

@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    '''index = find_post_indexx(id)

    my_posts.pop(index)'''
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()
    print(deleted_post)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT),deleted_post

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    '''index = find_post_indexx(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict'''
    cursor.execute("""UPDATE posts SET title = %s,content = %s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated = cursor.fetchone()
    conn.commit()
    print(updated)
    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post did not found")
    return {"data" : updated}