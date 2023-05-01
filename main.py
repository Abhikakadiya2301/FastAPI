from fastapi import FastAPI,HTTPException,Response,status,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
import model,schemas
from sqlalchemy.orm import Session
from database import *

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
@app.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db)):
    '''cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    print(all_posts)'''
    posts = db.query(model.Post).all()
    return posts
@app.post("/posts",status_code = status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.Postcreate,db:Session = Depends(get_db)):
    '''cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)'''
    new_post = model.Post(title = post.title,content = post.content,published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",status_code = status.HTTP_404_NOT_FOUND,response_model=schemas.PostResponse)
def get_post(id : int, db:Session = Depends(get_db)):
    #post = find_post(id)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    """post = cursor.fetchone()
    print(post)"""
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Does not exist")
    return post

@app.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db)):
    '''index = find_post_indexx(id)
    my_posts.pop(index)'''
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)),)
    """deleted_post = cursor.fetchone()
    conn.commit()"""
    deleted_post = db.query(model.Post).filter(model.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    deleted_post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT),deleted_post

@app.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.Post,db:Session = Depends(get_db)):

    #cursor.execute("""UPDATE posts SET title = %s,content = %s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    #updated = cursor.fetchone()
    #conn.commit()
    updated_post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post did not found")
    updated_post_query.update(post.dict())
    db.commit()
    return updated_post

@app.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.User)
def create_posts(user : schemas.User,db:Session = Depends(get_db)):

    new_user = model.User(email = user.email,password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
