from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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


posts = [
    {
        "title": "Fav Motorcycle",
        "content": "Triumph Speedmaster",
        "id": 1
    },
    {
        "title": "Fav Motorcycle 2",
        "content": "Triumph Bobber",
        "id": 2
    }
]


    
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}  


@app.get("/posts/{id}")
def get_spec_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} not found")
    return {"data": post}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """, 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))    
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")
    return {"data": updated_post}