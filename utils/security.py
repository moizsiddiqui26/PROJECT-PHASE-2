import hashlib
import secrets
import time

# =========================
# PASSWORD HASHING
# =========================
def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(input_password: str, stored_password: str) -> bool:
    """
    Verify input password with stored hash
    """
    return hash_password(input_password) == stored_password


# =========================
# TOKEN GENERATION
# =========================
def generate_token(length: int = 32) -> str:
    """
    Generate secure random token
    """
    return secrets.token_hex(length)


# =========================
# OTP GENERATION
# =========================
def generate_otp() -> str:
    """
    Generate 6-digit OTP
    """
    return str(secrets.randbelow(900000) + 100000)


# =========================
# SESSION TOKEN (BASIC)
# =========================
def create_session(email: str) -> dict:
    """
    Create session token with expiry
    """
    return {
        "user": email,
        "token": generate_token(16),
        "expires": time.time() + 3600  # 1 hour
    }


def is_session_valid(session: dict) -> bool:
    """
    Check if session is still valid
    """
    if not session:
        return False

    return time.time() < session.get("expires", 0)


# =========================
# INPUT VALIDATION
# =========================
def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    return "@" in email and "." in email


def validate_password(password: str) -> bool:
    """
    Password rules:
    - Min 6 chars
    """
    return len(password) >= 6


# =========================
# SANITIZATION
# =========================
def sanitize_input(text: str) -> str:
    """
    Basic input sanitization
    """
    return text.strip()
