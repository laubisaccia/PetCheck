from fastapi import FastAPI,Depends

import api.auth
import api.pets.endpoint
import api.customers.endpoint
import api.appointments.endpoint
import api.auth.endpoint
import api.doctors.endpoint
import api.users.endpoint
from api.core.database import engine,Base
from fastapi.middleware.cors import CORSMiddleware
from api.auth.endpoint import get_current_user, get_current_admin

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
app.include_router(api.customers.endpoint.router,prefix=f"{prefix_base}/customers",tags=["customers"],dependencies=[Depends(get_current_user)])
app.include_router(api.pets.endpoint.router, prefix=f"{prefix_base}/pets",tags=["pets"],dependencies=[Depends(get_current_user)])
app.include_router(api.appointments.endpoint.router, prefix=f"{prefix_base}/appointments",tags=["appointments"],dependencies=[Depends(get_current_user)])
app.include_router(api.doctors.endpoint.router, prefix=f"{prefix_base}/doctors",tags=["doctors"],dependencies=[Depends(get_current_user)])
app.include_router(api.users.endpoint.router, prefix=f"{prefix_base}/users",tags=["users"],dependencies=[Depends(get_current_admin)])


