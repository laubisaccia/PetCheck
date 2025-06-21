from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.models import UserDB
from api.auth.endpoint import get_current_admin, get_password_hash
from pydantic import BaseModel, EmailStr
import uuid

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  

class UserOut(BaseModel):
    email: EmailStr
    role: str

@router.post("/", response_model=UserOut, dependencies=[Depends(get_current_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    hashed_pw = get_password_hash(user.password)
    new_user = UserDB(id=str(uuid.uuid4()),email=user.email, hashed_password=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
