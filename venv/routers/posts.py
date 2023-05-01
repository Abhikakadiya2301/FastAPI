from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
import model, schemas, utils
from sqlalchemy.orm import Session
from database import *
from typing import List

router = APIRouter()

@router.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db)):
    '''cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    print(all_posts)'''
    posts = db.query(model.Post).all()
    return posts
@router.post("/posts",status_code = status.HTTP_201_CREATED,response_model=schemas.PostResponse)
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

@router.get("/posts/{id}",status_code = status.HTTP_404_NOT_FOUND,response_model=schemas.PostResponse)
def get_post(id : int, db:Session = Depends(get_db)):
    #post = find_post(id)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    """post = cursor.fetchone()
    print(post)"""
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Does not exist")
    return post

@router.delete("/posts/{id}",status_code = status.HTTP_204_NO_CONTENT)
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

@router.put("/posts/{id}",response_model=schemas.PostResponse)
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
