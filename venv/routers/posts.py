from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
import OAuth2
import model, schemas, utils
from sqlalchemy.orm import Session
from database import *
from typing import List

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db),current_user :int = Depends(OAuth2.get_current_user)):
    '''cursor.execute("""SELECT * FROM posts""")
    all_posts = cursor.fetchall()
    print(all_posts)'''
    posts = db.query(model.Post).filter(model.Post.owner_id == current_user.id).all()
    return posts
@router.post("/",status_code = status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.Postcreate,db:Session = Depends(get_db),current_user:int = Depends(OAuth2.get_current_user)):
    '''cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)'''
    print(current_user.id)
    new_post = model.Post(owner_id = current_user.id,title = post.title,content = post.content,published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id : int, db:Session = Depends(get_db),current_user:int = Depends(OAuth2.get_current_user)):
    #post = find_post(id)
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    """post = cursor.fetchone()
    print(post)"""
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Does not exist")
    return post

@router.delete("/{id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db:Session = Depends(get_db),current_user:int = Depends(OAuth2.get_current_user)):
    '''index = find_post_indexx(id)
    my_posts.pop(index)'''
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)),)
    """deleted_post = cursor.fetchone()
    conn.commit()"""
    deleted_post = db.query(model.Post).filter(model.Post.id == id)
    post = deleted_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised")
    deleted_post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT),deleted_post

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,post:schemas.Post,db:Session = Depends(get_db),current_user:int = Depends(OAuth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s,content = %s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    #updated = cursor.fetchone()
    #conn.commit()
    updated_post_query = db.query(model.Post).filter(model.Post.id == id)
    updated_post = updated_post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post did not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorised")
    updated_post_query.update(post.dict())
    db.commit()
    return updated_post
