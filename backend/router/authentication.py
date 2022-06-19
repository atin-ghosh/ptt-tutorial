from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import schemas, models, tokens
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin_user = db.query(models.AdminUser).filter(models.AdminUser.username == request.username).first()
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'admin_user {request.username} not found')
    if not pwd_cxt.verify(request.password, admin_user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'Invalid password for {request.username}')
    
    access_token = tokens.create_access_token(data={"sub": admin_user.username})
    return {"access_token": access_token, "token_type": "bearer"}