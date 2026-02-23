import os
import csv
import json
import sqlite3
from datetime import datetime, timezone


class Timeline:
    def __init__(self):
        # Each event is stored as a simple dictionary
        self.events = []

    # Add an event
    def add_event(self, dt, source, artifact, event_type, details, extra=None):
        """
        dt: a datetime object (preferred) OR a string timestamp
        source: where it came from (filesystem, exif, gpx, text, app_db, etc.)
        artifact: file path or artifact name
        event_type: what kind of timestamp/event this is
        details: short readable explanation
        extra: optional dictionary of extra fields
        """

        # Convert string timestamps to datetime if possible
        if isinstance(dt, str):
            dt = self.try_parse_datetime(dt)

        # If we still couldn't parse it, skip it
        if dt is None:
            return

        # Assume UTC if unknown
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # Convert to UTC
        dt_utc = dt.astimezone(timezone.utc)

        event = {
            "ts_utc": dt_utc.isoformat().replace("+00:00", "Z"),
            "source": source,
            "artifact": artifact,
            "event_type": event_type,
            "details": details,
            "extra": extra if extra else {}
        }

        self.events.append(event)

    # Parse timestamps
    def try_parse_datetime(self, text):
        """
        Tries to parse common timestamp formats.
        Returns datetime or None.
        """
        if not text:
            return None

        formats = [
            "%Y:%m:%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(text.strip(), fmt)
                return dt.replace(tzinfo=timezone.utc)
            except ValueError:
                pass

        return None

    # Add filesystem timestamps
    def add_filesystem_times(self, file_path):
        """
        Adds mtime/ctime/atime for a file into the timeline.
        """
        try:
            st = os.stat(file_path)

            self.add_event(
                datetime.fromtimestamp(st.st_mtime, tz=timezone.utc),
                "filesystem",
                file_path,
                "mtime",
                "File modified time"
            )

            self.add_event(
                datetime.fromtimestamp(st.st_ctime, tz=timezone.utc),
                "filesystem",
                file_path,
                "ctime",
                "File metadata change time (or creation time on some OS)"
            )

            self.add_event(
                datetime.fromtimestamp(st.st_atime, tz=timezone.utc),
                "filesystem",
                file_path,
                "atime",
                "File last access time"
            )

        except Exception as e:
            print("Filesystem timestamp error:", e)

    # Sorting
    def sort_events(self):
        self.events.sort(key=lambda e: e["ts_utc"])

    # Export formats
    def export_csv(self, out_path):
        self.sort_events()
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["ts_utc", "source", "artifact", "event_type", "details", "extra"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for e in self.events:
                row = e.copy()
                # store extra as JSON string in CSV so it fits in one column
                row["extra"] = json.dumps(row["extra"], ensure_ascii=False)
                writer.writerow(row)

    def export_json(self, out_path):
        self.sort_events()
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2, ensure_ascii=False)

    def export_sqlite(self, out_path):
        self.sort_events()

        conn = sqlite3.connect(out_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS timeline (
                ts_utc TEXT,
                source TEXT,
                artifact TEXT,
                event_type TEXT,
                details TEXT,
                extra TEXT
            )
        """)

        # clear old rows
        cur.execute("DELETE FROM timeline")

        for e in self.events:
            cur.execute(
                "INSERT INTO timeline VALUES (?, ?, ?, ?, ?, ?)",
                (
                    e["ts_utc"],
                    e["source"],
                    e["artifact"],
                    e["event_type"],
                    e["details"],
                    json.dumps(e["extra"], ensure_ascii=False)
                )
            )

        conn.commit()
        conn.close()
