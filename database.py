import sqlite3
from datetime import datetime

class KernelDatabase:
    def __init__(self, db_path="kernel.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        # تفعيل تزامنية عالية ومنع تعارض العمليات في الخلفية
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. خارطة المحيط والاستخبارات اللاسلكية
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topology (
                    node_id TEXT PRIMARY KEY,
                    last_known_ip TEXT,
                    signal_index INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'UNKNOWN',
                    discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # 2. مستودع الطرود والرسائل الممررة مشفرة
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS secure_pipeline (
                    packet_id TEXT PRIMARY KEY,
                    destination TEXT,
                    payload TEXT,
                    routing_path TEXT,
                    status TEXT DEFAULT 'PENDING',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def register_node(self, node_id, ip):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO topology (node_id, last_known_ip, last_seen)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(node_id) DO UPDATE SET
                    last_known_ip = excluded.last_known_ip,
                    last_seen = CURRENT_TIMESTAMP
            """, (node_id, ip))
            conn.commit()

    def get_active_topology(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM topology WHERE last_seen >= datetime('now', '-1 minute')")
            return [dict(row) for row in cursor.fetchall()]

