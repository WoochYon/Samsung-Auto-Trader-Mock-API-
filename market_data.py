import config
from api_client import safe_request
from logger import get_logger
from datetime import datetime, timedelta

logger = get_logger("market_data")

def get_market_data(symbol: str) -> dict:
    """Fetches the current price and volume data of a given symbol."""
    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": symbol
    }

    today_str = datetime.now().strftime("%Y%m%d")
    start_str = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    
    params2 = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_INPUT_ISCD": symbol,
        "FID_INPUT_DATE_1": start_str,  # Start Date (YYYYMMDD)
        "FID_INPUT_DATE_2": today_str,  # End Date (YYYYMMDD)
        "FID_PERIOD_DIV_CODE": "D",     # D: Daily data
        "FID_ORG_ADJ_PRC": "0"          # 0: Unadjusted price (1 for adjusted)
    }
    data = safe_request("GET", config.EP_PRICE, config.TR_ID_PRICE, params=params)
    data2 = safe_request("GET", config.EP_PRICE2, config.TR_ID_PRICE2, params=params2)

    try:
        # 가격 및 당일/전일 거래량 파싱
        price = int(data["output"]["stck_prpr"])
        today_vol = int(data["output"]["acml_vol"])
        yest_vol = int(data2["output1"]["prdy_vol"])
        
        logger.info(f"Market Data for {symbol}: Price {price:,} KRW | Today Vol: {today_vol:,} | Yest Vol: {yest_vol:,}")
        
        return {
            "price": price, 
            "today_vol": today_vol, 
            "yest_vol": yest_vol
        }
    except (KeyError, TypeError) as e:
        logger.error(f"Failed to parse market data: {e}")
        return {"price": 0, "today_vol": 0, "yest_vol": 0}
