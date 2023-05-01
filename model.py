from database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,Boolean
from sqlalchemy.sql.expression import null,true
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,nullable=False,primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='1')
    created_at = Column(TIMESTAMP,nullable=False,server_default=text("now()"))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,nullable=False,server_default=text("now()"))
