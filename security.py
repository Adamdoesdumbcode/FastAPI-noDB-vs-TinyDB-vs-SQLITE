# security.py
from config import API_KEYCFG, DEV_KEYCFG
from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader


# STATIC STRONG KEYS
API_KEY = API_KEYCFG
DEV_KEY = DEV_KEYCFG

# API Key dependencies
api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)
dev_key_header = APIKeyHeader(name="x-dev-key", auto_error=True)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

async def get_dev_key(dev_key: str = Depends(dev_key_header)):
    if dev_key != DEV_KEY:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid DEV Key"
        )
    return dev_key
