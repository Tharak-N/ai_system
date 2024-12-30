
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from aiohttp import web
# from aiohttp.web import , json_response
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
)

from datetime import datetime
from ..utilities.config import DefaultConfig
from ..bots.echo_bot import MyBot
from ..bots.conversation_bot import TeamsConversationBot

import traceback
import sys


router = APIRouter(
  prefix="/teams/bot",
  tags=[],
  dependencies=[],
  responses={404: {"description":"teams bot not found"}}
)


CONFIG = DefaultConfig()
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

BOT = MyBot()
CONVERSATION_BOT = TeamsConversationBot(app_id=CONFIG.APP_ID, app_password=CONFIG.APP_PASSWORD)

@router.post("/", response_model=None)
async def bot(request: Request):
    if "application/json" in request.headers["Content-Type"]:
        body = await request.json()
    else:
        return Response(status=415)
    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    print("the response from echo bot is", response)
    if response: 
        return JSONResponse(content=response.body, status_code=response.status)
    return JSONResponse(status_code=201, content={})

