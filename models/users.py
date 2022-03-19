from configs.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import sys
sys.path.append("..")


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, primary_key=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    papers = relationship("Paper", back_populates="owner")


class Paper(Base):
    __tablename__ = "papers"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_email = Column(Integer, ForeignKey("users.email"))
    public = Column(Boolean)
    owner = relationship("User", back_populates="papers")
