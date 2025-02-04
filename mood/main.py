from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Screen for Mood Logging
class MoodLoggingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Log your mood here", font_size=30)
        layout.add_widget(label)
        self.add_widget(layout)

# Screen for Questionnaire
class QuestionnaireScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Answer the questionnaire", font_size=30)
        layout.add_widget(label)
        self.add_widget(layout)

# Main App with Screen Manager
class MentalHealthApp(App):
    def build(self):
        # Set up Screen Manager
        sm = ScreenManager()
        
        # Add screens to manager
        sm.add_widget(MoodLoggingScreen(name='mood_logging'))
        sm.add_widget(QuestionnaireScreen(name='questionnaire'))
        
        # Main layout container
        layout = BoxLayout(orientation='vertical')
        
        # Add a Label for the title
        title = Label(text="Mental Health Check-In", font_size=30, size_hint=(1, 0.2))
        layout.add_widget(title)
        
        # Button to log mood
        log_button = Button(text="Log My Mood", size_hint=(1, 0.2))
        
        # Use a proper function for switching screens
        log_button.bind(on_press=lambda x: self.switch_screen(sm, 'mood_logging'))
        layout.add_widget(log_button)
        
        # Button for questionnaire-based mood prediction
        questionnaire_button = Button(text="Take Questionnaire", size_hint=(1, 0.2))
        
        # Use a proper function for switching screens
        questionnaire_button.bind(on_press=lambda x: self.switch_screen(sm, 'questionnaire'))
        layout.add_widget(questionnaire_button)
        
        layout.add_widget(sm)
        return layout

    def switch_screen(self, sm, screen_name):
        """Function to switch the screen."""
        sm.current = screen_name

if __name__ == "__main__":
    MentalHealthApp().run()