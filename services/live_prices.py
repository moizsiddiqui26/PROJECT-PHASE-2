```python
import requests

SYMBOL_MAP = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "BNB": "BNBUSDT",
    "XRP": "XRPUSDT",
    "SOL": "SOLUSDT",
    "ADA": "ADAUSDT",
    "DOGE": "DOGEUSDT",
    "TRX": "TRXUSDT",
    "MATIC": "MATICUSDT"
}

def get_live_prices():
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        res = requests.get(url, timeout=5)
        data = res.json()

        prices = {}

        for item in data:
            symbol = item["symbol"]
            price = float(item["price"])

            for k, v in SYMBOL_MAP.items():
                if v == symbol:
                    prices[k] = price

        return prices

    except:
        return {}
```
