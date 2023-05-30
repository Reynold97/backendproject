from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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

    
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts 


@app.get("/posts/{id}")
def get_spec_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} not found")
    return post


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """, 
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))    
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #if deleted_post == None:
    if post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")
    
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #               (updated_post.title, updated_post.content, updated_post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    #return {"data": updated_post}
    return post_query.first()



