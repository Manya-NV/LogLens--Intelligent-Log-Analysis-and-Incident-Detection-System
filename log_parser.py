
import sqlite3
from pathlib import Path
from log_parser import parse_log_file

DATABASE_PATH = Path(__file__).parent / "loglens.db"


def create_table():
    """Create the logs table if it does not exist."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)


def insert_logs(entries):
    """Save parsed log entries into the database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executemany("""
            INSERT INTO logs (timestamp, severity, message)
            VALUES (?, ?, ?)
        """, [
            (
                entry["timestamp"],
                entry["severity"],
                entry["message"]
            )
            for entry in entries
        ])


def fetch_logs():
    """Retrieve all logs from the database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute("""
            SELECT id, timestamp, severity, message
            FROM logs
            ORDER BY timestamp
        """)
        return cursor.fetchall()


if __name__ == "__main__":
    create_table()

    log_file = Path(__file__).parent / "sample.log"
    entries, invalid_count = parse_log_file(log_file)

    insert_logs(entries)

    saved_logs = fetch_logs()

    print("=== LogLens Database ===")
    print(f"Valid entries in file: {len(entries)}")
    print(f"Invalid lines skipped: {invalid_count}")
    print(f"Total records in database: {len(saved_logs)}")

    print("\nSaved logs:")
    for log in saved_logs:
        print(log)
