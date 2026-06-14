import os
import sqlite3
import json
from typing import List, Dict, Any, Optional

# Path setup for DB location
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("KCHIRO_DB_PATH", os.path.join(DB_DIR, "assets.db"))

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initializes the database schema if it doesn't already exist."""
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    parameters TEXT,
                    glb_path TEXT,
                    render_path TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def create_asset(self, prompt: str, asset_type: str, parameters: Dict[str, Any]) -> int:
        """Inserts a new asset generation record and returns its ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO assets (prompt, asset_type, parameters, status) VALUES (?, ?, ?, 'generating')",
                (prompt, asset_type, json.dumps(parameters))
            )
            conn.commit()
            return cursor.lastrowid

    def update_asset_success(self, asset_id: int, glb_path: str, render_path: str):
        """Updates the status of an asset to completed and saves the file paths."""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE assets SET glb_path = ?, render_path = ?, status = 'completed', error_message = NULL WHERE id = ?",
                (glb_path, render_path, asset_id)
            )
            conn.commit()

    def update_asset_failed(self, asset_id: int, error_message: str):
        """Updates the status of an asset to failed and saves the error message."""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE assets SET status = 'failed', error_message = ? WHERE id = ?",
                (error_message, asset_id)
            )
            conn.commit()

    def get_assets(self) -> List[Dict[str, Any]]:
        """Retrieves all asset generation records ordered by created_at descending."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets ORDER BY id DESC")
            rows = cursor.fetchall()
            assets = []
            for row in rows:
                asset = dict(row)
                if asset["parameters"]:
                    asset["parameters"] = json.loads(asset["parameters"])
                assets.append(asset)
            return assets

    def get_asset(self, asset_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single asset generation record by its ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
            row = cursor.fetchone()
            if row:
                asset = dict(row)
                if asset["parameters"]:
                    asset["parameters"] = json.loads(asset["parameters"])
                return asset
            return None

    def delete_asset(self, asset_id: int) -> bool:
        """Deletes an asset record from the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
            conn.commit()
            return cursor.rowcount > 0

if __name__ == "__main__":
    db = DatabaseManager()
    print("Database initialized successfully at:", db.db_path)
