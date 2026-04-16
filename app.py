import streamlit as st
import time
import requests
import random

# Services / Modules
from db.database import get_connection
from db.models import create_user, fetch_user
from utils.security import hash_password, verify_password
from services.crypto_api import get_top_10_prices
from email_alert import send_registration_mail, send_otp_mail

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="🚀 Crypto SaaS Platform", layout="wide")

# Hide Streamlit UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# GLOBAL CSS
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}

/* Navbar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:15px 30px;
    background:rgba(0,0,0,0.85);
    backdrop-filter:blur(12px);
}

/* Ticker */
.ticker {
    display:flex;
    gap:25px;
    padding:10px;
    background:rgba(255,255,255,0.05);
    border-radius:10px;
    margin-bottom:15px;
    overflow-x:auto;
}

/* Card */
.card {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
}

/* Button hover */
button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# =========================
# AUTO REFRESH
# =========================
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = time.time()
    st.rerun()

# =========================
# SESSION
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"

# =========================
# HEADER + TICKER
# =========================
def header():
    user = st.session_state.get("email", "Guest")

    col1, col2 = st.columns([8,1])

    with col1:
        st.markdown(f"""
        <div class="navbar">
            <div>
                <h3 style="margin:0;color:#4cc9f0;">🚀 Crypto SaaS</h3>
                <small style="color:gray;">Real-Time • AI • Analytics</small>
            </div>
            <div>👤 {user}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.session_state.auth:
            if st.button("🚪", key="logout"):
                st.session_state.auth = False
                st.rerun()

    # 🔥 Live Ticker
    prices = get_top_10_prices()

    if prices:
        ticker_html = "<div class='ticker'>"
        for coin, val in prices.items():
            ticker_html += f"<div>💰 {coin.upper()}: ${val['usd']}</div>"
        ticker_html += "</div>"

        st.markdown(ticker_html, unsafe_allow_html=True)

# =========================
# AUTH UI
# =========================
def login_ui():

    header()

    # ================= LOGIN =================
    if st.session_state.mode == "login":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Login"):
                user = fetch_user(email)

                if user and verify_password(password, user[3]):
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with col2:
            if st.button("Register"):
                st.session_state.mode = "register"

        with col3:
            if st.button("OTP Login"):
                st.session_state.mode = "otp"

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= REGISTER =================
    elif st.session_state.mode == "register":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        name = st.text_input("👤 Name")
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Create Account"):
            success = create_user(name, email, hash_password(password))

            if success:
                send_registration_mail(email)
                st.success("Account created")
                st.session_state.mode = "login"
            else:
                st.error("User already exists")

        if st.button("Back"):
            st.session_state.mode = "login"

        st.markdown("</div>", unsafe_allow_html=True)

    # ================= OTP =================
    elif st.session_state.mode == "otp":

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        email = st.text_input("📧 Email")

        if st.button("Send OTP"):
            otp = str(random.randint(100000, 999999))
            st.session_state.otp = otp
            st.session_state.temp_email = email
            send_otp_mail(email, otp)
            st.success("OTP sent")

        otp_input = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if otp_input == st.session_state.otp:
                st.session_state.auth = True
                st.session_state.email = st.session_state.temp_email
                st.success("Login success")
                st.rerun()
            else:
                st.error("Invalid OTP")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================
# MAIN FLOW
# =========================
if not st.session_state.auth:
    login_ui()
else:
    header()
    from ui.dashboard import main
    main()
