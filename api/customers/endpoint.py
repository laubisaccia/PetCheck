from fastapi import APIRouter,Depends,HTTPException,Body
from pydantic import BaseModel,Field,EmailStr
from typing import Optional, List
from fastapi.responses import JSONResponse
import uuid

router=APIRouter()

class Customer(BaseModel):
    id: str
    first_name: str=Field(default="First Name", min_length=3)
    last_name: str = Field(default="Last Name", min_length=3)
    email: EmailStr 
    phone: int = Field(..., ge=1000000, le=9999999999)

#para usar patch
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[int] = None

#para solucionar el problema del id hice este modelo
class CustomerCreate(BaseModel):
    first_name: str = Field(default="First Name", min_length=3)
    last_name: str = Field(default="Last Name", min_length=3)
    email: EmailStr
    phone: int = Field(..., ge=1000000, le=9999999999)

customers: List[dict] = [
    {
        "id": str(uuid.uuid4()),
        "first_name": "Laura",
        "last_name": "Pérez",
        "email": "laura@example.com",
        "phone": 123456789
    },
    {
        "id": str(uuid.uuid4()),
        "first_name": "Carlos",
        "last_name": "Gómez",
        "email": "carlos@example.com",
        "phone": 987654321
    }
]



@router.get("/",response_model=List[Customer])
async def get_customers():
    return customers

@router.get("/{id_customer}", response_model=Customer)
async def get_customer_by_id(id_customer: str):
    for customer in customers:
        if customer["id"] == id_customer:
            return customer
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



#model dump es dict
#es un metodo pydantic para validar datos basemodel. Customer es objeto de python pero se guardan
#en diccionarios no objetos entonces modeldump lo convierte


@router.post("/",response_model=Customer)
async def create_customer(customer: CustomerCreate):
    customer_data = customer.model_dump()
    customer_data["id"] = str(uuid.uuid4())
    customers.append(customer_data)
    return JSONResponse(
        content={
            "message": "New customer was added",
            "customers": customers
        },
        status_code=201
    )

@router.put("/{id_customer}", response_model=Customer)
async def update_customer(id_customer: str, updated_customer: CustomerCreate):
    for i, customer in enumerate(customers):
        if customer["id"] == id_customer:
            updated_data = updated_customer.model_dump()
            updated_data["id"] = id_customer 
            customers[i] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Customer not found")

@router.patch("/{id_customer}", response_model=Customer)
async def patch_customer(id_customer: str, customer_update: CustomerUpdate):
    for customer in customers:
        if customer["id"] == id_customer:
            update_data = customer_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                customer[key] = value
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@router.delete("/{id_customer}")
async def delete_customer(id_customer: str):
    for i, customer in enumerate(customers):
        if customer["id"] == id_customer:
            customers.pop(i)
            return {"message": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")






