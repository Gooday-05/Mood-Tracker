from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import sqlite3

Window.size = (dp(360), dp(640))
Window.softinput_mode = "below_target"

class StartScreen(Screen):
    pass  

class HomePageScreen(Screen):
    pass  

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

        # Store in SQLite
        conn = sqlite3.connect("mood_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO moods (score, mood) VALUES (?, ?)", (total_score, mood))
        conn.commit()
        conn.close()

        self.ids.result_label.text = f"Your mood is: {mood}"
    
    def analyze_mood(self, score):
        if score <= 7:
            return "Very Low Mood"
        elif score <= 13:
            return "Low Mood"
        elif score <= 17:
            return "Neutral"
        elif score <= 21:
            return "Good Mood"
        else:
            return "Very Happy Mood"

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
        conn.close()

if __name__ == "__main__":
    MindfulApp().run()
