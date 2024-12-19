
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.customer_service import main as customer_service_module

app = FastAPI()

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