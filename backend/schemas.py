from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from database import Base

class PostBase(BaseModel):
    title: str
    article: str
    likes: int
    hates: int
    post_time: datetime
    user_name: str
    board_name: str

class Post(PostBase):
    class Config():
        orm_mode = True

class WritePost(BaseModel):
    title: str
    article: str
    user: str
    board: str

class EditPost(BaseModel):
    post_id: int

class ReadPost(BaseModel):
    post_id: str

class BoardBase(BaseModel):
    board_name: str

class BoardFav(BaseModel):
    username: str
    board_name: str
    
class ShowBoard(BoardBase):
    board_posts: List[Post] = []
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    name: str
    company: str
    location: str
    email: str
    tel: str

class ShowUser(BaseModel):
    name: str
    email: str
    tel:str
    posts: List[Post] = []
    class Config():
        orm_mode = True

class HasUser(BaseModel):
    user: str

class EditUser(BaseModel):
    name: str
    email: str
    tel: str
    company: str
    location: str

class ReadInput(BaseModel):
    user_name: str
    post_id: int

class ReadCheckBoard(BaseModel):
    user_name: str
    board_name: str

class AdminUser(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    name: Optional[str] = None
