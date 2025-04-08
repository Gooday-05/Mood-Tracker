from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
import sqlite3
import hashlib

Window.size = (dp(360), dp(640))
Window.softinput_mode = "below_target"


class IconGrid(GridLayout):
    pass


class StartScreen(MDScreen):
    pass


class RegisterScreen(MDScreen):
    def register_user(self):
        name = self.ids.name.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()
        confirm_password = self.ids.confirm_password.text.strip()

        if not name or not email or not password:
            self.ids.error_label.text = "All fields are required!"
            return

        if password != confirm_password:
            self.ids.error_label.text = "Passwords do not match!"
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            self.ids.error_label.text = "Email already exists!"
            conn.close()
            return

        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        conn.close()

        self.manager.current = "login"


class LoginScreen(MDScreen):
    def login_user(self):
        email = self.ids.login_email.text.strip()
        password = self.ids.login_password.text.strip()

        if not email or not password:
            self.ids.error_label.text = "Fields cannot be empty!"
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email=? AND password=?", (email, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            home_screen = self.manager.get_screen("homepage")
            home_screen.user_id = user[0]
            home_screen.user_name = user[1]
            home_screen.update_welcome_message()
            self.manager.current = "homepage"
        else:
            self.ids.error_label.text = "Invalid email or password!"


class HomePageScreen(MDScreen):
    user_id = None
    user_name = ""

    mood_mapping = {
        "Sad": 0,
        "Stressed": 1,
        "Neutral": 2,
        "Good": 3,
        "Jolly": 4
    }

    reverse_mood_mapping = {v: k for k, v in mood_mapping.items()}

    def on_enter(self):
        self.update_welcome_message()
        if self.user_id:
            conn = sqlite3.connect("mood_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT mood FROM moods WHERE user_id=? ORDER BY id DESC LIMIT 1", (self.user_id,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.set_mood(result[0])

    def update_welcome_message(self):
        self.ids.greeting_label.text = f"Welcome, {self.user_name}!"

    def set_mood(self, mood):
        mood_slider = self.ids.mood_slider
        if mood in self.mood_mapping:
            mood_slider.value = self.mood_mapping[mood]
            self.update_mood_label(self.mood_mapping[mood])

    def update_mood_label(self, value):
        mood = self.reverse_mood_mapping.get(int(value), "Neutral")
        self.ids.affirmation_label.text = f"Current mood: {mood}"

    def store_manual_mood(self):
        mood_value = int(self.ids.mood_slider.value)
        mood = self.reverse_mood_mapping[mood_value]

        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO moods (user_id, score, mood) VALUES (?, ?, ?)",
                       (self.user_id, mood_value * 5, mood))
        conn.commit()
        conn.close()

        self.ids.affirmation_label.text = f"Saved mood: {mood}"


class CommunityScreen(MDScreen):
    pass


class QuestionnaireScreen(MDScreen):
    def submit_responses(self):
        try:
            responses = [
                int(self.ids.q1.value),
                int(self.ids.q2.value),
                int(self.ids.q3.value),
                int(self.ids.q4.value),
                int(self.ids.q5.value)
            ]
        except ValueError:
            return

        total_score = sum(responses)
        mood = self.analyze_mood(total_score)

        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()
        user_id = self.manager.get_screen("homepage").user_id

        cursor.execute("INSERT INTO moods (user_id, score, mood) VALUES (?, ?, ?)", (user_id, total_score, mood))
        conn.commit()
        conn.close()

        self.manager.get_screen("homepage").set_mood(mood)
        self.manager.current = "homepage"

    def analyze_mood(self, score):
        if score <= 7:
            return "Sad"
        elif score <= 13:
            return "Stressed"
        elif score <= 17:
            return "Neutral"
        elif score <= 21:
            return "Good"
        else:
            return "Jolly"


class AnalyticsScreen(MDScreen):
    def on_enter(self):
        self.update_mood_counts()

    def update_mood_counts(self):
        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()

        mood_list = ['Sad', 'Stressed', 'Neutral', 'Good', 'Jolly']
        label_ids = ['sad_count', 'stressed_count', 'neutral_count', 'good_count', 'jolly_count']

        for mood, label_id in zip(mood_list, label_ids):
            cursor.execute("SELECT COUNT(*) FROM moods WHERE mood = ?", (mood,))
            count = cursor.fetchone()[0]
            self.ids[label_id].text = f"{mood}: {count}"

        conn.close()


class MindfulApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        self.init_db()
        Builder.load_file("mindfultracker.kv")

        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen(name="start"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(HomePageScreen(name="homepage"))
        self.sm.add_widget(CommunityScreen(name="community"))
        self.sm.add_widget(QuestionnaireScreen(name="questionnaire"))
        self.sm.add_widget(AnalyticsScreen(name="analytics"))
        self.sm.current = "login"
        return self.sm

    def change_screen(self, screen_name):
        self.sm.current = screen_name

    def init_db(self):
        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                mood TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        conn.close()


if __name__ == "__main__":
    MindfulApp().run()
