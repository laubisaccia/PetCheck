from fastapi import APIRouter,Depends

router=APIRouter()

@router.get("/")
async def reservas():
    return{"reservas":"reservas"}