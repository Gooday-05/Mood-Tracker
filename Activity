from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen

# Set window size for testing
Window.size = (360, 640)

KV = """
MDScreenManager:

    HomeScreen:
    JournalScreen:
    MeditateScreen:
    GoalsScreen:
    AnalysisScreen:
    ActivityScreen:

<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: 0.94, 0.91, 0.85, 1  # Background Color

        MDTopAppBar:
            title: "Mindful Tracker"
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1
            size_hint_y: None
            height: "56dp"

        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "10dp"
                adaptive_height: True

                GridLayout:
                    cols: 2
                    spacing: "10dp"
                    padding: "10dp"
                    size_hint_y: None
                    height: self.minimum_height

                    # Journal Card
                    MDCard:
                        size_hint: None, None
                        size: "150dp", "180dp"
                        shadow_softness: 2
                        radius: [20, 20, 20, 20]
                        BoxLayout:
                            orientation: "vertical"
                            Image:
                                source: "journal.jpg"
                                allow_stretch: True
                                keep_ratio: False
                            MDRaisedButton:
                                text: "Journal"
                                size_hint_y: None
                                height: "40dp"
                                on_release: app.root.current = "journal"

                    # Meditate Card
                    MDCard:
                        size_hint: None, None
                        size: "150dp", "180dp"
                        shadow_softness: 2
                        radius: [20, 20, 20, 20]
                        BoxLayout:
                            orientation: "vertical"
                            Image:
                                source: "meditate.webp"
                                allow_stretch: True
                                keep_ratio: False
                            MDRaisedButton:
                                text: "Meditate"
                                size_hint_y: None
                                height: "40dp"
                                on_release: app.root.current = "meditate"

                    # My Goals Card
                    MDCard:
                        size_hint: None, None
                        size: "150dp", "180dp"
                        shadow_softness: 2
                        radius: [20, 20, 20, 20]
                        BoxLayout:
                            orientation: "vertical"
                            Image:
                                source: "my_goals.jpg"
                                allow_stretch: True
                                keep_ratio: False
                            MDRaisedButton:
                                text: "My Goals"
                                size_hint_y: None
                                height: "40dp"
                                on_release: app.root.current = "goals"

                    # Analysis Card
                    MDCard:
                        size_hint: None, None
                        size: "150dp", "180dp"
                        shadow_softness: 2
                        radius: [20, 20, 20, 20]
                        BoxLayout:
                            orientation: "vertical"
                            Image:
                                source: "analysis.jpg"
                                allow_stretch: True
                                keep_ratio: False
                            MDRaisedButton:
                                text: "Analysis"
                                size_hint_y: None
                                height: "40dp"
                                on_release: app.root.current = "analysis"

    MDBottomNavigation:
        size_hint_y: None
        height: "50dp"

        MDBottomNavigationItem:
            name: "home"
            text: "Home"
            icon: "home"

        MDBottomNavigationItem:
            name: "community"
            text: "Community"
            icon: "forum"

        MDBottomNavigationItem:
            name: "activity"
            text: "Activity"
            icon: "chart-bar"
            on_release: app.root.current = "activity"

        MDBottomNavigationItem:
            name: "profile"
            text: "Profile"
            icon: "account"

<JournalScreen>:
    name: "journal"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Journal"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "home")]]
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "This is the Journal Page"
            halign: "center"

<MeditateScreen>:
    name: "meditate"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Meditate"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "home")]]
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "This is the Meditation Page"
            halign: "center"

<GoalsScreen>:
    name: "goals"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "My Goals"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "home")]]
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "This is the My Goals Page"
            halign: "center"

<AnalysisScreen>:
    name: "analysis"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Analysis"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "home")]]
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "This is the Analysis Page"
            halign: "center"

<ActivityScreen>:
    name: "activity"

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Activity"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, "current", "home")]]
            md_bg_color: 0.4, 0.2, 0.6, 1
            specific_text_color: 1, 1, 1, 1

        MDLabel:
            text: "This is the Activity Page"
            halign: "center"
"""

# Screen Classes
class HomeScreen(MDScreen):
    pass

class JournalScreen(MDScreen):
    pass

class MeditateScreen(MDScreen):
    pass

class GoalsScreen(MDScreen):
    pass

class AnalysisScreen(MDScreen):
    pass

class ActivityScreen(MDScreen):
    pass

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    MainApp().run()
