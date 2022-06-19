from operator import mod
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import select, and_, desc
from fastapi import APIRouter
from database import get_db
import schemas
import models
import oauth2

router = APIRouter(
    prefix='/board',
    tags=["Board"]
)



@router.get('/all')
def all(db:Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    boards = db.query(models.Board.name).all()
    return boards



@router.get('/all_board_names')
def all(db:Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    boards = db.query(models.Board.name).all()
    return boards



@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    new_board = models.Board(name = request.board_name)
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board



@router.post('/get_posts')
def get_posts(request:schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    posts_from_board = db.query(models.Post).where(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).all()
    return posts_from_board



@router.post('/count_likes', status_code=status.HTTP_202_ACCEPTED)
def count_likes(request:schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # below query is to check if the board has no posts/does not exist
    query = select(models.Board).join(models.Post).where(models.Board.name == request.board_name)
    if not db.execute(query).first():
        return "board has no posts or the board does not exist"
    
    # we query the total likes from the Post table, since every post will be tagged to a board_name.
    total_likes = db.query(func.sum(models.Post.likes)).group_by(models.Post.board_name).having(models.Post.board_name == request.board_name).scalar()
    return f"{total_likes}"



@router.post('/get_latest_post_time')
def get_latest_post_time(request: schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # first we find the title of the latest post for the blog
    latest_post = db.query(models.Post).filter(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).first()
    latest_post_time = latest_post.post_time
    return latest_post_time



@router.post('/get_latest_post_id')
def get_latest_post_id(request: schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # first we find the title of the latest post for the blog
    latest_post = db.query(models.Post).filter(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).first()
    return latest_post



@router.post('/is_latest_unread')
def is_latest_unread(request: schemas.ReadCheckBoard, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # below query is to check if the board has no posts/does not exist
    query = select(models.Board).join(models.Post).where(models.Board.name == request.board_name)    
    if not db.execute(query).first():
        return "board has no posts or the board does not exist"
    
    # first we find the id of the latest post for the blog
    latest_post = db.query(models.Post).filter(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).first()
    latest_post_id = latest_post.id

    # now we see if this pairing is in the ReadTable
    read_check = select(models.ReadTable).where(and_(
        models.ReadTable.user_name == request.user_name, 
        models.ReadTable.post_id == latest_post_id))
    if not db.execute(read_check).first():
        return "Y"
    return "N"



@router.post('/read_latest_post', status_code=status.HTTP_202_ACCEPTED)
def read_latest_post(request:schemas.BoardBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # below query is to check if the board has no posts/does not exist
    query = select(models.Board).join(models.Post).where(models.Board.name == request.board_name)    
    if not db.execute(query).first():
        return "board has no posts or the board does not exist"
    latest_post = db.query(models.Post).filter(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).first()
    formatted_latest_post = {
        "author": latest_post.user_name,
        "board": latest_post.board_name,
        "post_datetime": latest_post.post_time,
        "title": latest_post.title,
        "article": latest_post.article
    }
    return formatted_latest_post



@router.post('/add_fav')
def add_fav(request:schemas.BoardFav, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # below query is to check if the board is already in the favourites of the user

    query = select(models.FavouriteBoards).where(and_(
        models.FavouriteBoards.username == request.username,
        models.FavouriteBoards.board_name == request.board_name))
        
    if db.execute(query).first():
        return "board is already in favorites"
    
    new_fav_board = models.FavouriteBoards(
        username = request.username,
        board_name = request.board_name)
    db.add(new_fav_board)
    db.commit()
    db.refresh(new_fav_board)
    return new_fav_board

@router.post('/get_fav')
def get_fav(request: schemas.HasUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    fav_boards = db.query(models.FavouriteBoards).filter(models.FavouriteBoards.username == request.user).all()
    return fav_boards



@router.delete('/del_fav')
def del_fav(request: schemas.BoardFav, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    fav_to_delete = db.query(models.FavouriteBoards).filter(and_(
        models.FavouriteBoards.username == request.username, 
        models.FavouriteBoards.board_name == request.board_name))
    if not fav_to_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"board < {request.board_name} > not a favourite of < {request.username} >")
    fav_to_delete.delete(synchronize_session=False)
    db.commit()
    return {'done'}
