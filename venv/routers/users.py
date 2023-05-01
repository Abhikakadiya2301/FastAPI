from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter
import model, schemas, utils
from sqlalchemy.orm import Session
from database import *
from typing import List

router = APIRouter()

@router.post("/users",status_code = status.HTTP_201_CREATED,response_model=schemas.UserRespo)
def create_posts(user : schemas.User,db:Session = Depends(get_db)):

    hased_pwd = hash(user.password)
    new_user = model.User(email = user.email,password = hased_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/users/{id}",response_model=schemas.UserRespo)
def get_user(id : int,db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return user