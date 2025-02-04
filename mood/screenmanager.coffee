ScreenManager:
    HomeScreen:
        name: 'home'
    MoodLoggingScreen:
        name: 'mood_logging'
    ActivityScreen:
        name: 'activity'

<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome to Mental Health Check-In'
        Button:
            text: 'Log Mood'
            on_press: root.manager.current = 'mood_logging'
        Button:
            text: 'View Activity'
            on_press: root.manager.current = 'activity'

<MoodLoggingScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Select your mood'
        Button:
            text: 'Happy'
            on_press: root.save_mood('Happy')
        Button:
            text: 'Sad'
            on_press: root.save_mood('Sad')
        Button:
            text: 'Neutral'
            on_press: root.save_mood('Neutral')
        Button:
            text: 'Back to Home'
            on_press: root.manager.current = 'home'

<ActivityScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Your Activity'
        Button:
            text: 'Back to Home'
            on_press: root.manager.current = 'home'
