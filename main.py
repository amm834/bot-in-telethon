from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/up")
async def read_root():
    return {
        "message": "Service is healthy",
    }


@app.post("/webhook")
async def webhook_handler(event: Union[dict, list]):
    return {
        "message": "Webhook received",
        "event": event
    }
