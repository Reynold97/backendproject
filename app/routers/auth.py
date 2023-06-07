from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app import models, schemas, utils, database, oauth2

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    # create token
    acces_token = oauth2.create_acces_token(data= {"user_id": user.id})
    return {"acces_token": acces_token, "token_type": "bearer"}