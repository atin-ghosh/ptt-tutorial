from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_USERNAME, DB_PASSWORD

user = DB_USERNAME.value + "@ptt-db"
password = DB_PASSWORD.value

DATABASE_URL = 'postgresql://' + user + ':' + password + '@ptt-db.postgres.database.azure.com:5432/postgres'

engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args ={
#     "check_same_thread": False
# })
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()