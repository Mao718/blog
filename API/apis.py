from typing import List

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from configs.database import get_db
import crud.crud as crud
import service.service as service

import document.schemas as schemas
APIrouter = APIRouter()


@APIrouter.post("/signup/", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already exist")
    return service.create_user(db, user)


@APIrouter.post("/login/{user.email}", response_model=schemas.Token)
def login(user: schemas.User_login, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not exist")
    return service.login(db, user)


@APIrouter.post("/paper_submit/{paper.tile}")
def paper_submit(user_token: schemas.Token, paper: schemas.Paper, db: Session = Depends(get_db)):
    user = service.check_user(db, user_token)
    paper_name = schemas.paper_name(owner_email=user.email, title=paper.title)
    if crud.check_paper_submitable(db, paper_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Author have a paper with same name")
    paper_token = service.create_paper_id(paper, user)
    paper = schemas.Paper_submit(
        title=paper.title, description=paper.description, public=paper.public, owner_email=user.email, id=paper_token.token)
    return service.paper_submit(db, paper)


@APIrouter.post("/test/")
def test(paper: schemas.Paper_submit, db: Session = Depends(get_db)):
    return crud.save_paper(db, paper)
