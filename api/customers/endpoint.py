from fastapi import APIRouter,Depends,HTTPException,Body
from pydantic import BaseModel
from typing import Optional


router=APIRouter()

class Customer(BaseModel):
    ID_customer: int
    first_name: str
    last_name: str
    email: str
    phone: int

#para usar patch
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None

customers = [
    {
        "ID_customer": 1,
        "first_name": "Laura",
        "last_name": "Pérez",
        "email": "laura@example.com",
        "phone": "123456789"
    },
    {
        "ID_customer": 2,
        "first_name": "Carlos",
        "last_name": "Gómez",
        "email": "carlos@example.com",
        "phone": "987654321"
    }
]

@router.get("/")
async def get_customers():
    return{"customers":customers}

@router.get("/{id_customer}")
async def get_customer_by_id(id_customer: int):
    for cust in customers:
        if cust["ID_customer"] == id_customer:
            return cust
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



#model dump es dict
@router.post("/")
async def create_customer(customer: Customer):
    customers.append(customer.model_dump())  
    return customer

@router.put("/{id_customer}")
async def update_customer(id_customer: int, updated_customer: Customer):
    for i, customer in enumerate(customers):
        if customer["ID_customer"] == id_customer:
            customers[i] = updated_customer.model_dump()
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found")

@router.patch("/{id_customer}")
async def patch_customer(id_customer: int, customer_update: CustomerUpdate):
    for customer in customers:
        if customer["ID_customer"] == id_customer:
            update_data = customer_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                customer[key] = value
            return customer
    raise HTTPException(status_code=404, detail="Customer not found")

@router.delete("/{id_customer}")
async def delete_customer(id_customer: int):
    for idx, customer in enumerate(customers):
        if customer["ID_customer"] == id_customer:
            customers.pop(idx)
            return {"message": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")






