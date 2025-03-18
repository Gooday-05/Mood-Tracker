from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import requests

Window.size = (dp(360), dp(640))  
Window.softinput_mode = "below_target"

class StartScreen(Screen):
    pass  

class HomePageScreen(Screen):
    def update_greeting(self, instance):
        self.ids.greeting_label.text = f"Hello, {instance.text}!"

    def log_mood(self, mood):
        user = self.ids.name_input.text.strip()
        if not user:
            self.ids.greeting_label.text = "Please enter your name first!"
            return

        data = {"user": user, "mood": mood}
        response = requests.post("http://localhost:3000/log_mood", json=data)

        if response.status_code == 200:
            print("Mood saved successfully!")
        else:
            print("Error saving mood.")

class MindfulApp(MDApp):  
    def build(self):
        Builder.load_file("mindfultracker.kv")
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))  
        sm.add_widget(HomePageScreen(name="homepage"))
        return sm

if __name__ == "__main__":
    MindfulApp().run()
