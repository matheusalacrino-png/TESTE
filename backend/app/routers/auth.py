from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.db import get_db
from app.models import Company, User
from app.schemas import Token, UserLogin, UserRegister


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='E-mail já cadastrado')

    company = Company(
        name=payload.company_name,
        whatsapp_number=payload.whatsapp_number,
    )
    db.add(company)
    db.flush()

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        company_id=company.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return Token(access_token=create_access_token(str(user.id)))


@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Credenciais inválidas')

    return Token(access_token=create_access_token(str(user.id)))
