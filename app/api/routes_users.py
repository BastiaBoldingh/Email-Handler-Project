from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import hash_password, verify_password_hash, create_access_token, verify_token
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.models.db_models import User

router = APIRouter()

def check_email(email: str, db: Session = Depends(get_db)):
    if db.execute(select(User).filter(User.email == email)).scalar():
        return True
    else:
        return False



@router.post("/register")
def register(email: str, username: str, password: str, db: Session = Depends(get_db)):
    if check_email(email):
        raise HTTPException(status_code=400, detail="Already an account with this email")
    hashed_password = hash_password(password)
    new_user = User(
        email=email,
        password=hashed_password,
        username=username,
    )
    db.add(new_user)
    db.commit()
    return {"msg": "user created"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.email == email)).scalar()
    if not user or not verify_password_hash(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}
