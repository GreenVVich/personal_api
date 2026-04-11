from fastapi import Request, HTTPException
from app.core.config import ALLOWED_IPS

def check_ip(request: Request):
    if request.client.host not in ALLOWED_IPS:
        raise HTTPException(403)
