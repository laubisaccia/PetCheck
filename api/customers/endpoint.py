from fastapi import APIRouter,Depends,HTTPException,Body
from pydantic import BaseModel,Field,EmailStr
from typing import Optional, List
from fastapi.responses import JSONResponse
import uuid
from api.core.database import get_db
from sqlalchemy.orm import Session
from api.core.models import Customer as CustomerModel


router=APIRouter()

class Customer(BaseModel):
    id: str
    firstName: str=Field(default="First Name", min_length=3)
    lastName: str = Field(default="Last Name", min_length=3)
    email: EmailStr 
    phone: int = Field(..., ge=1000000, le=9999999999)

#para usar patch
class CustomerUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None

#para solucionar el problema del id hice este modelo
class CustomerCreate(BaseModel):
    firstName: str = Field(default="First Name", min_length=3)
    lastName: str = Field(default="Last Name", min_length=3)
    email: EmailStr
    phone: int = Field(..., ge=1000000, le=9999999999)

customers: List[dict] = [
    {
        "id": str(uuid.uuid4()),
        "firstName": "Laura",
        "lastName": "Pérez",
        "email": "laura@example.com",
        "phone": 123456789
    },
    {
        "id": str(uuid.uuid4()),
        "firstName": "Carlos",
        "lastName": "Gómez",
        "email": "carlos@example.com",
        "phone": 987654321
    }
]



@router.get("/",response_model=List[Customer])
async def get_customers(db: Session = Depends(get_db)):
    customers = db.query(CustomerModel).all()
    return customers

@router.get("/{id_customer}", response_model=Customer)
async def get_customer_by_id(id_customer: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id_customer).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


#model dump es dict
#es un metodo pydantic para validar datos basemodel. Customer es objeto de python pero se guardan
#en diccionarios no objetos entonces modeldump lo convierte


@router.post("/", response_model=Customer, status_code=201)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = CustomerModel(
        id=str(uuid.uuid4()),
        firstName=customer.firstName,
        lastName=customer.lastName,
        email=customer.email,
        phone=customer.phone,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer 


@router.put("/{id_customer}", response_model=Customer)
async def update_customer(id_customer: str, updated_customer: CustomerCreate, db: Session = Depends(get_db)):
    customer_db = db.query(CustomerModel).filter(CustomerModel.id == id_customer).first()
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_db.firstName = updated_customer.firstName
    customer_db.lastName = updated_customer.lastName
    customer_db.email = updated_customer.email
    customer_db.phone = updated_customer.phone

    db.commit()
    db.refresh(customer_db)
    return customer_db


@router.patch("/{id_customer}", response_model=Customer)
async def patch_customer(id_customer: str, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    customer_db = db.query(CustomerModel).filter(CustomerModel.id == id_customer).first()
    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_update.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
        #puedo cambiar el valor de uno pero sin saber el nombre
        setattr(customer_db, key, value)

    db.commit()
    db.refresh(customer_db)
    return customer_db

@router.delete("/{id_customer}")
async def delete_customer(id_customer: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id_customer).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}




