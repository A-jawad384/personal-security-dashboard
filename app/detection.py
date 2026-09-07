from database import get_event_type_count, create_alert, has_active_alert


def detect_multiple_failed_logins(threshold=3):
    failed_login_count = get_event_type_count("LOGIN_FAILED")

    if failed_login_count >= threshold:
        alert = {
            "detected": True,
            "alert_type": "MULTIPLE_FAILED_LOGINS",
            "severity": "HIGH",
            "message": "Multiple failed login attempts detected."
        }

        if not has_active_alert(alert["alert_type"]):
            create_alert(
                alert["alert_type"],
                alert["severity"],
                alert["message"]
            )

        return alert

    return {
        "detected": False,
        "alert_type": "MULTIPLE_FAILED_LOGINS",
        "severity": "LOW",
        "message": "No multiple failed login pattern detected."
    }