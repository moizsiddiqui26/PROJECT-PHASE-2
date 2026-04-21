# =========================
# SAFE MODULE LOADER
# =========================
import os
import importlib.util

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
email_service = load_module("email_service", os.path.join(BASE_DIR, "services", "email_service.py"))
auth_service = load_module("auth_service", os.path.join(BASE_DIR, "auth", "auth_service.py"))
db_module = load_module("database", os.path.join(BASE_DIR, "db", "database.py"))
ui_components = load_module("components", os.path.join(BASE_DIR, "ui", "components.py"))

# Extract functions
get_top_10_prices = crypto_api.get_top_10_prices

send_welcome_email = email_service.send_welcome_email
send_otp_email = email_service.send_otp_email

login_user = auth_service.login_user
register_user = auth_service.register_user
generate_login_otp = auth_service.generate_login_otp
verify_otp = auth_service.verify_otp

init_db = db_module.init_db

render_public_header = ui_components.render_public_header
render_app_header = ui_components.render_app_header
render_ticker = ui_components.render_ticker


# =========================
# IMPORTS
# =========================
import streamlit as st


# =========================
# INIT
# =========================
init_db()

st.set_page_config(page_title="🚀 Crypto SaaS Platform", layout="wide")

# Hide Streamlit default UI
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# Global styling
st.markdown("""
<style>
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

if "otp" not in st.session_state:
    st.session_state.otp = None

if "temp_email" not in st.session_state:
    st.session_state.temp_email = None


# =========================
# HEADER + TICKER
# =========================
def render_top():

    prices = get_top_10_prices()

    if st.session_state.auth:
        render_app_header(st.session_state.get("email"))
    else:
        render_public_header()

    render_ticker(prices)


# =========================
# AUTH UI
# =========================
def login_ui():

    render_top()

    if st.session_state.mode == "login":

        st.subheader("🔐 Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Login", key="login_btn"):
                res = login_user(email, password)

                if res["success"]:
                    st.session_state.auth = True
                    st.session_state.email = res["user"]["email"]
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error(res["msg"])

        with col2:
            if st.button("Register", key="register_btn"):
                st.session_state.mode = "register"

        with col3:
            if st.button("OTP Login", key="otp_btn"):
                st.session_state.mode = "otp"

    elif st.session_state.mode == "register":

        st.subheader("📝 Register")

        name = st.text_input("Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Create Account", key="create_acc"):
            res = register_user(name, email, password)

            if res["success"]:
                send_welcome_email(email)
                st.success(res["msg"])
                st.session_state.mode = "login"
            else:
                st.error(res["msg"])

        if st.button("Back", key="back_from_register"):
            st.session_state.mode = "login"

    elif st.session_state.mode == "otp":

        st.subheader("🔐 OTP Login")

        email = st.text_input("Email", key="otp_email")

        if st.button("Send OTP", key="send_otp_btn"):
            otp = generate_login_otp()
            st.session_state.otp = otp
            st.session_state.temp_email = email

            send_otp_email(email, otp)
            st.success("OTP sent")

        otp_input = st.text_input("Enter OTP", key="otp_input")

        if st.button("Verify OTP", key="verify_otp_btn"):
            if verify_otp(otp_input, st.session_state.otp):
                st.session_state.auth = True
                st.session_state.email = st.session_state.temp_email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid OTP")

        if st.button("Back", key="back_from_otp"):
            st.session_state.mode = "login"


# =========================
# MAIN APP
# =========================
def main_app():

    render_top()

    # Load dashboard
    dashboard = load_module("dashboard", os.path.join(BASE_DIR, "ui", "dashboard.py"))
    dashboard.main()


# =========================
# ROUTING
# =========================
if not st.session_state.auth:
    login_ui()
else:
    main_app()
