import streamlit as st

# =========================
# HEADER / NAVBAR
# =========================
def render_header(user="Guest"):
    col1, col2 = st.columns([8,1])

    with col1:
        st.markdown(f"""
        <div style="
        position:sticky;
        top:0;
        z-index:999;
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:15px 25px;
        background:rgba(0,0,0,0.85);
        backdrop-filter:blur(12px);
        border-bottom:1px solid rgba(255,255,255,0.1);
        margin-bottom:10px;
        ">
            <div>
                <h3 style="margin:0;color:#4cc9f0;">🚀 Crypto SaaS</h3>
                <small style="color:gray;">AI • Risk • Analytics</small>
            </div>
            <div>👤 {user}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.session_state.get("auth"):
            if st.button("🚪", key="logout_component"):
                st.session_state.auth = False
                st.rerun()


# =========================
# LIVE TICKER
# =========================
def render_ticker(prices: dict):

    if not prices:
        return

    ticker_html = """
    <div style="
    display:flex;
    gap:25px;
    padding:10px;
    background:rgba(255,255,255,0.05);
    border-radius:10px;
    margin-bottom:15px;
    overflow-x:auto;
    ">
    """

    for coin, val in prices.items():
        try:
            ticker_html += f"<div>💰 {coin.upper()}: ${val['usd']}</div>"
        except:
            continue

    ticker_html += "</div>"

    st.markdown(ticker_html, unsafe_allow_html=True)


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
# METRIC ROW (MULTI CARDS)
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
# SUCCESS / ERROR ALERTS
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


# =========================
# NAVIGATION BAR (TOP MENU)
# =========================
def top_nav():
    return st.radio(
        "",
        ["📊 Dashboard", "💰 Investment", "⚠ Risk", "🔮 Forecast", "👤 Portfolio"],
        horizontal=True,
        label_visibility="collapsed"
    )
