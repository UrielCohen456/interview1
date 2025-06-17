from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def get_ip(request: Request):
    # Incase we are sitting behind a proxy such as nginx-ingress
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # The first index passed by nginx header is the original requester's ip
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return ip
