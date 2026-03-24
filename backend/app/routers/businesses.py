from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Company, User
from app.schemas import CompanyOut, CompanyUpdate, MeOut


router = APIRouter(prefix='/business', tags=['Business'])


@router.get('/me', response_model=CompanyOut)
def get_my_company(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    company = db.query(Company).filter(Company.id == user.company_id).first()
    return company


@router.patch('/me', response_model=CompanyOut)
def update_my_company(
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.id == user.company_id).first()
    data = payload.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(company, key, value)

    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get('/me/user', response_model=MeOut)
def get_me(user: User = Depends(get_current_user)):
    return user
