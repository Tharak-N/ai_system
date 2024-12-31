
# bot imports
from botbuilder.core import ( 
  ActivityHandler, 
  TurnContext, 
  CardFactory 
)
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes

# system imports 
import json
import os
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTRO_CARD_TEMPLATE_FILE_PATH = os.path.join(BASE_DIR, '../utilities/bot_templates/IntroCardTemplate.json')

class MyBot(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            action_value = turn_context.activity.value.get("action")
            # await turn_context.send_activity(
            #     Activity(
            #         type=ActivityTypes.message,
            #         text=action_value,
            #         from_property=turn_context.activity.from_property,  
            #         recipient=turn_context.activity.recipient          
            #     )
            # )
            # await turn_context.send_activity(user_message.text)
            if action_value == "get_started":
                await self._add_typing_activity(turn_context=turn_context)
                await turn_context.send_activity("Sure, Let's get started. Please provide me some inputs on which you need information")
        
        else:
            await self._add_typing_activity(turn_context=turn_context)
            # add the RAG over here
            await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Hi there, {member.name}"
                )

                # await turn_context.send_activity(
                #     f"Welcome to the Customer Chat Service"
                # )

                await self.send_intro_card(turn_context=turn_context)

    async def send_intro_card(self, turn_context: TurnContext):
        template_json = ""
        with open(INTRO_CARD_TEMPLATE_FILE_PATH, 'r') as file:
            template_json = json.load(file)

        intro_card = Activity(
            attachments=[CardFactory.adaptive_card(template_json)]
        )

        await turn_context.send_activity(intro_card)

    async def _add_typing_activity(self, turn_context: TurnContext):
        typing_activity = Activity(type=ActivityTypes.typing)
        await turn_context.send_activity(typing_activity)
        await asyncio.sleep(0.2)