from logger import log_event


print("Personal Security Monitoring Dashboard")
print("Security monitoring system is starting...")

log_event(
    "LOGIN_SUCCESS",
    "LOW",
    "authentication",
    "User logged in successfully"
)

log_event(
    "LOGIN_FAILED",
    "HIGH",
    "authentication",
    "Failed login attempt detected"
)

log_event(
    "PASSWORD_CHANGED",
    "MEDIUM",
    "account",
    "User password was changed"
)

log_event(
    "SUSPICIOUS_ACTIVITY",
    "CRITICAL",
    "security",
    "Multiple failed login attempts detected"
)

log_event(
    "SYSTEM_EVENT",
    "LOW",
    "system",
    "Security monitoring system started"
)

print("Security events recorded successfully.")