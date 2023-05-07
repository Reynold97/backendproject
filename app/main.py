from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    
    return {"data": posts}  


@app.get("/posts/{id}")
def get_spec_post(id: int, response: Response):
    
    for p in posts:
        if p["id"] == int(id):
            return {"data": p}

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} not found")
    return {"data": "not found"}


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):

    post_dic = post.dict()
    post_dic["id"] = randrange(0,1000000)
    posts.append(post_dic)

    return {"data": post_dic}


@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    index = -1
    for i,p in enumerate(posts):
        if p["id"]==int(id):
            index = i
    
    if index == -1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")

    posts.pop(index)

    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = -1
    for i,p in enumerate(posts):
        if p["id"]==int(id):
            index = i
    
    if index == -1:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")

    post_dic = post.dict()
    post_dic["id"] = id
    posts[index] = post_dic

    return {"data": post_dic}