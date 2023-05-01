import schemas
from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
import database,schemas,model,utils
from database import *

router = APIRouter(tags=['authentication'])
@router.post("/login")
def login(user_cred : schemas.UserLogin,db:Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_cred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credintials")
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credintials")

    return {"Token" : "Demo Token"}
