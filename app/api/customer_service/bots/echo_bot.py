# bot imports
from botbuilder.core import ActivityHandler, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes, Attachment

# system imports
import json
import os
import asyncio
import aiohttp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INTRO_CARD_TEMPLATE_FILE_PATH = os.path.join(
    BASE_DIR, "../utilities/bot_templates/IntroCardTemplate.json"
)


class MyBot(ActivityHandler):

    def __init__(self):
        super().__init__()
        self._typing_task = asyncio.Event()

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            action_value = turn_context.activity.value.get("action")
            await self._add_typing_activity(turn_context=turn_context)

            if action_value == "imBack":
                # user_message = Activity(
                #     type=ActivityTypes.message,
                #     from_property=turn_context.activity.from_property,
                #     text="action_value",

                #     # recipient=turn_context.activity.recipient
                # )

                # await turn_context.send_activity(user_message)
                await turn_context.send_activity(
                    "Sure, Let's get started. Please provide me some inputs on which you need information"
                )

        else:

            # if (
            #     turn_context.activity.attachments
            #     and len(turn_context.activity.attachments) > 0
            # ):
            #     await self.handle_attachments(turn_context)
            # else:
            await self._add_typing_activity(turn_context=turn_context)
            try:
                http_response = await self._fetch_data(turn_context.activity.text)
            finally:
                await self._stop_typing_activity()

            await turn_context.send_activity(http_response)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(f"Hi there")

                # await turn_context.send_activity(
                #     f"Welcome to the Customer Chat Service"
                # )

                await self.send_intro_card(turn_context=turn_context)

    async def handle_attachments(self, turn_context: TurnContext):
        for attachement in turn_context.activity.attachments:
            print(attachement)

    async def send_intro_card(self, turn_context: TurnContext):
        template_json = ""
        with open(INTRO_CARD_TEMPLATE_FILE_PATH, "r") as file:
            template_json = json.load(file)

        intro_card = Activity(attachments=[CardFactory.adaptive_card(template_json)])

        await turn_context.send_activity(intro_card)

    async def _stop_typing_activity(self):
        if self._typing_task:
            self._typing_task.cancel()
            try:
                await self._typing_task  # Ensure the task is awaited to handle cancellation
            except asyncio.CancelledError:
                pass  # Expected when the task is canceled
            self._typing_task = None  # Reset the reference

    async def _add_typing_activity(self, turn_context: TurnContext):

        async def send_typing_activity():
            try:
                while True:
                    typing_activity = Activity(type=ActivityTypes.typing)
                    await turn_context.send_activity(typing_activity)
                    await asyncio.sleep(2)  # Short interval for better UX
            except asyncio.CancelledError:
                # Exit the loop gracefully when the task is canceled
                pass

        # Create the typing task
        self._typing_task = asyncio.create_task(send_typing_activity())

    async def _fetch_data(self, query: str):
        api_url = f"http://18.209.65.205:5000/api/answer?collectionName=polaris&input=${query}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    print("the resposne is", response)
                    if response.status == 200:
                        data = await response.json()
                        return data.get("answer", "")
                    else:
                        return "Something went wrong!"
            except Exception as e:
                return "Unable to process the request"
