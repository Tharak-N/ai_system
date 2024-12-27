
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

from .api.customer_service import main as customer_service_module

import os

os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={os.environ.get("PHOENIX_API_KEY")}"

trace_provider = register(
  project_name="ai_system",
)

OpenAIInstrumentor().instrument(trace_provider=trace_provider)

app = FastAPI(
  title="AI System",
  description="An AI system for all POC's"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(customer_service_module.router)


@app.get("/")
def root():
  return "hola!"

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )