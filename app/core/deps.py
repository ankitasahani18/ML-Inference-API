from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = verify_token(credentials.credentials)
        return payload["sub"]

    except:
        raise HTTPException(status_code=401, detail="Invalid token")