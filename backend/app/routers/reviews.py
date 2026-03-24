from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import RequestStatus, ReviewRequest, User
from app.schemas import DashboardMetrics, ReviewRequestCreate, ReviewRequestOut, ReviewResponseIn


router = APIRouter(prefix='/reviews', tags=['Reviews'])


@router.post('/requests', response_model=ReviewRequestOut)
def create_request(
    payload: ReviewRequestCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    request = ReviewRequest(
        company_id=user.company_id,
        customer_name=payload.customer_name,
        customer_whatsapp=payload.customer_whatsapp,
        service_name=payload.service_name,
        status=RequestStatus.pending,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.get('/requests', response_model=list[ReviewRequestOut])
def list_requests(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return (
        db.query(ReviewRequest)
        .filter(ReviewRequest.company_id == user.company_id)
        .order_by(ReviewRequest.id.desc())
        .all()
    )


@router.post('/requests/{request_id}/respond', response_model=ReviewRequestOut)
def respond_request(
    request_id: int,
    payload: ReviewResponseIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    request = (
        db.query(ReviewRequest)
        .filter(ReviewRequest.id == request_id, ReviewRequest.company_id == user.company_id)
        .first()
    )
    if not request:
        raise HTTPException(status_code=404, detail='Solicitação não encontrada')

    request.stars = payload.stars
    request.comment = payload.comment

    if payload.stars <= 2:
        if not payload.comment:
            raise HTTPException(status_code=400, detail='Feedback obrigatório para 1-2 estrelas')
        request.status = RequestStatus.internal
    else:
        request.status = RequestStatus.google

    db.add(request)
    db.commit()
    db.refresh(request)
    return request


@router.get('/dashboard', response_model=DashboardMetrics)
def dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items = db.query(ReviewRequest).filter(ReviewRequest.company_id == user.company_id).all()

    total = len(items)
    rated = [item for item in items if item.stars is not None]
    positive = [item for item in rated if item.stars >= 3]
    critical = [item for item in rated if item.stars <= 2]
    pending = [item for item in items if item.status == RequestStatus.pending]
    average = sum(item.stars for item in rated) / len(rated) if rated else 0

    return DashboardMetrics(
        total_requests=total,
        rated=len(rated),
        average=round(average, 1),
        positive_rate=round((len(positive) / len(rated) * 100), 1) if rated else 0,
        critical_count=len(critical),
        pending=len(pending),
    )
