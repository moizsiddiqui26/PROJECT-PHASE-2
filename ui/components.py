import streamlit as st

# =========================
# GLOBAL STYLES
# =========================
st.markdown("""
<style>

/* ===== NAVBAR ===== */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(90deg, #0f0c29, #302b63);
    padding: 12px 30px;
    border-radius: 0 0 12px 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* ===== LOGO ===== */
.logo {
    font-size: 22px;
    font-weight: bold;
    color: #00f5ff;
}

/* ===== USER ===== */
.user-box {
    text-align: right;
    font-size: 14px;
}

/* ===== CARD ===== */
.card {
    background: rgba(255,255,255,0.06);
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

/* ===== TICKER CARD ===== */
.ticker {
    background: #1e1e2f;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.3);
    transition: 0.3s;
}

.ticker:hover {
    transform: scale(1.05);
}

/* ===== SECTION ===== */
.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* ===== BUTTON ===== */
.stButton>button {
    border-radius: 8px;
    padding: 6px 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER / NAVBAR
# =========================
def render_header(user):

    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    col1, col2, col3 = st.columns([2,6,2])

    # LOGO
    with col1:
        st.markdown('<div class="logo">🚀 Crypto SaaS</div>', unsafe_allow_html=True)

    # NAVIGATION
    with col2:
        nav = st.radio(
            "",
            ["📊 Dashboard", "💰 Investment", "⚠ Risk", "🔮 Forecast", "👤 Portfolio"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.page = nav

    # USER + LOGOUT
    with col3:
        st.markdown(f'<div class="user-box">👤 {user}</div>', unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# =========================
# LIVE TICKER (IMPROVED)
# =========================
import requests
import pandas as pd

def render_ticker(prices):

    st.markdown("### 💰 Live Market Prices")

    symbol_map = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "tether": "USDT",
        "binancecoin": "BNB",
        "ripple": "XRP",
        "solana": "SOL",
        "cardano": "ADA",
        "dogecoin": "DOGE",
        "tron": "TRX",
        "polygon": "MATIC"
    }

    # 🪙 LOGOS (CoinGecko CDN)
    logo_map = {
        "bitcoin": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png",
        "ethereum": "https://assets.coingecko.com/coins/images/279/small/ethereum.png",
        "tether": "https://assets.coingecko.com/coins/images/325/small/Tether.png",
        "binancecoin": "https://assets.coingecko.com/coins/images/825/small/bnb-icon2_2x.png",
        "ripple": "https://assets.coingecko.com/coins/images/44/small/xrp-symbol-white-128.png",
        "solana": "https://assets.coingecko.com/coins/images/4128/small/solana.png",
        "cardano": "https://assets.coingecko.com/coins/images/975/small/cardano.png",
        "dogecoin": "https://assets.coingecko.com/coins/images/5/small/dogecoin.png",
        "tron": "https://assets.coingecko.com/coins/images/1094/small/tron-logo.png",
        "polygon": "https://assets.coingecko.com/coins/images/4713/small/matic-token-icon.png"
    }

    if not prices:
        return

    coins = list(prices.items())
    cols_per_row = 4

    for i in range(0, len(coins), cols_per_row):
        row = coins[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if j < len(row):
                coin, data = row[j]

                symbol = symbol_map.get(coin, coin.upper())
                price = list(data.values())[0]
                logo = logo_map.get(coin, "")

                # 📈 MINI CHART DATA (last 7 days)
                try:
                    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
                    res = requests.get(url, params={"vs_currency": "usd", "days": 7}, timeout=5)
                    chart_data = res.json()["prices"]

                    df = pd.DataFrame(chart_data, columns=["time", "price"])
                    spark = df["price"].tail(30)

                except:
                    spark = None

                with cols[j]:
                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.05);
                        padding: 15px;
                        border-radius: 14px;
                        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
                    ">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <img src="{logo}" width="25">
                            <span style="color:gray;">{symbol}</span>
                        </div>

                        <div style="
                            font-size:20px;
                            font-weight:bold;
                            color:#00ffcc;
                            margin-top:5px;
                        ">
                            ${price}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 📈 Sparkline chart
                    if spark is not None:
                        st.line_chart(spark, height=80, use_container_width=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)# =========================
# CARD COMPONENT
# =========================
def card(title, value, color="white"):
    st.markdown(f"""
    <div class="card">
        <div style="color:gray;">{title}</div>
        <div style="font-size:22px;font-weight:bold;color:{color};">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# METRIC ROW
# =========================
def metric_row(metrics: list):

    cols = st.columns(len(metrics))

    for i, m in enumerate(metrics):
        with cols[i]:
            card(m["title"], m["value"], m.get("color", "white"))


# =========================
# SECTION TITLE
# =========================
def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


# =========================
# ALERTS
# =========================
def show_success(msg):
    st.success(msg)


def show_error(msg):
    st.error(msg)


# =========================
# LOADING
# =========================
def loading(text="Loading..."):
    return st.spinner(text)

