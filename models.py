from sqlalchemy import Column,Integer,String
from database import Base

class User(Base):
    __tablename__="user_tb"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(20))
    DEPARTMAENT=Column(String(50))
    email=Column(String(20))
    
    def __repr__(self):
        return '<User %r>'% (self.id)