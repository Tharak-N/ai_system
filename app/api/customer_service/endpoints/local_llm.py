
from openai import OpenAI

from fastapi import APIRouter, Response, HTTPException
from fastapi.responses import StreamingResponse
from app.models.model import Phi3Model
import asyncio

router = APIRouter(
  prefix="/local/phi3",
  tags=["phi3"],
  dependencies=[]
)


@router.post("/", response_class=StreamingResponse)
async def local_phi3_response(body: Phi3Model):

  client = OpenAI(base_url="http://192.168.134.233:1235/v1/", api_key="llm-studio")

  try:
    completion = client.chat.completions.create(
      model="llama-3.2-1b-instruct",
      messages=[
            {"role": "system", "content": "You are an AI assistant who answers to the user query"},
      {"role": "user", "content": body.prompt }
      ],
      stream=True
    )

    async def async_generator():
      for chunk in completion: 
        if hasattr(chunk, "choices") and len(chunk.choices) > 0:
          delta = chunk.choices[0].delta  # Access delta as an attribute, not a dictionary
          content = getattr(delta, "content", "")  # Safely access content attribute
          if content:
            await asyncio.sleep(0.1)
            yield content
      
    return StreamingResponse(
      async_generator(), 
      media_type="text/plain", 
    )
  except Exception as e: 
    raise HTTPException(status_code=500, detail=str(e))

  