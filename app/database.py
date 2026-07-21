import json
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "sqlite.db"
SHIPMENTS_PATH = PROJECT_ROOT / "shipments.json"

with sqlite3.connect(DATABASE_PATH) as connection:
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS shipment (
            id INTEGER,
            content TEXT,
            weight REAL,
            destination INTEGER,
            status TEXT
        )
        """
    )

    columns = {
        column[1] for column in cursor.execute("PRAGMA table_info(shipment)")
    }
    if "destination" not in columns:
        cursor.execute("ALTER TABLE shipment ADD COLUMN destination INTEGER")

    with SHIPMENTS_PATH.open(encoding="utf-8") as shipments_file:
        shipments = json.load(shipments_file)

    cursor.executemany(
        """
        INSERT INTO shipment (id, content, weight, destination, status)
        SELECT :id, :content, :weight, :destination, :status
        WHERE NOT EXISTS (
            SELECT 1 FROM shipment WHERE id = :id
        )
        """,
        shipments,
    )
