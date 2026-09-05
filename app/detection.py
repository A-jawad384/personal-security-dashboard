from database import get_event_type_count


def detect_multiple_failed_logins(threshold=3):
    failed_login_count = get_event_type_count("LOGIN_FAILED")

    if failed_login_count >= threshold:
        return {
            "detected": True,
            "alert_type": "MULTIPLE_FAILED_LOGINS",
            "severity": "HIGH",
            "message": "Multiple failed login attempts detected."
        }

    return {
        "detected": False,
        "alert_type": "MULTIPLE_FAILED_LOGINS",
        "severity": "LOW",
        "message": "No multiple failed login pattern detected."
    }