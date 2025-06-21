import uuid
from api.core.database import Session, engine, Base, get_db
from api.core.models import UserDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_admin():
    Base.metadata.create_all(bind=engine)

    db = Session(bind=engine)
    email_admin = "admin@petshop.com"  
    password_admin = "admin123"        

    existing = db.query(UserDB).filter(UserDB.email == email_admin).first()
    if existing:
        print("Admin ya existe")
        return

    hashed_pw = get_password_hash(password_admin)
    admin = UserDB(
        id=str(uuid.uuid4()),
        email=email_admin,
        hashed_password=hashed_pw,
        role="admin"
    )
    db.add(admin)
    db.commit()
    print(f"Admin creado con email: {email_admin} y contraseña: {password_admin}")

if __name__ == "__main__":
    create_admin()
