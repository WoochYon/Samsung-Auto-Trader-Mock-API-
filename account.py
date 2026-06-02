import config
from api_client import safe_request
from logger import get_logger

logger = get_logger("account")

def get_holdings_and_balance() -> dict:
    """Returns available cash and current holdings for the target symbol."""
    params = {
        "CANO": config.CANO,
        "ACNT_PRDT_CD": config.ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "N",
        "INQR_DVSN": "01",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    
    data = safe_request("GET", config.EP_BALANCE, config.TR_ID_BALANCE, params=params)
    
    result = {
        "cash": 0,
        "symbol_qty": 0
    }
    
    try:
        # Extract available cash
        output2 = data.get("output2", [{}])[0]
        result["cash"] = int(output2.get("prvs_rcdl_excc_amt", 0))
        
        # Extract stock holdings
        output1 = data.get("output1", [])
        for item in output1:
            if item.get("pdno") == config.SYMBOL:
                result["symbol_qty"] = int(item.get("hldg_qty", 0))
                break
                
        logger.info(f"Balance check -> Cash: {result['cash']:,} KRW | {config.SYMBOL} Holdings: {result['symbol_qty']} shares")
        return result
    except Exception as e:
        logger.error(f"Failed to parse account balance: {e}")
        return result
