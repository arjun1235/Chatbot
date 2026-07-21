import sqlite3
from pathlib import Path


DATABASE = Path("database/tickets.db")


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE)

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                issue TEXT,

                priority TEXT,

                status TEXT,

                confidence REAL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def create_ticket(self, issue, confidence):

        self.cursor.execute("""

            INSERT INTO tickets
            (issue, priority, status, confidence)

            VALUES (?, ?, ?, ?)

        """, (
            issue,
            "Medium",
            "Open",
            confidence
        ))

        self.connection.commit()

        return self.cursor.lastrowid

    def get_all_tickets(self):

        self.cursor.execute("""

            SELECT *

            FROM tickets

            ORDER BY id DESC

        """)

        return self.cursor.fetchall()
        
    def get_statistics(self):

        self.cursor.execute("SELECT COUNT(*) FROM tickets")
        total = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT COUNT(*) FROM tickets WHERE status='Open'"
        )
        open_tickets = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT AVG(confidence) FROM tickets"
        )
        avg_conf = self.cursor.fetchone()[0]

        return {
            "total": total,
            "open": open_tickets,
            "avg_confidence": round(avg_conf or 0, 2)
        }


    def get_issue_counts(self):

        self.cursor.execute("""

            SELECT issue, COUNT(*)

            FROM tickets

            GROUP BY issue

            ORDER BY COUNT(*) DESC

        """)

        return self.cursor.fetchall()