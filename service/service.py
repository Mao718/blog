from datetime import datetime, timedelta
import email
from hashlib import algorithms_available
import document.schemas as schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import crud.crud as crud
import bcrypt
from jose import jwt

SELECTKEY = "zxcvnjk325v231q5349v519a3s5438338"
ALGORITHM = "HS256"


def create_user(db: Session, user: schemas.UserCreate):
    salt = bcrypt.gensalt()
    user.password = bcrypt.hashpw(bytes(user.password, encoding="utf8"), salt)
    dbuser = crud.create_user(db, user)
    exist_user = schemas.User(email=dbuser.email)
    return exist_user


def create_access_token(user: schemas.User_login):
    to_encode = {"sub": user.email,
                 "exp": datetime.utcnow()+timedelta(minutes=5)
                 }
    encode = jwt.encode(to_encode, SELECTKEY, algorithm=ALGORITHM)
    return schemas.Token(token=encode)


def login(db: Session, user: schemas.UserCreate):
    db_user = crud.get_user_by_email(db, user.email)
    if bcrypt.checkpw(bytes(user.password, encoding="utf8"), db_user.hashed_password):
        return create_access_token(user)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="worng password")


def token_decode(token: schemas.Token):
    decode = jwt.decode(token.token, SELECTKEY, algorithms=[ALGORITHM])
    return schemas.User(email=decode["sub"])


def check_user(db: Session, token: schemas.Token):
    user = token_decode(token)
    dbuser = crud.get_user_by_email(db, user.email)
    if not dbuser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not exist")
    return user


SELECTKEY_paper = "paper"


def create_paper_id(paper: schemas.Paper, user: schemas.User):
    to_encode = {
        'author': user.email,
        'title': paper.title
    }
    encode = jwt.encode(to_encode, SELECTKEY_paper, algorithm=ALGORITHM)
    return schemas.Token(token=encode)


def paper_submit(db: Session, paper: schemas.Paper_submit):
    dbpaper = crud.save_paper(db, paper)
    # exist_paper = schemas.paper_name(
    #    owner_email=paper.owner_email, title=dbpaper.title)
    return dbpaper
