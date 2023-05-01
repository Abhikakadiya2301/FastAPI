from pydantic import BaseModel,EmailStr

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

class Postcreate(Post):
    pass

class PostResponse(BaseModel):
    title : str
    content : str
    published : bool

    class Config:
        orm_mode = True

class User(BaseModel):
    email : EmailStr
    password : str

    class Config:
        orm_mode = True
class UserRespo(BaseModel):
    email : EmailStr
    id: int
    class Config:
        orm_mode = True
