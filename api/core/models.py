from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

from api.core.database import Base

class Clientes(Base):
    __tablename__="clientes"
    id=Column(Integer,primary_key=True, index=True)
    nombre=Column(String,nullable=True)