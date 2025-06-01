from fastapi import APIRouter,Depends
from pydantic import BaseModel, Field
from typing import Optional,List
import uuid
from fastapi import APIRouter,Depends,HTTPException
from api.core.database import get_db
from sqlalchemy.orm import Session
from api.core.models import Pet as PetModel, Customer as CustomerModel


router=APIRouter()

class PetBase(BaseModel):
    name: str = Field(min_length=2)
    animal: str= Field(min_length=3)
    breed: str = Field(min_length=3)
    age: int

class PetCreate(PetBase):
    customer_id: str

class Pet(PetBase):
    id: str
    customer_id: str
#esto seria para transformarlo en orm objeto sino seria un dict. es para no convertir a dict
    class Config:
        orm_mode = True

class PetUpdate(BaseModel):
    name: Optional[str] = None
    animal: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None

@router.post("/", response_model=Pet, status_code=201)
def create_pet(pet: PetCreate, db: Session = Depends(get_db)):
    # primero necesito sabe si existe el cliente
    owner = db.query(CustomerModel).filter(CustomerModel.id == pet.customer_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_pet = PetModel(
        id=str(uuid.uuid4()),
        name=pet.name,
        animal=pet.animal,
        breed=pet.breed,
        age=pet.age,
        customer_id=pet.customer_id
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

@router.get("/by-customer/{id_customer}", response_model=List[Pet])
def get_pets_by_customer(id_customer: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id_customer).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.pets 

@router.get("/{id_pet}", response_model=Pet)
def get_pet_by_id(id_pet: str, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == id_pet).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.delete("/{id_pet}")
def delete_pet(id_pet: str, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == id_pet).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"message": "Pet deleted"}

@router.patch("/{id_pet}", response_model=Pet)
def update_pet(id_pet: str, pet_update: PetUpdate, db: Session = Depends(get_db)):
    pet = db.query(PetModel).filter(PetModel.id == id_pet).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    update_data = pet_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pet, key, value)

    db.commit()
    db.refresh(pet)
    return pet

# @router.get("/")
# async def mascotas():
#     return{"mascotas":"mascotas"}
