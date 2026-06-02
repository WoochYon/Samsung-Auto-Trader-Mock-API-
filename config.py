import os

# --- Credentials ---
# Load secrets from environment variables (e.g., Github Secrets or local env)
APP_KEY = os.environ.get("GH_APPKEY", "")
APP_SECRET = os.environ.get("GH_APPSECRET", "")
ACCOUNT_NO = os.environ.get("GH_ACCOUNT", "")

# Split account number into standard format for KIS API (first 8 digits, last 2 digits)
CANO = ACCOUNT_NO[:8] if ACCOUNT_NO else ""
ACNT_PRDT_CD = ACCOUNT_NO[8:] if len(ACCOUNT_NO) > 8 else "01"

# --- API Configuration ---
# Mock Trading Base URL
BASE_URL = "https://openapivts.koreainvestment.com:29443"

# --- Trading Parameters ---
SYMBOL = "005930"  # Samsung Electronics
ORDER_QTY = 1      # Quantity to buy/sell per cycle
ORDER_PRICE_SPREAD = 1000 #2000  # Spread for buy/sell orders (KRW)
POLL_INTERVAL_SEC = 15     # Conservative polling interval to avoid rate limits

# --- Endpoints & TR_IDs (Mock Trading) ---
# Note: Isolated here as requested so they can be easily verified or updated
EP_TOKEN = "/oauth2/tokenP"
EP_PRICE = "/uapi/domestic-stock/v1/quotations/inquire-price"
EP_BALANCE = "/uapi/domestic-stock/v1/trading/inquire-balance"
EP_ORDER = "/uapi/domestic-stock/v1/trading/order-cash"

TR_ID_PRICE = "FHKST01010100"
TR_ID_BALANCE = "VTTC8434R"   # Mock balance inquiry
TR_ID_BUY = "VTTC0802U"       # Mock cash buy
TR_ID_SELL = "VTTC0801U"      # Mock cash sell

EP_PRICE2 = "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
TR_ID_PRICE2 = "FHKST03010100"
