import streamlit as st


# =========================
# PUBLIC HEADER (BEFORE LOGIN)
# =========================
def render_public_header():

    st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        width: 100%;
        background: linear-gradient(90deg, #0f0c29, #302b63);
        padding: 15px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 999;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }

    .logo {
        font-size: 22px;
        font-weight: bold;
        color: #00f5ff;
    }

    .spacer {
        height: 80px;
    }
    </style>

    <div class="navbar">
        <div class="logo">🚀 Crypto SaaS</div>
    </div>

    <div class="spacer"></div>
    """, unsafe_allow_html=True)

    # Login/Register buttons
    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("Login"):
            st.session_state.mode = "login"

        if st.button("Register"):
            st.session_state.mode = "register"


# =========================
# APP HEADER (AFTER LOGIN)
# =========================
def render_app_header(user):

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "📊 Dashboard"

    st.markdown("""
    <style>
    .navbar {
        position: fixed;
        top: 0;
        width: 100%;
        background: linear-gradient(90deg, #0f0c29, #302b63);
        padding: 10px 40px;
        z-index: 999;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }

    .spacer {
        height: 90px;
    }

    .user {
        font-size: 14px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,6,2])

    # LOGO
    with col1:
        st.markdown("### 🚀 Crypto SaaS")

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
        st.markdown(f"<div class='user'>👤 {user}</div>", unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)


# =========================
# LIVE MARKET TICKER (CARDS)
# =========================
def render_ticker(prices):

    st.markdown("### 💰 Live Market Prices")

    if not prices:
        st.warning("No price data available")
        return

    cols = st.columns(len(prices))

    for i, (coin, data) in enumerate(prices.items()):

        try:
            price = list(data.values())[0]
        except:
            price = "N/A"

        cols[i].markdown(f"""
        <div style="
            background: #1e1e2f;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
        ">
            <div style="font-size: 13px; color: #aaa;">
                {coin.upper()}
            </div>
            <div style="font-size: 18px; font-weight: bold; color: #00ffcc;">
                ${price}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# CARD COMPONENT
# =========================
def card(title, value, color="white"):
    st.markdown(f"""
    <div style="
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    text-align:center;
    ">
        <h4 style="margin:0;color:gray;">{title}</h4>
        <h2 style="margin:0;color:{color};">{value}</h2>
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
    st.markdown(f"### {title}")


# =========================
# ALERTS
# =========================
def show_success(msg):
    st.success(msg)


def show_error(msg):
    st.error(msg)


# =========================
# LOADING SPINNER
# =========================
def loading(text="Loading..."):
    return st.spinner(text)
