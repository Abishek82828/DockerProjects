from fastapi import FastAPI, Request
from datetime import datetime
import os

app = FastAPI()

LOG_PATH = os.getenv("LOG_PATH", "/logs/requests.log")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/inspect")
async def inspect(request: Request):
    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")
    ua = request.headers.get("user-agent", "unknown")
    now = datetime.utcnow().isoformat() + "Z"

    line = f"{now} ip={client_ip} ua={ua}\n"
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

    return {
        "time_utc": now,
        "client_ip": client_ip,
        "method": request.method,
        "path": str(request.url.path),
        "user_agent": ua,
        "headers_sample": {
            "host": request.headers.get("host"),
            "accept": request.headers.get("accept"),
        },
    }
