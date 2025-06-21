from sqlalchemy import Column, String, Integer, Text
from database import Base

class Blog(Base):

    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    password = Column(String(255), nullable=False)

    