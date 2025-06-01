from .database import Base
from sqlalchemy import Column,Integer, String

class Customer(Base):
    __tablename__="customers"
    id=Column(String,primary_key=True)
    firstName= Column(String)
    lastName= Column(String)
    email=Column(String)
    phone=Column(Integer)



