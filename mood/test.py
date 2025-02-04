from database import log_mood, get_mood_history

# Log a test mood
log_mood(user_id=1, mood="Sad")

# Retrieve and print mood history
history = get_mood_history(user_id=1)
for mood, timestamp in history:
    print(f"Mood: {mood}, Logged at: {timestamp}")
