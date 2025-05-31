from fastapi import FastAPI


import api.mascotas.endpoint
import api.customers.endpoint
import api.reservas.endpoint

app = FastAPI(
    title="Pet Check",
    description="PetCheck is a web application for facilities that provide pet care services. It allows staff to register users and pets, schedule check-ups, and manage medical records.",
    version="0.0.1"
)

prefix_base= "/api/v1"
app.include_router(api.customers.endpoint.router, prefix=f"{prefix_base}/customers",tags=["customers"])
app.include_router(api.mascotas.endpoint.router, prefix=f"{prefix_base}/mascotas",tags=["mascotas"])
app.include_router(api.reservas.endpoint.router, prefix=f"{prefix_base}/reservas",tags=["reservas"])


