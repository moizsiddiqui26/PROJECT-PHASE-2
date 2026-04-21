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
        prices = {}

        # ✅ Fetch only required coins (FAST)
        for name, symbol in SYMBOL_MAP.items():

            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            res = requests.get(url, timeout=2)

            if res.status_code == 200:
                data = res.json()
                prices[name] = float(data["price"])

        return prices

    except:
        return {}
