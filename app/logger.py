from datetime import datetime
from database import get_connection, initialize_database

LOG_FILE = "logs/security_events.log"


def log_event(event_type, severity, source, message):
    timestamp = datetime.now().isoformat()

    log_entry = (
        f"{timestamp} | {event_type} | {severity} | "
        f"{source} | {message}\n"
    )

    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

    initialize_database()

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO security_events
        (timestamp, event_type, severity, source, message)
        VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, event_type, severity, source, message)
    )

    connection.commit()
    connection.close()