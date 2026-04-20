import requests
import pandas as pd
import time

# =========================
# TOP 10 CRYPTO LIST
# =========================
TOP_10_COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "SOL": "solana",
    "ADA": "cardano",
    "DOGE": "dogecoin",
    "TRX": "tron",
    "MATIC": "polygon"
}

BASE_URL = "https://api.coingecko.com/api/v3"


# =========================
# 🔥 GET LIVE PRICES (FIXED)
# =========================
def get_top_10_prices():
    """
    Returns live prices for top 10 coins
    """
    try:
        ids = ",".join(TOP_10_COINS.values())

        response = requests.get(
            f"{BASE_URL}/simple/price",
            params={"ids": ids, "vs_currencies": "usd"},
            timeout=10
        )

        if response.status_code != 200:
            print("API Error:", response.status_code)
            return {}

        return response.json()

    except Exception as e:
        print("Error fetching prices:", e)
        return {}


# =========================
# HISTORICAL DATA
# =========================
def get_historical_data(days=120):
    """
    Fetch historical data for all coins
    """
    all_data = []

    for symbol, coin_id in TOP_10_COINS.items():
        try:
            response = requests.get(
                f"{BASE_URL}/coins/{coin_id}/market_chart",
                params={"vs_currency": "usd", "days": days},
                timeout=10
            )

            if response.status_code != 200:
                continue

            data = response.json()

            if "prices" not in data:
                continue

            df = pd.DataFrame(data["prices"], columns=["timestamp", "Close"])
            df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["Crypto"] = symbol

            all_data.append(df[["Date", "Crypto", "Close"]])

            time.sleep(1)  # avoid rate limit

        except Exception as e:
            print("Error:", e)
            continue

    if not all_data:
        return pd.DataFrame(columns=["Date", "Crypto", "Close"])

    return pd.concat(all_data)


# =========================
# SINGLE COIN DATA
# =========================
def get_coin_data(symbol, days=120):
    """
    Fetch data for one coin
    """
    coin_id = TOP_10_COINS.get(symbol)

    if not coin_id:
        return pd.DataFrame()

    try:
        response = requests.get(
            f"{BASE_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": days},
            timeout=10
        )

        data = response.json()

        df = pd.DataFrame(data["prices"], columns=["timestamp", "Close"])
        df["Date"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df[["Date", "Close"]]

    except Exception as e:
        print("Error:", e)
        return pd.DataFrame()
