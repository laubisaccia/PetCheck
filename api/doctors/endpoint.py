from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
import uuid
from typing import List

from api.appointments.endpoint import DoctorInfo
from api.core.database import get_db
from sqlalchemy.orm import Session
from api.core.models import Doctor 
from api.core.models import Doctor as DoctorModel
from api.auth.endpoint import get_current_admin
from typing import Optional

router=APIRouter()

class DoctorCreate(BaseModel):
    name: str

class DoctorRead(BaseModel):
    id: str
    name: str
    class Config:
        from_attributes = True  # Para Pydantic v2

class DoctorUpdate(BaseModel):
    name: Optional[str] = None  

@router.get("", response_model=List[DoctorInfo])
def get_all_doctors(db: Session = Depends(get_db)):
    return db.query(DoctorModel).all()

#aca limito solo el post para el admin
@router.post("", response_model=DoctorRead)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db), user = Depends(get_current_admin)):
    new_doctor = Doctor(id=str(uuid.uuid4()), name=doctor.name)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@router.delete("/{id_doctor}")
async def delete_doctor(id_doctor: str, db: Session = Depends(get_db)):
    doctor = db.query(DoctorModel).filter(DoctorModel.id == id_doctor).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": "Doctor deleted"}

@router.patch("/{id_doctor}", response_model=DoctorRead) 
async def patch_doctor(id_doctor: str, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    doctor_db = db.query(DoctorModel).filter(DoctorModel.id == id_doctor).first()
    if not doctor_db:
        raise HTTPException(status_code=404, detail="Doctor not found")

    update_data = doctor_update.model_dump(exclude_unset=True)  # para Pydantic v2

    for key, value in update_data.items():
        setattr(doctor_db, key, value)

    db.commit()
    db.refresh(doctor_db)
    return doctor_db