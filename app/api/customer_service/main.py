

from fastapi import APIRouter
from .endpoints import local_llm

router = APIRouter(
  prefix="/customer-service",
  tags=["customer-service"],
  dependencies=[],
  responses={404: {"description": "Customer service not found"}}
)

router.include_router(local_llm.router)

