import time
from datetime import datetime
from zoneinfo import ZoneInfo
import config
from market_data import get_market_data
from account import get_holdings_and_balance
from orders import place_order
from logger import get_logger

logger = get_logger("trader")
KST = ZoneInfo("Asia/Seoul")
def is_trading_window() -> bool:
    """Checks if current time is between 09:10 and 15:30 in KST."""
    now = datetime.now(KST)
    start_time = now.replace(hour=9, minute=10, second=0, microsecond=0)
    end_time = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return start_time <= now <= end_time

def run_trading_loop():
    logger.info("Initializing Trading Bot...")
    
    while True:
        now = datetime.now(KST)
        
        # 1. Stop if trading day is over
        if now.hour >= 15 and now.minute > 30:
            logger.info("Trading window closed (after 15:30 KST). Shutting down.")
            break
            
        # 2. Wait if before trading window
        if not is_trading_window():
            logger.info("Outside trading window. Waiting...")
            time.sleep(60)
            continue
            
        logger.info(f"--- Starting new trading cycle at {now.strftime('%H:%M:%S')} ---")
        
        # 3. Check current market data
        market_data = get_market_data(config.SYMBOL)
        price = market_data["price"]
        if price == 0:
            time.sleep(config.POLL_INTERVAL_SEC)
            continue
            
        today_vol = market_data["today_vol"]
        yest_vol = market_data["yest_vol"]
        
        # 거래량 환산 계산 (09:00 ~ 15:30 = 총 390분)
        elapsed_minutes = (now.hour - 9) * 60 + now.minute
        if elapsed_minutes <= 0:
            elapsed_minutes = 1  # 0으로 나누는 오류 방지

        # 4. Check initial balance/holdings
        initial_status = get_holdings_and_balance()
        current_qty = initial_status["symbol_qty"]
        current_cash = initial_status["cash"]    
        # --- [신규] 최소 10주 유지 보장 및 긴급 매수 로직 ---
        if current_qty < 10:
                    deficit_qty = 10 - current_qty
                    required_cash = price * deficit_qty
                    
                    logger.warning(f"Holdings ({current_qty} shares) below minimum (10 shares). Deficit: {deficit_qty} shares.")
                    logger.info(f"Placing emergency buy order for {deficit_qty} shares at CURRENT PRICE {price:,} KRW.")
                    
                    if current_cash >= required_cash:
                        place_order(config.SYMBOL, price, deficit_qty, is_buy=True)
                    else:
                        logger.error(f"Insufficient cash ({current_cash:,} KRW) to maintain minimum 10 shares. Required: {required_cash:,} KRW.")
                    
                    # 긴급 매수 주문 처리 시간을 위해 대기 후 이번 사이클 종료 (다음 사이클에서 재체크)
                    logger.info("Waiting 3 seconds before verifying emergency execution...")
                    time.sleep(3)
                    get_holdings_and_balance()
                    
                    logger.info(f"Cycle complete. Sleeping for {config.POLL_INTERVAL_SEC} seconds.")
                    time.sleep(config.POLL_INTERVAL_SEC)
                    continue
            
        projected_vol = today_vol * (390 / elapsed_minutes)
        logger.info(f"Volume Check -> Projected: {projected_vol:,.0f} | Yesterday: {yest_vol:,}")
            
    
        # 5. Calculate target prices
        buy_price = price - config.ORDER_PRICE_SPREAD
        sell_price = price + config.ORDER_PRICE_SPREAD
        
        # 조건: 
        # 매수 = 전일거래량 < 당일환산거래량 (Projected Vol > Yesterday Vol)
        # 매도 = 전일거래량 > 당일환산거래량 (Projected Vol < Yesterday Vol)
        buy_condition = projected_vol > yest_vol
        sell_condition = projected_vol < yest_vol
        
        # 6. Execute Orders
        # Place Buy Order
        if buy_condition:
            if initial_status["cash"] >= buy_price * config.ORDER_QTY:
                place_order(config.SYMBOL, buy_price, config.ORDER_QTY, is_buy=True)
            else:
                logger.warning("Insufficient cash for buy order.")
        else:
            logger.info("Buy condition not met (Projected Vol <= Yesterday Vol).")
            
        # Place Sell Order
        if sell_condition:
            if initial_status["symbol_qty"] >= config.ORDER_QTY:
                place_order(config.SYMBOL, sell_price, config.ORDER_QTY, is_buy=False)
            else:
                logger.warning("Insufficient holdings for sell order.")
        else:
            logger.info("Sell condition not met (Projected Vol >= Yesterday Vol).")
            
        # 7. Verify Execution
        logger.info("Waiting 3 seconds before verifying execution...")
        time.sleep(3)
        final_status = get_holdings_and_balance()
        
        if initial_status != final_status:
            logger.info("Execution suspected! Holdings or balance changed.")
        else:
            logger.info("No immediate execution detected (orders likely sitting in book).")
            
        # 8. Sleep conservatively to avoid rate limit
        logger.info(f"Cycle complete. Sleeping for {config.POLL_INTERVAL_SEC} seconds to respect rate limits.")
        time.sleep(config.POLL_INTERVAL_SEC)
