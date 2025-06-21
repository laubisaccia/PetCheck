from .database import Base
from sqlalchemy import Column,Integer, String,ForeignKey,DateTime,Text
from sqlalchemy.orm import relationship
import datetime

class UserDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    
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
    appointments = relationship("Appointment", back_populates="pet", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(String, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    pet_id = Column(String, ForeignKey("pets.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)

    pet = relationship("Pet", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String, primary_key=True)
    name = Column(String)

    appointments = relationship("Appointment", back_populates="doctor")
