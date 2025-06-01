from fastapi import FastAPI,Depends


import api.auth
import api.pets.endpoint
import api.customers.endpoint
import api.reservas.endpoint
import api.auth.endpoint
from api.auth.endpoint import BearerJWT
from api.core.database import Session,engine,Base
from api.core.models import Customer


app = FastAPI(
    title="Pet Check",
    description="PetCheck is a web application for facilities that provide pet care services. It allows staff to register users and pets, schedule check-ups, and manage medical records.",
    version="0.0.1"
)

Base.metadata.create_all(bind=engine)

prefix_base= "/api/v1"
app.include_router(api.auth.endpoint.router, prefix=f"{prefix_base}/login",tags=["login"])
app.include_router(api.customers.endpoint.router,prefix=f"{prefix_base}/customers",tags=["customers"],dependencies=[Depends(BearerJWT())])
app.include_router(api.pets.endpoint.router, prefix=f"{prefix_base}/pets",tags=["pets"])
app.include_router(api.reservas.endpoint.router, prefix=f"{prefix_base}/reservas",tags=["reservas"])


