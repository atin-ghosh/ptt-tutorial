from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    article = Column(String)
    likes = Column(Integer)
    hates = Column(Integer)
    post_time = Column(DateTime, default=datetime.utcnow)
    user_name = Column(String, ForeignKey("users.name"))
    board_name = Column(String, ForeignKey("board.name"))
    author = relationship("User", back_populates = "posts")
    on_board = relationship("Board", back_populates = "board_posts" )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True)
    email = Column(String)
    tel = Column(String)
    company = Column(String)
    location = Column(String)
    posts = relationship("Post", back_populates = "author")

class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True)
    board_posts = relationship("Post", back_populates = "on_board")

class ReadTable(Base):
    __tablename__ = 'read_table'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)
    user_name = Column(String)

class FavouriteBoards(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    board_name = Column(String)

class AdminUser(Base):
    __tablename__ = "admin_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)