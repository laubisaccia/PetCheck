
from fastapi import APIRouter,Request,HTTPException
from pydantic import BaseModel,Field,EmailStr
from api.user_jwt import createToken,validateToken
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

router=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self,request:Request):
        auth=await super().__call__(request)
        data=validateToken(auth.credentials)
        if data["email"]!= "laubisaccia@gmail.com":
            raise HTTPException(status_code=403,detail="Wrong credentials")

class User(BaseModel):
    email:EmailStr
    password:str


@router.post("/login")
def login(user:User):
    if user.email=="laubisaccia@gmail.com" and user.password=="123":
        token:str=createToken(user.model_dump())
        print(token)
        return JSONResponse(content=token)
