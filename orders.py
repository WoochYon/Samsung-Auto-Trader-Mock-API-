import config
from api_client import safe_request
from logger import get_logger

logger = get_logger("orders")

def place_order(symbol: str, price: int, qty: int, is_buy: bool) -> bool:
    """Places a mock limit order."""
    order_type = "Buy" if is_buy else "Sell"
    tr_id = config.TR_ID_BUY if is_buy else config.TR_ID_SELL
    
    payload = {
        "CANO": config.CANO,
        "ACNT_PRDT_CD": config.ACNT_PRDT_CD,
        "PDNO": symbol,
        "ORD_DVSN": "00", # 00 = Limit order
        "ORD_QTY": str(qty),
        "ORD_UNPR": str(price)
    }
    
    logger.info(f"Placing {order_type} Order: {qty} shares of {symbol} at {price:,} KRW")
    
    data = safe_request("POST", config.EP_ORDER, tr_id, payload=payload)
    
    if data.get("rt_cd") == "0":
        logger.info(f"{order_type} order request successful. Msg: {data.get('msg1')}")
        return True
    else:
        logger.error(f"{order_type} order failed.")
        return False
