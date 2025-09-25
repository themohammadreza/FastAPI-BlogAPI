from sqlalchemy import Column, ForeignKey, String, Integer
from .database import base
from sqlalchemy.orm import relationship 


class Blog(base):
    __tablename__ = 'Blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('Users.id'))

    creator = relationship('User', back_populates='blogs')

class User(base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    blogs = relationship("Blog", back_populates="creator")
