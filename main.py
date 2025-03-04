from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton  # ✅ Import this explicitly
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window
from kivymd.uix.button.button import MDRaisedButton



Window.size = (360, 640)

KV = """
ScreenManager:
    StartScreen:
    HomePageScreen:

<StartScreen>:
    name: "start"
    MDBoxLayout:
        orientation: "vertical"
        padding: "20dp"
        spacing: "20dp"

        MDLabel:
            text: "Welcome to Mindful Tracker"
            halign: "center"
            font_style: "H5"

        MDRaisedButton:
            text: "Take Questionnaire"
            size_hint_x: None
            size: "200dp", "50dp"
            pos_hint: {"center_x": 0.5}
            on_release: app.start_questionnaire()

        MDRaisedButton:
            text: "Login Directly"
            size_hint_x: None
            size: "200dp", "50dp"
            pos_hint: {"center_x": 0.5}
            on_release: app.login_directly()

<HomePageScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            text: "Welcome to the Home Page!"
            halign: "center"
"""
class MainApp(MDApp):
    def build(self):
        print("Building the app...")  # Debugging print
        self.theme_cls.primary_palette = "Blue"
        sm = Builder.load_string(KV)
        print("KV Loaded Successfully!")  # Debugging print
        return sm


class StartScreen(Screen):
    pass

class HomePageScreen(Screen):
    pass

class MainApp(MDApp):
    def build(self):
        print("Building the app...")  # Debugging print
        self.theme_cls.primary_palette = "Blue"
        sm = Builder.load_string(KV)  # ✅ Load the KV string properly
        print("KV Loaded Successfully!")  # Debugging print
        return sm
    
    def start_questionnaire(self):
        print("Questionnaire feature to be implemented!")

    def login_directly(self):
        print(f"Current screens: {[screen.name for screen in self.root.children]}")  # Debugging print
        self.root.current = "home"

if __name__ == "__main__":
    MainApp().run()
