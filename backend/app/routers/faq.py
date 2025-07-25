from app.models.schemas import FAQ
from app.services.faq_service import get_faqs
from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_model=list[FAQ])
def get_faq_list():
    return get_faqs()
