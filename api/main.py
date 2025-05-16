from fastapi import FastAPI


import api.mascotas.endpoint
import api.clientes.endpoint
import api.reservas.endpoint

app = FastAPI()

prefix_base= "/api/v1"
app.include_router(api.clientes.endpoint.router, prefix=f"{prefix_base}/clientes",tags=["Clientes"])
app.include_router(api.mascotas.endpoint.router, prefix=f"{prefix_base}/mascotas",tags=["Mascotas"])
app.include_router(api.reservas.endpoint.router, prefix=f"{prefix_base}/reservas",tags=["Reservas"])


