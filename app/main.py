
from fastapi import FastAPI
from .api.customer_service import chat


app = FastAPI()


app.include_router(chat.router)


@app.get("/")
def root():
  return "hola!"