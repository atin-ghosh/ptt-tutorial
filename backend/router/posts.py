from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from typing import List
from database import get_db
import models
import schemas
import oauth2


router = APIRouter(
    prefix='/post',
    tags=["post"]
)

@router.get('/', response_model=List[schemas.Post])
# def all(db:Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
def all(db:Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

@router.post('/write_post', status_code=status.HTTP_201_CREATED)
def create(request:schemas.WritePost, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        title = request.title, 
        article = request.article, 
        likes = 0,
        hates = 0,
        post_time = None,
        user_name = request.user,
        board_name = request.board
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return "OK"



@router.post('/read_post')
def read_post(request: schemas.EditPost, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    post_to_read = db.query(models.Post).filter(models.Post.id == request.post_id).first()
    formatted_post = {
        "title": post_to_read.title,        
        "author": post_to_read.user_name,
        "likes": post_to_read.likes,
        "hates": post_to_read.hates,
        "post_datetime": post_to_read.post_time,
        "article": post_to_read.article,
        "board": post_to_read.board_name
    }
    return formatted_post


@router.put('/add_likes', status_code=status.HTTP_202_ACCEPTED)
def add_likes(request: schemas.EditPost, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == request.post_id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id < {request.post_id} > not found")
    
    likes = db.query(models.Post.likes).filter(models.Post.id == request.post_id).scalar()
    
    post.update({"likes": likes + 1}, synchronize_session=False)
    db.commit()
    return {"updated successfully"}

@router.put('/add_hates', status_code=status.HTTP_202_ACCEPTED)
def add_hates(request: schemas.EditPost, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == request.post_id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id < {request.post_id} > not found")
    
    hates = db.query(models.Post.hates).filter(models.Post.id == request.post_id).scalar()
    
    post.update({"hates": hates + 1}, synchronize_session=False)
    db.commit()
    return {"updated successfully"}