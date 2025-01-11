from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse, HTMLResponse
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter(
    prefix="/whats/bot",
    tags=[],
    dependencies=[],
    responses={404: {"description": "whatsapp bot not found"}},
)


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        incoming_message = form_data.get("Body", "").strip()  # User's message
        sender = form_data.get("From", "")  # User's WhatsApp number

        # Initialize response
        response = MessagingResponse()
        reply = ""

        print("incoming message is", incoming_message)

        # Handle incoming messages
        if "recommendation" in incoming_message.lower():
            reply = "Sure! What product category are you interested in?"
        elif "laptops" in incoming_message.lower():
            reply = "<b>We recommend the XYZ Laptop. It has great specs for its price</b>!"
            # message = response.message("Our top pick for laptops:")
            # message.media("https://example.com/abc-laptop-image.jpg")  # Replace with your image URL
            # message.body(
            #     "*ABC Laptop*\n"
            #     "⚡ Powerful processor and sleek design.\n"
            #     "🖥️ Crystal-clear display.\n\n"
            #     "👉 [Learn More](https://example.com/abc-laptop)"
            # )
        else:
            reply = "I'm sorry, I didn't understand that. Can you rephrase?"

        # Send the reply
        response.message(reply)
        return HTMLResponse(str(response), media_type="application/xml")
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


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
    print(":the post rquest is", request.body)
    return "hola!"
