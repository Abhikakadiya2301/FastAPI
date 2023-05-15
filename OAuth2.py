from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas,model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Config import settings

import database

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MIN = settings.access_token_expire_min


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credintial_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("user_id")

        if id is None:
            raise credintial_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credintial_exception
    return token_data


def get_current_user(token: str = Depends(oauth_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token,credentials_exception)
    user = db.query(model.User).filter(model.User.id == token.id).first()
    return user
