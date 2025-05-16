from fastapi import APIRouter,Depends

router=APIRouter()

@router.get("/")
async def clientes():
    return{"clientes":"clientes"}