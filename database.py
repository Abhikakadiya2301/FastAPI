from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",password="12345", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection successful!!!")
        break

    except Exception as error:
        print("Connection Failed!!")
        print("Error:",error)
        time.sleep(2)"""