from fastapi import APIRouter,Depends
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Optional,List
from fastapi import APIRouter,Depends,HTTPException

from api.core.database import get_db
from sqlalchemy.orm import Session,joinedload

from api.core.models import Appointment as AppointmentModel, Pet as PetModel, Doctor as DoctorModel

router=APIRouter()

class AppointmentBase(BaseModel):
    date: datetime
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pet_id: str
    doctor_id: str

class Appointment(AppointmentBase):
    id: str
    pet_id: str
    doctor_id: str

    class Config:
        orm_mode = True

class AppointmentUpdate(BaseModel):
    date: Optional[datetime] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None       


class OwnerInfo(BaseModel):
    id: str
    firstName: str
    lastName: str

    class Config:
        orm_mode = True
   
class PetInfo(BaseModel):
    id: str
    name: str
    owner: OwnerInfo 

    class Config:
        orm_mode = True

class DoctorInfo(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


# Modelo de appointment con pet y doctor 
class AppointmentWithNames(AppointmentBase):
    id: str
    pet: PetInfo
    doctor: DoctorInfo

    class Config:
        orm_mode = True




@router.post("/", response_model=Appointment, status_code=201)
def create_appointment(app_data: AppointmentCreate, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == app_data.pet_id).first()
    doctor = db.query(DoctorModel).filter(DoctorModel.id == app_data.doctor_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_app = AppointmentModel(
        id=str(uuid.uuid4()),
        date=app_data.date,
        diagnosis=app_data.diagnosis,
        treatment=app_data.treatment,
        pet_id=app_data.pet_id,
        doctor_id=app_data.doctor_id
    )

    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

#este era el de todos los appointments que por el momento no se uso
# @router.get("", response_model=List[Appointment])
# def get_all_appointments(db: Session = Depends(get_db)):
#     return db.query(AppointmentModel).all()

@router.get("/with-names", response_model=List[AppointmentWithNames])
def get_appointments_with_names(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentModel).options(
        joinedload(AppointmentModel.pet).joinedload(PetModel.owner),
        joinedload(AppointmentModel.doctor)
    ).all()
    return appointments

@router.get("/by-pet/{pet_id}", response_model=List[Appointment])
def get_appointments_by_pet(pet_id: str, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet.appointments

@router.patch("/{appointment_id}", response_model=Appointment)
def update_appointment(appointment_id: str, update_data: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()