import hashlib
import hmac

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/up")
async def read_root():
    return {
        "message": "Service is healthy",
    }


# WEBHOOK_SECRET = "lin_wh_39JXATaYOqEsGJlPOyiw121RUgPsFaINmcwdGFCa8pqV"

WEBHOOK_SECRET = "lin_wh_g14SfvkEZOnkwQJSIE4o5SNOSK4QntPyENSg66nXjkOM"


@app.post("/webhook")
async def webhook_handler(request: Request):
    rawBody = await request.body()
    rawBody = rawBody.decode('utf-8')
    body = await request.json()

    digest = hmac.new(
        bytes(WEBHOOK_SECRET, 'UTF-8'),
        msg=bytes(rawBody, 'UTF-8'),
        digestmod=hashlib.sha256)

    signature = digest.hexdigest()

    if signature != request.headers.get('linear-signature'):
        return {
            "message": "Invalid signature"
        }

    return {
        "message": "Webhook received",
        "data": body,
    }
