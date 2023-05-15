from pydantic import BaseModel,EmailStr,conint
from typing import Optional

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class Postcreate(Post):
    pass

class UserRespo(BaseModel):
    email : EmailStr
    id: int
    class Config:
        orm_mode = True
class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    owner_id: int
    owner : UserRespo
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True
class User(BaseModel):
    email : EmailStr
    password : str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)