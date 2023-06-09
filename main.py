from fastapi import FastAPI
import model
from database import *
from routers import posts,users,auth,vote

model.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message" : "Hello World!!"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)