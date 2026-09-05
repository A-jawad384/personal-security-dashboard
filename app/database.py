import sqlite3

DATABASE_FILE = "security_events.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            source TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_events():
    connection = get_connection()

    events = connection.execute(
        """
        SELECT id, timestamp, event_type, severity, source, message
        FROM security_events
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return events


def get_event_count():
    connection = get_connection()

    count = connection.execute(
        "SELECT COUNT(*) FROM security_events"
    ).fetchone()[0]

    connection.close()

    return count
def get_events_by_severity(severity):
    connection = get_connection()
def get_severity_count(severity):
    connection = get_connection()

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM security_events
        WHERE severity = ?
        """,
        (severity,)
    ).fetchone()[0]

    connection.close()

    return count
    events = connection.execute(
        """
        SELECT id, timestamp, event_type, severity, source, message
        FROM security_events
        WHERE severity = ?
        ORDER BY id DESC
        """,
        (severity,)
    ).fetchall()

    connection.close()

    return events

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")