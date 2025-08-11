
from utils.db_utils import execute_query_without_no_value


def init_db():

    execute_query_without_no_value("""
            CREATE TABLE IF NOT EXISTS user_interests (
            user_id INTEGER,
            interest TEXT,
            count INTEGER DEFAULT 1,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT DEFAULT 'cold',
            PRIMARY KEY (user_id, interest)
            );
        """)
    
    execute_query_without_no_value("""
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        tags TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    execute_query_without_no_value("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            due_at TEXT,
            category TEXT,
            tags TEXT,
            remind INTEGER DEFAULT 0
        )
    """)
    execute_query_without_no_value("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            type TEXT NOT NULL DEFAULT 'expense',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    execute_query_without_no_value("""
        CREATE TABLE IF NOT EXISTS user_facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            fact TEXT NOT NULL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    execute_query_without_no_value("""
        CREATE TABLE IF NOT EXISTS user_item_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id INTEGER,
            interaction_type TEXT,
            interaction_value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    execute_query_without_no_value("""
       CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        occupation TEXT,
        preferences TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

init_db()