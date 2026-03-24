from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Company, User
from app.schemas import GoogleReviewLinkOut, WhatsAppTemplatePayload
from app.services.google_business import build_review_link, fetch_place_details
from app.services.whatsapp import send_review_template


router = APIRouter(prefix='/integrations', tags=['Integrations'])


@router.get('/google/review-link', response_model=GoogleReviewLinkOut)
def get_google_review_link(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    company = db.query(Company).filter(Company.id == user.company_id).first()

    if company.google_review_url:
        return GoogleReviewLinkOut(place_id=company.google_place_id, review_url=company.google_review_url)

    if not company.google_place_id:
        raise HTTPException(status_code=400, detail='Configure google_place_id ou google_review_url')

    review_url = build_review_link(company.google_place_id)
    company.google_review_url = review_url
    db.add(company)
    db.commit()

    return GoogleReviewLinkOut(place_id=company.google_place_id, review_url=review_url)


@router.get('/google/place-details')
def get_place_details(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company.google_place_id:
        raise HTTPException(status_code=400, detail='Configure google_place_id')
    return fetch_place_details(company.google_place_id)


@router.post('/whatsapp/send-template')
def send_whatsapp_template(
    payload: WhatsAppTemplatePayload,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    company = db.query(Company).filter(Company.id == user.company_id).first()
    review_link = company.google_review_url or ''

    try:
        result = send_review_template(
            to=payload.to,
            customer_name=payload.customer_name,
            company_name=payload.company_name,
            review_link=review_link,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f'Falha no envio WhatsApp: {exc}') from exc

    return {'status': 'sent', 'provider_response': result}
