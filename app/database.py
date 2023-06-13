from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time



engine = create_engine(f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#while True:
#    try:
#        conn = psycopg2.connect(host = "localhost", database = os.getenv("DATABASE"), user = os.getenv("USER"), 
#                                password = os.getenv("PASSWORD"), cursor_factory = RealDictCursor)
#        cursor = conn.cursor()
#        print("Database connection was succesfull")
#        break
#    except Exception as error:
#        print("Database connection failed")
#        print("Error: ", error)
#        time.sleep(2)