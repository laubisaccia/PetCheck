from fastapi import FastAPI,Depends


import api.auth
import api.pets.endpoint
import api.customers.endpoint
import api.appointments.endpoint
import api.auth.endpoint
import api.doctors.endpoint
from api.auth.endpoint import BearerJWT
from api.core.database import Session,engine,Base
from api.core.models import Customer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Pet Check",
    description="PetCheck is a web application for facilities that provide pet care services. It allows staff to register users and pets, schedule check-ups, and manage medical records.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

prefix_base= "/api/v1"
app.include_router(api.auth.endpoint.router, prefix=f"{prefix_base}",tags=["login"])
app.include_router(api.customers.endpoint.router,prefix=f"{prefix_base}/customers",tags=["customers"],dependencies=[Depends(BearerJWT())])
app.include_router(api.pets.endpoint.router, prefix=f"{prefix_base}/pets",tags=["pets"])
app.include_router(api.appointments.endpoint.router, prefix=f"{prefix_base}/appointments",tags=["appointments"])
app.include_router(api.doctors.endpoint.router, prefix=f"{prefix_base}/doctors",tags=["doctors"])


