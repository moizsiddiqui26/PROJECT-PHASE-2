import pandas as pd
import numpy as np


# =========================
# CALCULATE RETURNS
# =========================
def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add daily return column
    """
    df = df.copy()
    df["Return"] = df.groupby("Crypto")["Close"].pct_change()
    return df


# =========================
# CALCULATE VOLATILITY
# =========================
def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate rolling volatility (7-day std)
    """
    df = df.copy()
    df["Volatility"] = df.groupby("Crypto")["Return"].transform(
        lambda x: x.rolling(7).std()
    )
    return df


# =========================
# RISK CLASSIFICATION
# =========================
def classify_risk(volatility: float) -> str:
    """
    Assign risk level based on volatility
    """
    if pd.isna(volatility):
        return "Unknown"

    if volatility > 0.05:
        return "High"
    elif volatility > 0.02:
        return "Medium"
    else:
        return "Low"


# =========================
# FULL RISK ANALYSIS
# =========================
def run_risk_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full pipeline:
    - returns
    - volatility
    - risk level
    """

    if df.empty:
        return pd.DataFrame()

    df = calculate_returns(df)
    df = calculate_volatility(df)

    # Get latest values per crypto
    latest = df.sort_values("Date").groupby("Crypto").tail(1)

    result = latest[["Crypto", "Volatility"]].copy()
    result["Risk"] = result["Volatility"].apply(classify_risk)

    return result.reset_index(drop=True)


# =========================
# PORTFOLIO RISK SCORE
# =========================
def calculate_portfolio_risk(df: pd.DataFrame) -> dict:
    """
    Overall portfolio risk score
    """

    risk_df = run_risk_analysis(df)

    if risk_df.empty:
        return {"score": 0, "level": "Unknown"}

    # Convert risk to numeric
    mapping = {"Low": 1, "Medium": 2, "High": 3}
    risk_df["Score"] = risk_df["Risk"].map(mapping)

    avg_score = risk_df["Score"].mean()

    if avg_score >= 2.5:
        level = "High"
    elif avg_score >= 1.5:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": round(avg_score, 2),
        "level": level
    }


# =========================
# RISK ALERTS
# =========================
def get_high_risk_assets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return only high-risk assets
    """
    risk_df = run_risk_analysis(df)
    return risk_df[risk_df["Risk"] == "High"]
