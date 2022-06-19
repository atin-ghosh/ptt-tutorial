from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from database import get_db
import models
import oauth2
import schemas


router = APIRouter(
    prefix='/delete',
    tags=["delete"]
)

@router.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    post_to_delete = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    post_to_delete.delete(synchronize_session=False)
    db.commit()
    return {'done'}

@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    user.delete(synchronize_session=False)
    db.commit()
    return {'done'}
    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    board_to_delete = db.query(models.Board).filter(models.Board.id == id)
    
    if not board_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"board with id {id} not found")
    
    board_to_delete.delete(synchronize_session=False)
    db.commit()
    return {'done'}