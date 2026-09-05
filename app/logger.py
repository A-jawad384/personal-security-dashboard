from datetime import datetime


LOG_FILE = "logs/security_events.log"


def log_event(event_type, severity, source, message):
    timestamp = datetime.now().isoformat()

    log_entry = (
        f"{timestamp} | {event_type} | {severity} | "
        f"{source} | {message}\n"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)