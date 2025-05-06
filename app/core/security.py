from typing import Optional

from fastapi import Header, HTTPException, status

from app.core.config import config


from fastapi import Header, HTTPException, status
from typing import Optional
from app.core.config import config


async def get_api_key(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("ApiKey "):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key"
        )

    key = authorization.removeprefix("ApiKey ").strip()
    if key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or missing API key"
        )

    return key
