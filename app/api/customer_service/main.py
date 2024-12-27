

from fastapi import APIRouter
from .routes import local_llm, teams_bot

router = APIRouter(
  prefix="/customer-service",
  tags=["customer-service"],
  dependencies=[],
  responses={404: {"description": "Customer service not found"}}
)

router.include_router(local_llm.router)
router.include_router(teams_bot.router)
