
from fastapi import APIRouter,Request,HTTPException, status,Depends,Body
from pydantic import BaseModel,Field,EmailStr
from api.user_jwt import createToken,validateToken
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from api.core.database import Base
from api.core.database import get_db,Session
from api.core.models import UserDB
import uuid


router=APIRouter()

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        try:
            data = validateToken(auth.credentials) 
            return auth.credentials  
        except Exception:
            raise HTTPException(status_code=403, detail="Token inválido")

def get_current_user(token: str = Depends(BearerJWT()), db: Session = Depends(get_db)):
    data = validateToken(token)
    user = db.query(UserDB).filter(UserDB.email == data["email"]).first()
    if not user:
        raise HTTPException(status_code=403, detail="Usuario no encontrado")
    return user

def get_current_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="No autorizado: se requiere admin role")
    return user

def get_current_employee(user=Depends(get_current_user)):
    if user.role not in ["employee", "admin"]:
        raise HTTPException(status_code=403, detail="No autorizado: se requiere empleado o admin")
    return user

class User(BaseModel):
    email:EmailStr
    password:str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # admin o employee
    role: str  


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectas")

    token: str = createToken({"email": db_user.email, "role": db_user.role})
    return JSONResponse(content=token)
