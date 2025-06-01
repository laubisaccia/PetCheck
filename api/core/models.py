from .database import Base
from sqlalchemy import Column,Integer, String,ForeignKey
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__="customers"
    id=Column(String,primary_key=True)
    firstName= Column(String)
    lastName= Column(String)
    email=Column(String)
    phone=Column(Integer)

#aca esto me viene bien porque si se borra un customer se borran sus mascotas
#relationship me crea una conexion entre los modelos
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")

class Pet(Base):
    __tablename__ = "pets"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    animal = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)

    owner = relationship("Customer", back_populates="pets")



