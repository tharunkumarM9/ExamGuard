import sqlite3
import os


DATABASE = "database/examguard.db"


# ----------------------------------------
# DATABASE CONNECTION
# ----------------------------------------
def get_db():

    connection = sqlite3.connect(DATABASE)

    # Allows dictionary-style access:
    # candidate["id"]
    # candidate["name"]
    # candidate["email"]
    # candidate["password"]
    # candidate["photo"]
    # candidate["created_at"]

    connection.row_factory = sqlite3.Row

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ----------------------------------------
# INITIALIZE DATABASE
# ----------------------------------------
def init_db():

    # Create database folder if it does not exist
    os.makedirs("database", exist_ok=True)

    connection = get_db()


    # ----------------------------------------
    # CANDIDATES TABLE
    # ----------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            photo TEXT,

            created_at TEXT
        )
    """)


    # ----------------------------------------
    # CHECK CREATED_AT COLUMN
    # ----------------------------------------
    columns = connection.execute(
        "PRAGMA table_info(candidates)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "created_at" not in column_names:

        connection.execute(
            "ALTER TABLE candidates ADD COLUMN created_at TEXT"
        )


    # ----------------------------------------
    # EXAM SESSION LIFECYCLE
    # ----------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS exam_sessions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            session_id TEXT UNIQUE NOT NULL,

            status TEXT NOT NULL DEFAULT 'in_progress',

            started_at TEXT NOT NULL,

            paused_at TEXT,

            resumed_at TEXT,

            submitted_at TEXT,

            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)
        )
    """)


    # ----------------------------------------
    # FACE MONITORING EVENTS
    # ----------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS face_events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            session_id TEXT NOT NULL,

            event_type TEXT NOT NULL,

            started_at TEXT NOT NULL,

            ended_at TEXT,

            duration_seconds REAL,

            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)
        )
    """)


    # ----------------------------------------
    # BROWSER ACTIVITY EVENTS
    # ----------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS browser_events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            session_id TEXT NOT NULL,

            event_type TEXT NOT NULL,

            event_time TEXT NOT NULL,

            details TEXT,

            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)
        )
    """)


    # ----------------------------------------
    # SUSPICIOUS EVENTS
    # ----------------------------------------
    connection.execute("""
        CREATE TABLE IF NOT EXISTS suspicious_events (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            session_id TEXT NOT NULL,

            event_type TEXT NOT NULL,

            reason TEXT NOT NULL,

            event_time TEXT NOT NULL,

            severity TEXT NOT NULL,

            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)
        )
    """)


    # ----------------------------------------
    # CHECK REGISTERED CANDIDATES
    # ----------------------------------------
    candidates = connection.execute(
        """
        SELECT id, name, email
        FROM candidates
        """
    ).fetchall()

    print("\n----------------------------------------")
    print("REGISTERED CANDIDATES")
    print("----------------------------------------")

    if candidates:

        for candidate in candidates:
            print(dict(candidate))

    else:

        print("No candidates registered yet.")

    print("----------------------------------------\n")


    # ----------------------------------------
    # SAVE DATABASE CHANGES
    # ----------------------------------------
    connection.commit()


    # ----------------------------------------
    # CLOSE DATABASE CONNECTION
    # ----------------------------------------
    connection.close()
    