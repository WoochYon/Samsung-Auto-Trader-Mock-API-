# Samsung Auto Trader (Mock API)

A simple, polling-based Python automated trading script for Samsung Electronics (005930) using the Korea Investment & Securities (KIS) Open API in a mock trading environment.

## Modifications
- In order to gain arbitrage profit from selling, the model buys specified number of stock at market price to hold at least 10 stocks.
- Under assumption that trading volume signifies liquidity of asset, this model attempts to buy(sell) stock when trading volume increases(decreases).
- The model buys stock 1,000KRW less than current market price, only when trading volume(converted to 7:30 hours) is higher than that of yesterday.
- The model sells stock 1,000KRW above current market price, only when trading volume(converted to 7:30 hours) is lower than that of yesterday.
## Features
- **Strict Rate Limiting:** Designed to poll conservatively (every 15s) and enforce delays between HTTP requests to avoid KIS API bans.
- **Token Caching:** Automatically caches OAuth tokens locally to ensure same-day reuse.
- **Verification by Holdings:** Verifies order execution by actively comparing account balance and stock holdings before and after orders.
- **Safe Bounds:** Strictly trades between 09:10 AM and 03:30 PM.

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
