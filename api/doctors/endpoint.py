from fastapi import APIRouter, HTTPException,Depends
from pydantic import BaseModel
import uuid
from api.core.database import get_db
from sqlalchemy.orm import Session
from api.core.models import Doctor 



router=APIRouter()

class DoctorCreate(BaseModel):
    name: str

class DoctorRead(BaseModel):
    id: str
    name: str

@router.post("/doctors/", response_model=DoctorRead)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(id=str(uuid.uuid4()), name=doctor.name)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

