from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List

from sqlalchemy.orm import Session

from app import models, schemas, database, oauth2

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts 


@router.get("/{id}", response_model= schemas.PostOut)
def get_spec_post(id: int, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} not found")
    return post


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostOut)
def create_posts(post: schemas.PostCreate, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """, 
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))    
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    #if deleted_post == None:
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post {id} was not found")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.PostOut)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(database.get_db), user_id: int = Depends(oauth2.get_current_user)):
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