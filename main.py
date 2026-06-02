from trader import run_trading_loop
from logger import get_logger
import config

logger = get_logger("main")

if __name__ == "__main__":
    if not all([config.APP_KEY, config.APP_SECRET, config.ACCOUNT_NO]):
        logger.error("Missing credentials! Ensure GH_APPKEY, GH_APPSECRET, and GH_ACCOUNT are set.")
        exit(1)
        
    try:
        run_trading_loop()
    except KeyboardInterrupt:
        logger.info("Trader stopped manually.")
    except Exception as e:
        logger.error(f"Fatal error encountered: {e}")
