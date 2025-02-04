import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("mood_tracker.db")
cursor = conn.cursor()

# Create mood logs table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mood_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        mood TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()


# Function to log mood
def log_mood(user_id, mood):
    """Save a mood entry to the database."""
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO mood_logs (user_id, mood) VALUES (?, ?)", (user_id, mood))
    
    conn.commit()
    conn.close()


# Function to retrieve mood history
def get_mood_history(user_id):
    """Fetch mood history for a user."""
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT mood, timestamp FROM mood_logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    data = cursor.fetchall()
    
    conn.close()
    return data


def log_mood(user_id, mood):
    """Save a mood entry to the database."""
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO mood_logs (user_id, mood) VALUES (?, ?)", (user_id, mood))
    
    conn.commit()
    conn.close()


def get_mood_history(user_id):
    """Fetch mood history for a user."""
    conn = sqlite3.connect("mood_tracker.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT mood, timestamp FROM mood_logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    data = cursor.fetchall()
    
    conn.close()
    return data
