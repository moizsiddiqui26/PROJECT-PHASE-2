
# =========================
# SAFE MODULE LOADER
# =========================
import os
import importlib.util
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# =========================
# LOAD MODULES
# =========================
crypto_api = load_module("crypto_api", os.path.join(BASE_DIR, "services", "crypto_api.py"))
auth_service = load_module("auth_service", os.path.join(BASE_DIR, "auth", "auth_service.py"))
ui = load_module("components", os.path.join(BASE_DIR, "ui", "components.py"))

get_raw_prices = crypto_api.get_top_10_prices

login_user = auth_service.login_user
register_user = auth_service.register_user

render_header = ui.render_header
render_ticker = ui.render_ticker


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="🚀 Crypto SaaS", layout="wide")


# =========================
# GLOBAL STYLE
# =========================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: white;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================
if "auth" not in st.session_state:
    st.session_state.auth = False

if "mode" not in st.session_state:
    st.session_state.mode = "login"


# =========================
# SAFE PRICE FETCH (FIXES 429 ISSUE)
# =========================
@st.cache_data(ttl=60)
def get_prices_safe():
    data = get_raw_prices()

    # ✅ reject bad API responses
    if not isinstance(data, dict):
        return {}

    if "status" in data:
        return {}

    # ensure valid crypto structure
    valid = {
        k: v for k, v in data.items()
        if isinstance(v, dict) and "usd" in v
    }

    return valid


# =========================
# LOGIN UI (CLEAN)
# =========================
def login_ui():

    st.markdown("""
    <div style="text-align:center; padding:40px 0;">
        <h1 style="color:#00f5ff;">🚀 Crypto SaaS</h1>
        <p style="color:gray;">Smart Crypto Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,4,2])

    with col2:

        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.05);
            padding:30px;
            border-radius:15px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        ">
        """, unsafe_allow_html=True)

        # LOGIN
        if st.session_state.mode == "login":

            st.markdown("### 🔐 Login")

            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("🚀 Login", use_container_width=True):
                res = login_user(email, password)

                if res["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.rerun()
                else:
                    st.error(res["msg"])

            colA, colB = st.columns(2)

            if colA.button("📝 Register"):
                st.session_state.mode = "register"

        # REGISTER
        elif st.session_state.mode == "register":

            st.markdown("### 📝 Register")

            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("✅ Create Account", use_container_width=True):
                res = register_user(name, email, password)

                if res["success"]:
                    st.session_state.auth = True
                    st.session_state.email = email
                    st.success("Account created & logged in 🚀")
                    st.rerun()
                else:
                    st.error(res["msg"])

            if st.button("⬅ Back"):
                st.session_state.mode = "login"

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN APP
# =========================
def main_app():

    render_header(st.session_state.email)

    prices = get_prices_safe()

    # ✅ show only if valid
    if prices:
        render_ticker(prices)
    else:
        st.warning("⚠ Market data unavailable (API limit). Try again in a minute.")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    dashboard = load_module("dashboard", os.path.join(BASE_DIR, "ui", "dashboard.py"))
    dashboard.main()


# =========================
# ROUTING
# =========================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
