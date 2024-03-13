import hashlib
import hmac
from typing import Union

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/up")
async def read_root():
    return {
        "message": "Service is healthy",
    }


WEBHOOK_SECRET = "lin_wh_39JXATaYOqEsGJlPOyiw121RUgPsFaINmcwdGFCa8pqV"


@app.post("/webhook")
async def webhook_handler(event: Union[dict, list], request: Request):
    digest = hmac.new(bytes(WEBHOOK_SECRET, 'UTF-8'),
                      bytes(event, 'UTF-8'), hashlib.sha256)
    signature = digest.hexdigest()

    if signature != request.headers.get('linear-signature'):
        return {
            "message": "Invalid signature",
            "event": event
        }

    return {
        "message": "Webhook received",
        "event": event
    }
