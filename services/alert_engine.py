from db.models import get_all_active_alerts, deactivate_alert
from services.email_service import send_alert_email

def check_alerts(live_prices: dict):
    """
    Call this every price refresh cycle.
    live_prices = {"BTC": 65000.0, "ETH": 3200.0, ...}
    """
    alerts = get_all_active_alerts()   # fetch all users' active alerts

    for alert_id, email, coin, condition, target_price in alerts:
        current = live_prices.get(coin)
        if current is None:
            continue

        triggered = (
            (condition == "above" and current >= target_price) or
            (condition == "below" and current <= target_price)
        )

        if triggered:
            send_alert_email(email, coin, condition, target_price, current)
            deactivate_alert(alert_id)   # one-shot alert
