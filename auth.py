import os
import json
import requests
from datetime import datetime, timedelta
import config
from logger import get_logger

logger = get_logger("auth")
TOKEN_FILE = "token_cache.json"

def get_access_token() -> str:
    """Retrieves token from cache if valid, otherwise fetches a new one."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            try:
                cache = json.load(f)
                expiry = datetime.fromisoformat(cache["expiry"])
                # If current time is before expiry (with 1 hr buffer), reuse token
                if datetime.now() < (expiry - timedelta(hours=1)):
                    logger.info("Reusing cached API token.")
                    return cache["token"]
            except Exception as e:
                logger.warning(f"Failed to read token cache: {e}. Fetching new token.")

    logger.info("Fetching new API token...")
    url = f"{config.BASE_URL}{config.EP_TOKEN}"
    payload = {
        "grant_type": "client_credentials",
        "appkey": config.APP_KEY,
        "appsecret": config.APP_SECRET
    }
    
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    token = data["access_token"]
    # KIS tokens typically expire in 24 hours. We save the expiry limit.
    expires_in = data.get("expires_in", 86400) 
    expiry_time = datetime.now() + timedelta(seconds=expires_in)
    
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "token": token,
            "expiry": expiry_time.isoformat()
        }, f)
        
    logger.info(f"New token generated. Expires at {expiry_time}")
    return token
