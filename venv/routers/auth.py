from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from database import *
import database,schemas,model,utils,OAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(tags=['authentication'])
@router.post("/login")
def login(user_cred : OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):

    user = db.query(model.User).filter(model.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credintials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = OAuth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token,"token_type" : "bearer"}
