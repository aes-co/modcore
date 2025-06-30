import sqlite3
import logging
import os
import time
from typing import List, Dict

logger = logging.getLogger(__name__)

DB_FILE = "data/bot_database.db"

def init_db():
    """Menginisialisasi database dan tabel-tabel yang diperlukan"""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            
            # Buat tabel jika belum ada
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    username TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp INTEGER NOT NULL
                )
            """)
            
            # Tambahkan index untuk mempercepat query
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_group_id ON chat_data(group_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON chat_data(user_id)")
            
            conn.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)
        raise

def add_chat_data(group_id: int, user_id: int, username: str, message_type: str, content: str) -> bool:
    """Menambahkan data chat ke database"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            timestamp = int(time.time())
            cursor.execute(
                """INSERT INTO chat_data 
                (group_id, user_id, username, message_type, content, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (group_id, user_id, username, message_type, content, timestamp)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        logger.error(f"Failed to add chat data: {e}", exc_info=True)
        return False

def get_chat_data(group_id: int) -> List[Dict]:
    """Mengambil data chat untuk group tertentu"""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, message_type, content FROM chat_data WHERE group_id = ?",
                (group_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logger.error(f"Failed to get chat data: {e}", exc_info=True)
        return []
