from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import engine, get_db
from app.routers import post, user

from dotenv import load_dotenv
import os

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = "localhost", database = os.getenv("DATABASE"), user = os.getenv("USER"), 
                                password = os.getenv("PASSWORD"), cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)

    
app.include_router(post.router)
app.include_router(user.router)








