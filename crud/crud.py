from operator import mod
from sqlalchemy.orm import Session

import models.users as models
import document.schemas as schemas
import sys
sys.path.append("..")


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def save_paper(db: Session, paper: schemas.Paper_submit):
    db_paper = models.Paper(id=paper.id, title=paper.title, description=paper.description,
                            owner_email=paper.owner_email, public=paper.public)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


def check_paper_submitable(db: Session, paper: schemas.paper_name):
    return db.query(models.Paper).filter(models.Paper.title == paper.title, models.Paper.owner_email == paper.owner_email).first()
