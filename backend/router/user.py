from operator import and_, is_
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from database import get_db
from fastapi import Depends
from passlib.context import CryptContext
from typing import List
import schemas, models
import oauth2

router = APIRouter(
    prefix='/user',
    tags=["user"]
)

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")



@router.post('/')
def create_user(request: schemas.UserBase, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    new_user = models.User(
        name = request.name,
        company = request.company,
        location = request.location, 
        email = request.email,
        tel = request.tel)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/has_user')
def has_user(request: schemas.HasUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    query = select(models.User).where(models.User.name == request.user)
    if db.execute(query).first():
        return 'Y'
    return 'N'

@router.post('/has_read')
def has_read(request: schemas.ReadInput, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # check if it is already in:
    query = select(models.ReadTable).where(and_(
        models.ReadTable.user_name == request.user_name, 
        models.ReadTable.post_id == request.post_id))
    if db.execute(query).first():
        return f"{request.user_name} has read {request.post_id}"

    new_pair = models.ReadTable(
        user_name = request.user_name, 
        post_id = request.post_id)
    db.add(new_pair)
    db.commit()
    db.refresh(new_pair)
    return {"added"}



@router.post('/get_user')
def get_user(request: schemas.HasUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    user_info = db.query(models.User).filter(models.User.name == request.user).first()
    formatted_user = {
        "company": user_info.company,        
        "location": user_info.location,
        "email": user_info.email,
        "telephone": user_info.tel
    }
    return formatted_user



@router.post('/edit_user')
def edit_user(request: schemas.EditUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    user_info = db.query(models.User).filter(models.User.name == request.name)
    user_info.update({
        "email": request.email,
        "tel": request.tel,
        "company": request.company,
        "location": request.location
        }, synchronize_session=False)
    db.commit()
    return {"updated successfully"}



@router.post('/get_all_boards_info')
def get_all_boards_info(request: schemas.HasUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # subquery returns all the top dated posts for each boad
    subquery = db.query(models.Post,func.rank().over(order_by=models.Post.post_time.desc(),partition_by=models.Post.board_name).label('rank')).subquery()
    # subuery_2 returns the read tables by the user
    subquery_read = db.query(models.ReadTable).filter(models.ReadTable.user_name == request.user).subquery()
    all_info = db.query(subquery, subquery_read.c.id.label('has_read_id')).join(
        subquery_read, subquery.c.id == subquery_read.c.post_id, isouter=True).filter(
            subquery.c.rank == 1).all()
    all_boards_info = []
    for info in all_info:
        all_boards_info.append({
        "board_name": info.board_name,
        "has_read": True if info.has_read_id else False,
        "last_post": info.post_time})
    return all_boards_info
    # boards = db.query(models.Board.name).all()
    # all_boards_info = []
    # for x in boards:
    #     name_of_board = x.name
    #     latest_post = db.query(models.Post).filter(models.Post.board_name == name_of_board).order_by(models.Post.post_time.desc()).first()
    #     latest_post_time = latest_post.post_time
    #     latest_post_id = latest_post.id
    #     has_read = False
    #     is_fav = False
    #     query_read = select(models.ReadTable).where(and_(
    #         models.ReadTable.user_name == request.user, 
    #         models.ReadTable.post_id == latest_post_id))
    #     if db.execute(query_read).first():
    #         has_read = True
    #     query_fav = select(models.FavouriteBoards).where(and_(
    #         models.FavouriteBoards.board_name == name_of_board,
    #         models.FavouriteBoards.username == request.user))
    #     if db.execute(query_fav).first():
    #         is_fav = True

    #     all_boards_info.append( {
    #         "board_name": name_of_board,
    #         "has_read": has_read,
    #         "last_post": latest_post_time,
    #         "favourite": is_fav
    #     } )
    # return all_boards_info



@router.post('/get_all_fav_info')
def get_all_fav_info(request: schemas.HasUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # subquery returns all the top dated posts for each boad
    subquery = db.query(models.Post,func.rank().over(order_by=models.Post.post_time.desc(),partition_by=models.Post.board_name).label('rank')).subquery()
    # subuery_2 returns the read tables by the user
    subquery_read = db.query(models.ReadTable).filter(models.ReadTable.user_name == request.user).subquery()
    # subquery_3 returns the favouite boards by the user

    subquery_fav = db.query(models.FavouriteBoards).filter(models.FavouriteBoards.username == request.user).subquery()
    
    all_info_subquery = db.query(subquery, subquery_read.c.id.label('has_read_id')).join(
        subquery_read, subquery.c.id == subquery_read.c.post_id, isouter=True).filter(
            subquery.c.rank == 1).subquery()
    all_info = db.query(all_info_subquery, subquery_fav.c.id.label('is_fav_id')).join(
        subquery_fav, all_info_subquery.c.board_name == subquery_fav.c.board_name, isouter=False).all()

    all_favs_info = []
    for info in all_info:
        all_favs_info.append({
        "board_name": info.board_name,
        "has_read": True if info.has_read_id else False,
        "last_post": info.post_time,
        "favourite": True if info.is_fav_id else False})
    return all_favs_info

    # boards = db.query(models.FavouriteBoards.board_name).where(models.FavouriteBoards.username == request.user).all()
    # fav_boards_info = []
    # for x in boards:
    #     name_of_board = x.board_name
    #     latest_post = db.query(models.Post).filter(models.Post.board_name == name_of_board).order_by(models.Post.post_time.desc()).first()
    #     latest_post_time = latest_post.post_time
    #     latest_post_id = latest_post.id
    #     has_read = False
    #     is_fav = False
    #     query_read = select(models.ReadTable).where(and_(
    #         models.ReadTable.user_name == request.user, 
    #         models.ReadTable.post_id == latest_post_id))
    #     if db.execute(query_read).first():
    #         has_read = True
    #     query_fav = select(models.FavouriteBoards).where(and_(
    #         models.FavouriteBoards.board_name == name_of_board,
    #         models.FavouriteBoards.username == request.user))
    #     if db.execute(query_fav).first():
    #         is_fav = True

    #     fav_boards_info.append( {
    #         "board_name": name_of_board,
    #         "has_read": has_read,
    #         "last_post": latest_post_time,
    #         "favourite": is_fav,
    #     } )
    # return fav_boards_info



@router.post('/get_all_posts_info')
def get_all_posts_info(request:schemas.BoardFav, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).where(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).all()
    posts = db.query(models.Post, models.ReadTable.id).join(models.ReadTable, 
    and_(models.Post.id == models.ReadTable.post_id, models.ReadTable.user_name == request.username), isouter=True).where(models.Post.board_name == request.board_name).order_by(models.Post.post_time.desc()).all()
    all_posts_info = []
    for x in posts:
        all_posts_info.append( {
            "id": x.Post.id,
            "hates": x.Post.hates,
            "user_name": x.Post.user_name,
            "title": x.Post.title,
            "likes": x.Post.likes,
            "post_time": x.Post.post_time,
            "board_name": x.Post.board_name,
            "has_read": True if x.id else False
        })
    return all_posts_info


@router.post('/admin_creation')
def create_admin(request: schemas.AdminUser, db: Session = Depends(get_db), current_user: schemas.AdminUser = Depends(oauth2.get_current_user)):
    new_admin = models.AdminUser(
        username = request.username, 
        password = pwd_cxt.hash(request.password))
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

