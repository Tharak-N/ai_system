
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter(
    prefix="/whats/bot",
    tags=[],
    dependencies=[],
    responses={404: {"description": "whatsapp bot not found"}},
)


@router.get("/")
async def whatsapp_bot(request: Request) -> str:
    verification_token = "narayana"
    
    hub = request.query_params
    mode = hub.get("hub.mode")
    challenge = hub.get("hub.challenge")
    verify_token = hub.get("hub.verify_token")

    if verify_token == verification_token:
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        return PlainTextResponse(content="Verification failed", status_code=403)

    # return "hitted"


@router.post("/")
async def whatsapp_bot(request: Request):
    print(":the post rquest is", request)
    pass