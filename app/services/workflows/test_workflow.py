# llama index imports
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step
from llama_index.llms.openai import OpenAI


class Events(Event):
    text: str


class WorkflowStarter(Workflow):
    llm = OpenAI()

    @step
    async def generate_text(self, ev: StartEvent) -> Events:
        llm_response = await llm.acomplete("tell me about swami vivekananda")
        return Events(text=str(llm_response))

    @step
    async def validating_output(self, ev: Events) -> StopEvent:
        context = ev.text

        prompt = f"Given a output response of about swami vivekananda, validate it and make it concise {context}"
        response = await self.llm.acomplete(prompt)

        return StopEvent(result=str(response))


w = WorkflowStarter(verbose=True)
w.run(topic="tell me about swami vivekananda")
