from fastapi import APIRouter,Depends

router=APIRouter()

@router.get("/")
async def mascotas():
    return{"mascotas":"mascotas"}