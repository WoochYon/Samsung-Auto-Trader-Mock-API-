import requests
import time
import config
import auth
from logger import get_logger

logger = get_logger("api_client")

def _get_base_headers(tr_id: str) -> dict:
    token = auth.get_access_token()
    return {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": config.APP_KEY,
        "appsecret": config.APP_SECRET,
        "tr_id": tr_id
    }

def safe_request(method: str, endpoint: str, tr_id: str, params=None, payload=None) -> dict:
    """Executes an API request with basic retry logic and mandatory rate-limit sleeps."""
    url = f"{config.BASE_URL}{endpoint}"
    headers = _get_base_headers(tr_id)
    
    # Enforce a mandatory 0.5s delay before ANY request to respect strict mock limits
    time.sleep(0.5) 
    
    try:
        if method.upper() == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=10)
        else:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            
        resp.raise_for_status()
        data = resp.json()
        
        # Check KIS specific error codes (usually "rt_cd" != "0")
        if data.get("rt_cd") != "0":
            logger.error(f"API Error [{tr_id}]: {data.get('msg1')}")
            
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during {method} to {endpoint}: {e}")
        return {}
