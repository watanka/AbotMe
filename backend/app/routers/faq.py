from fastapi import APIRouter
from app.models.schemas import FAQ
from app.services.faq_service import get_faqs

router = APIRouter()


@router.get("/", response_model=list[FAQ])
def get_faq_list():
    return get_faqs()
