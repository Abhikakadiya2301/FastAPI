class Post(Base):
    __tablename__ = "data"

    id = Column(Integer,nullable=False,primary_key=True)
    name = Column(String,nullable=False)
    gender = Column(String,nullable=False)
    married = Column(Boolean,nullable=False,default=False)
    age = Column(Integer,nullable=False)
