

from fastapi import APIRouter

router = APIRouter(
  prefix="/customer_service",
  tags=["customer_service"],
  dependencies=[], 
)

@router.get('/')
async def chat():
  return ""