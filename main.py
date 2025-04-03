from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import sqlite3
from kivy.clock import Clock

Window.size = (dp(360), dp(640))
Window.softinput_mode = "below_target"

class StartScreen(Screen):
    pass  

class HomePageScreen(Screen):
    mood_mapping = {
        "Sad": 0,
        "Stressed": 1,
        "Neutral": 2,
        "Good": 3,
        "Jolly": 4
    }

    def on_enter(self):
        """Fetch and update the mood slider when entering the home page."""
        try:
            conn = sqlite3.connect("mood_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT mood FROM moods ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
        except sqlite3.Error as e:
            print("Database error:", e)
            result = None
        finally:
            conn.close()

        if result:
            self.set_mood(result[0])

    def set_mood(self, mood):
        """Update the slider based on the stored mood."""
        mood_slider = self.ids.mood_slider
        if mood in self.mood_mapping:
            mood_slider.value = self.mood_mapping[mood]

    def store_manual_mood(self):
        """Save mood manually from slider."""
        mood_slider = self.ids.mood_slider
        reverse_mood_mapping = {v: k for k, v in self.mood_mapping.items()}
        mood = reverse_mood_mapping.get(int(mood_slider.value), "Neutral")

        try:
            conn = sqlite3.connect("mood_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO moods (score, mood) VALUES (?, ?)", (0, mood))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()

class CommunityScreen(Screen):
    pass  

class QuestionnaireScreen(Screen):
    def submit_responses(self):
        responses = [
            int(self.ids.q1.value),
            int(self.ids.q2.value),
            int(self.ids.q3.value),
            int(self.ids.q4.value),
            int(self.ids.q5.value)
        ]

        total_score = sum(responses)
        mood = self.analyze_mood(total_score)

        try:
            conn = sqlite3.connect("mood_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO moods (score, mood) VALUES (?, ?)", (total_score, mood))
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()

        # Show the mood result
        self.ids.result_label.text = f"Your mood is: {mood}"

        # Update mood in homepage and transition smoothly
        self.manager.get_screen("homepage").set_mood(mood)
        Clock.schedule_once(lambda dt: self.transition_to_home(), 2)  # Wait 2 seconds before switching

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

    def transition_to_home(self):
        """Smoothly transition to the home page."""
        self.manager.current = "homepage"

class MindfulApp(MDApp):
    def build(self):
        self.init_db()
        Builder.load_file("mindfultracker.kv")
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(HomePageScreen(name="homepage"))
        sm.add_widget(CommunityScreen(name="community"))
        sm.add_widget(QuestionnaireScreen(name="questionnaire"))
        return sm

    def change_screen(self, screen_name):
        self.root.current = screen_name

    def init_db(self):
        try:
            conn = sqlite3.connect("mood_data.db")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS moods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score INTEGER,
                    mood TEXT
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    MindfulApp().run()
