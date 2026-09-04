from datetime import datetime


LOG_FILE = "logs/security_events.log"


def log_event(event_type, message):
    timestamp = datetime.now().isoformat()

    log_entry = f"{timestamp} | {event_type} | {message}\n"

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)


print("Personal Security Monitoring Dashboard")
print("Security monitoring system is starting...")

log_event("LOGIN_SUCCESS", "User logged in successfully")
log_event("LOGIN_FAILED", "Failed login attempt detected")

print("Security events recorded successfully.")