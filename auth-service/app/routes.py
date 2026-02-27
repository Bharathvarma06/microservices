from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, auth

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = auth.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created"}

@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user or not auth.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token({"sub": user.username})
    return {"access_token": token}
