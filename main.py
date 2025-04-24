    
    
    
    
    
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
import hashlib
import psycopg2
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime, timedelta
from collections import Counter
from kivy.app import App
from collections import Counter, defaultdict
import numpy as np
from io import BytesIO
from kivy.core.image import Image as CoreImage
import pandas as pd
import os
from matplotlib.ticker import MaxNLocator
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import datetime
from plyer import notification
from kivy.storage.jsonstore import JsonStore
import requests
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField



store = JsonStore('user_status.json')


if not os.path.exists('graphs'):
    os.makedirs('graphs')


#plt.savefig('graphs/daily_mood_bar_chart.png', bbox_inches='tight')
#plt.savefig('graphs/pie.png', bbox_inches='tight')

DB_URL = "postgresql://postgres:OzmMvQTBFLDzOFfyjbscpsEIFzSJzucV@gondola.proxy.rlwy.net:18005/railway"  
Window.size = (360, 640)  
import psycopg2

def connect_db():
    return psycopg2.connect(
        host="gondola.proxy.rlwy.net",
        database="railway",
        user="postgres",
        password="OzmMvQTBFLDzOFfyjbscpsEIFzSJzucV",
        port=18005
    )

def get_mood_data(user_id, days):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT CAST(mood_value AS INTEGER), created_at FROM moods 
            WHERE user_id = %s AND created_at >= NOW() - INTERVAL %s
        """
        interval_str = f"{int(days)} days"
        cursor.execute(query, (user_id, interval_str))
        return cursor.fetchall()
    except Exception as e:
        print("Error fetching mood data:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_bar_graph(user_id, days=1):
    data = get_mood_data(user_id, days)
    print(f"Fetched mood data for {days} day(s): {data}")  # Debug log

    if not data:
        print(f"No data available for the last {days} day(s).")
        return

    # Count the frequency of each mood
    mood_counts = Counter([int(mood) for mood, _ in data])
    print(f"Mood counts: {mood_counts}")

    # Define labels and colors for the moods
    all_labels = ['Stressed', 'Sad', 'Neutral', 'Good', 'Jolly']
    all_colors = ['#FF8A80', '#FFD180', '#FFFF8D', '#A5D6A7', '#80D8FF']

    # Filter out moods with no occurrences and sort by count in descending order
    mood_data = [
        (all_labels[i], mood_counts.get(i, 0), all_colors[i])
        for i in range(5)
        if mood_counts.get(i, 0) > 0
    ]

    # Sort by frequency of mood (descending)
    mood_data.sort(key=lambda x: x[1], reverse=True)

    if not mood_data:
        print("All mood counts are zero. No chart will be generated.")
        return

    # Unpack the sorted data
    labels, values, colors = zip(*mood_data)

    # Set up the bar chart
    plt.clf()
    bars = plt.bar(labels, values, color=colors)
    plt.ylabel("Count")
    plt.title(f"Mood for the last {days} day(s)")
    plt.tight_layout()

    # Set y-axis to have integer values only
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

    # Save the bar chart image
    if days == 1:
        filename = "daily_mood_bar_chart.png"
    elif days == 7:
        filename = "weekly_mood_bar_chart.png"
    else:
        filename = "monthly_mood_bar_chart.png"

    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"Bar chart saved as {filename}")


def generate_mood_pie_chart(user_id, days=1):
    # Fetch the mood data
    data = get_mood_data(user_id, days)
    print(f"Fetched mood data for {days} day(s): {data}")  # Debug log

    if not data:
        print(f"No data available for the last {days} day(s).")
        return
    
    # Count the frequency of each mood
    mood_counts = Counter([int(mood) for mood, _ in data])
    print(f"Mood counts: {mood_counts}")

    # Define labels and colors for the moods
    all_labels = ['Stressed', 'Sad', 'Neutral', 'Good', 'Jolly']
    all_colors = ['#FF8A80', '#FFD180', '#FFFF8D', '#A5D6A7', '#80D8FF']

    # Filter out moods with no occurrences
    mood_data = [
        (all_labels[i], mood_counts.get(i, 0), all_colors[i])
        for i in range(5)
        if mood_counts.get(i, 0) > 0
    ]

    if not mood_data:
        print("All mood counts are zero. No chart will be generated.")
        return

    # Unpack the filtered data
    labels, values, colors = zip(*mood_data)

    # Set up the pie chart
    plt.clf()
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title(f"Mood for the last {days} day(s)")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the pie chart image
    if days == 1:
        filename = "daily_pie.png"
    elif days == 7:
        filename = "weekly_pie.png"
    else:
        filename = "monthly_pie.png"

    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # Close the plot after saving to free memory
    print(f"Pie chart saved as {filename}")


def generate_daily_graph(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT mood_value, COUNT(*) 
        FROM moods 
        WHERE user_id = %s AND created_at >= NOW()::DATE
        GROUP BY mood_value
    """, (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    # Map numeric mood values to mood names
    mood_map = {
        1: "Sad",
        2: "Stressed",
        3: "Neutral",
        4: "Good",
        5: "Jolly"
    }

    data = {mood_map.get(row[0], "Unknown"): row[1] for row in rows}

    generate_bar_graph(data, "daily.png", "Today's Mood")


def generate_weekly_graph(user_id):
    data = get_mood_data(user_id, 7)
    generate_bar_graph(data, "weekly.png", "Mood This Week")

def generate_monthly_graph(user_id):
    data = get_mood_data(user_id, 30)
    generate_bar_graph(data, "monthly.png", "Mood This Month")



Window.size = (dp(360), dp(640))
Window.softinput_mode = "below_target"

class IconGrid(ButtonBehavior, MDBoxLayout):
    def __init__(self, icon="", text="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "4dp"
        self.spacing = "2dp"
        self.icon = MDIconButton(icon=icon, user_font_size="20sp", theme_icon_color="Custom", icon_color=(0, 0, 0, 1), pos_hint={"center_x": 0.5})
        self.label = MDLabel(text=text, halign="center", font_style="Caption", theme_text_color="Primary")
        self.add_widget(self.icon)
        self.add_widget(self.label)

def get_db_connection():
    return psycopg2.connect(
        host="gondola.proxy.rlwy.net",
        port=18005,
        database="railway",
        user="postgres",
        password="OzmMvQTBFLDzOFfyjbscpsEIFzSJzucV",
        sslmode='require'
    )

class StartScreen(MDScreen): pass



class CommunityScreen(MDScreen):
    dialog = None
    api_base_url = "http://127.0.0.1:5000" # <--- REPLACE THIS

    def load_community_data(self):
        user_id = App.get_running_app().current_user_id
        if not user_id:
            return

        try:
            response_friends = requests.get(f"{self.api_base_url}/friends/{user_id}")
            if response_friends.ok:
                friends = response_friends.json().get("friends", [])
                friend_list = self.ids.friend_list
                friend_list.clear_widgets()
                for friend in friends:
                    friend_list.add_widget(OneLineListItem(text=friend["name"]))
            else:
                print(f"Error fetching friends: {response_friends.status_code} - {response_friends.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching friends: {e}")

        try:
            response_msgs = requests.get(f"{self.api_base_url}/messages/{user_id}")
            if response_msgs.ok:
                messages = response_msgs.json().get("messages", [])
                msg_list = self.ids.message_list
                msg_list.clear_widgets()
                for msg in messages:
                    name = msg["sender_name"]
                    text = msg["text"]
                    msg_list.add_widget(OneLineListItem(text=f"{name}: {text}"))
            else:
                print(f"Error fetching messages: {response_msgs.status_code} - {response_msgs.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching messages: {e}")

        
        
        
class SettingsScreen(MDScreen): pass





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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            self.ids.error_label.text = "Email already exists!"
            conn.close()
            return
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email=%s AND password=%s", (email, hashed_password))
        user = cursor.fetchone()
        conn.close()
        if user:
            from kivy.app import App  # Make sure to import if not already done
            App.get_running_app().user_id = user[0] # <-- This is the fix
            App.get_running_app().load_community_data()
            homepage = self.manager.get_screen("homepage")
            homepage.user_id = user[0]
            homepage.user_name = user[1]
            homepage.update_welcome_message()
            store = JsonStore('user_status.json')
            store.put('user', logged_in=True)
            self.manager.current = "homepage"
            self.manager.current = "start" 
        else:
            self.ids.error_label.text = "Invalid email or password!"


class HomePageScreen(MDScreen):
    user_id = None
    user_name = ""
    mood_mapping = {"Sad": 0, "Stressed": 1, "Neutral": 2, "Good": 3, "Jolly": 4}
    reverse_mood_mapping = {v: k for k, v in mood_mapping.items()}
    def on_enter(self):
        self.update_welcome_message()
    def update_welcome_message(self):
        self.ids.greeting_label.text = f"Welcome, {self.user_name}!"
    def update_mood_label(self, value):
        mood = self.reverse_mood_mapping.get(int(value), "Neutral")
        self.ids.affirmation_label.text = f"Current mood: {mood}"
    def store_manual_mood(self):
        mood_value = int(self.ids.mood_slider.value)
        mood = self.reverse_mood_mapping[mood_value]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO moods (user_id, mood_value, method, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)", (self.user_id, mood_value, 'slider'))
        conn.commit()
        conn.close()
        self.ids.affirmation_label.text = f"Saved mood: {mood}"

class QuestionnaireScreen(MDScreen):
    def submit_responses(self):
        try:
            responses = [int(self.ids.q1.value), int(self.ids.q2.value),
                         int(self.ids.q3.value), int(self.ids.q4.value), int(self.ids.q5.value)]
        except ValueError:
            return
        total_score = sum(responses)
        mood = self.analyze_mood(total_score)
        user_id = self.manager.get_screen("homepage").user_id
        mood_value = {"Sad": 0, "Stressed": 1, "Neutral": 2, "Good": 3, "Jolly": 4}[mood]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO moods (user_id, mood_value, method, created_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)", (user_id, mood_value, 'questionnaire'))
        conn.commit()
        conn.close()
        self.manager.get_screen("homepage").ids.affirmation_label.text = f"Mood (via questions): {mood}"
        self.manager.current = "homepage"
    def analyze_mood(self, score):
        if score <= 7: return "Sad"
        elif score <= 13: return "Stressed"
        elif score <= 17: return "Neutral"
        elif score <= 21: return "Good"
        else: return "Jolly"

def generate_mood_bar_chart(user_id, days=1):
    # Fetch the mood data (make sure this function exists and works correctly)
    data = get_mood_data(user_id, days)
    print(f"Fetched mood data for {days} day(s): {data}")  # Log data to debug

    # If no data is found for the given days, return early
    if not data:
        print(f"No data available for the last {days} day(s).")
        return
    
    # Count the frequency of each mood
    mood_counts = Counter([int(mood) for mood, _ in data])
    print(f"Mood counts: {mood_counts}")  # Log mood counts to verify

    # Labels for the moods
    labels = ['Stressed', 'Sad', 'Neutral', 'Good', 'Jolly']
    
    # Get the count of each mood from the mood_counts; default to 0 if mood not found
    values = [mood_counts.get(i, 0) for i in range(5)]
    print(f"Values for bar chart: {values}")  # Log the values for the bar chart

    # If no moods are recorded (all counts are zero), skip chart generation
    if sum(values) == 0:
        print("All mood counts are zero. No chart will be generated.")
        return

    # Set up the bar chart
    plt.clf()  # Clear the previous figure (useful if updating)
    plt.bar(labels, values, color=['#FF8A80', '#FFD180', '#FFFF8D', '#A5D6A7', '#80D8FF'])
    plt.ylabel("Count")
    plt.title(f"Mood for the last {days} day(s)")
    plt.tight_layout()

    # Save the image with a unique filename based on the days parameter
    if days == 1:
        filename = "daily_mood_bar_chart.png"
    elif days == 7:
        filename = "weekly_mood_bar_chart.png"
    else:
        filename = "monthly_mood_bar_chart.png"

    # Save the figure
    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # Close the plot after saving to free memory
    print(f"Bar chart saved as {filename}")  # Log the file save

def generate_mood_pie_chart(user_id, days=1):
    # Fetch the mood data (make sure this function exists and works correctly)
    data = get_mood_data(user_id, days)
    print(f"Fetched mood data for {days} day(s): {data}")  # Log data to debug

    if not data:
        print(f"No data available for the last {days} day(s).")
        return
    
    # Count the frequency of each mood
    mood_counts = Counter([int(mood) for mood, _ in data])
    print(f"Mood counts: {mood_counts}")  # Log mood counts to verify

    labels = ['Stressed', 'Sad', 'Neutral', 'Good', 'Jolly']
    values = [mood_counts.get(i, 0) for i in range(5)]
    print(f"Values for pie chart: {values}")  # Log the values for the pie chart

    if sum(values) == 0:
        print("All mood counts are zero. No chart will be generated.")
        return

    # Set up the pie chart
    plt.clf()  # Clear the previous figure (useful if updating)
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['#FF8A80', '#FFD180', '#FFFF8D', '#A5D6A7', '#80D8FF'])
    plt.title(f"Mood for the last {days} day(s)")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Save the pie chart image
    if days == 1:
        filename = "daily_pie.png"
    elif days == 7:
        filename = "weekly_pie.png"
    else:
        filename = "monthly_pie.png"

    # Save the pie chart as an image
    plt.savefig(filename, bbox_inches='tight')
    plt.close()  # Close the plot after saving to free memory
    print(f"Pie chart saved as {filename}")  # Log the file save

def generate_time_series_bar_chart(user_id, days=7):
    data = get_mood_data(user_id, days)
    if not data:
        return

    mood_labels = ['Stressed', 'Sad', 'Neutral', 'Good', 'Jolly']
    colors = ['#FF8A80', '#FFD180', '#FFFF8D', '#A5D6A7', '#80D8FF']

    # Prepare mood counts by date
    aggregated = defaultdict(lambda: [0] * 5)
    for mood, created_at in data:
        date = created_at.strftime("%Y-%m-%d")
        aggregated[date][int(mood)] += 1

    # Sort by date
    sorted_dates = sorted(aggregated.keys())
    bar_data = [aggregated[date] for date in sorted_dates]
    bar_data = np.array(bar_data)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')

    bottom = np.zeros(len(sorted_dates))
    for i in range(5):
        ax.bar(sorted_dates, bar_data[:, i], label=mood_labels[i], bottom=bottom, color=colors[i])
        bottom += bar_data[:, i]

    ax.set_title('Mood Trend Over Time')
    ax.set_ylabel('Mood Count')
    ax.set_xlabel('Date')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('bar_chart.png', bbox_inches='tight')
    plt.close()



def get_analytics(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    def fetch(days):
        cursor.execute("""
            SELECT DATE(created_at), mood_value::INTEGER, COUNT(*)
            FROM moods WHERE user_id=%s AND created_at >= %s
            GROUP BY DATE(created_at), mood_value::INTEGER
        """, (user_id, datetime.now() - timedelta(days=days)))
        result = cursor.fetchall()
        mood_labels = {0: 'Sad', 1: 'Stressed', 2: 'Neutral', 3: 'Good', 4: 'Jolly'}
        return [(r[0], mood_labels.get(r[1], 'Neutral'), r[2]) for r in result]
    counts = {m: 0 for m in ["Sad", "Stressed", "Neutral", "Good", "Jolly"]}
    cursor.execute("SELECT mood_value::INTEGER FROM moods WHERE user_id=%s", (user_id,))
    for row in cursor.fetchall():
        mood = {0: "Sad", 1: "Stressed", 2: "Neutral", 3: "Good", 4: "Jolly"}.get(row[0], "Neutral")
        counts[mood] += 1
    daily = fetch(1)
    weekly = fetch(7)
    monthly = fetch(30)
    conn.close()
    return {"counts": counts, "daily": daily, "weekly": weekly, "monthly": monthly}

class AnalyticsScreen(MDScreen):
    most_frequent_mood = StringProperty("Loading...")

    def on_enter(self):
        user_id = App.get_running_app().user_id
        # Fetch the data and generate the charts
        self.load_chart("daily")  # Display default daily chart

    def load_chart(self, chart_type):
       user_id = App.get_running_app().user_id
       print(f"[DEBUG] load_chart called with chart_type: {chart_type}")

       if chart_type == "daily":
           generate_mood_bar_chart(user_id, days=1)
           generate_mood_pie_chart(user_id, days=1)
           self.ids.mood_graph.source = "daily_mood_bar_chart.png"
           self.ids.pie_graph.source = "daily_pie.png"
       elif chart_type == "weekly":
           generate_mood_bar_chart(user_id, days=7)
           generate_mood_pie_chart(user_id, days=7)
           self.ids.mood_graph.source = "weekly_mood_bar_chart.png"
           self.ids.pie_graph.source = "weekly_pie.png"
       elif chart_type == "monthly":
           generate_mood_bar_chart(user_id, days=30)
           generate_mood_pie_chart(user_id, days=30)
           self.ids.mood_graph.source = "monthly_mood_bar_chart.png"
           self.ids.pie_graph.source = "monthly_pie.png"

       self.ids.mood_graph.reload()
       self.ids.pie_graph.reload()



class ProfileScreen(Screen):
    notification_event = None

    def toggle_notifications(self, switch, value):
        self.ids.notification_label.text = "Notifications: On" if value else "Notifications: Off"

        if value:
            self.notification_event = Clock.schedule_interval(self.send_daily_notification, 43200)
            self.send_daily_notification(0)
        else:
            if self.notification_event:
                self.notification_event.cancel()
                self.notification_event = None

    def send_daily_notification(self, dt):
        notification.notify(
            title='Mood Reminder',
            message='Don’t forget to log your mood today!',
            app_name='Hygge',
            timeout=10
        )

    def send_daily_notification(self, dt):
        notification.notify(
            title='Mood Reminder',
            message='Don’t forget to log your mood today!',
            timeout=10
        )

    
    def change_profile_picture(self):
        from kivy.uix.filechooser import FileChooserIconView
        from kivy.uix.popup import Popup

        filechooser = FileChooserIconView()
        filechooser.bind(on_selection=self.load_profile_picture)
        popup = Popup(title="Select Profile Picture", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def load_profile_picture(self, filechooser, selection):
        if selection:
            self.ids.profile_image.source = selection[0]

    def logout(self):
       from kivy.storage.jsonstore import JsonStore
       store = JsonStore('user_status.json')
       store.put('user', logged_in=False)
       self.manager.current = 'login'





class MindfulApp(MDApp):
    api_base_url = "http://127.0.0.1:5000"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self.user_name = None
        

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        self.store = JsonStore('user_status.json')

        Builder.load_file("mindfultracker.kv")

        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(StartScreen(name="start"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(HomePageScreen(name="homepage"))
        self.sm.add_widget(CommunityScreen(name="community"))
        self.sm.add_widget(QuestionnaireScreen(name="questionnaire"))
        self.sm.add_widget(AnalyticsScreen(name="analytics"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        if self.store.exists('user') and self.store.get('user')['logged_in']:
            self.sm.current = 'start'
        else:
            self.sm.current = 'login'

        return self.sm

    def on_start(self):
        # self.load_community_data() 
        pass

    def change_screen(self, screen_name):
        self.sm.current = screen_name

    def init_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        self.current_user_id = None
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS moods (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                mood_value TEXT,
                method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
        conn.close()

    def load_community_data(self):
        if not self.user_id:
            return

        try:
            response = requests.get(f"http://localhost:5000/friends/{self.user_id}")
            if response.status_code == 200:
                friends = response.json().get("friends", [])

                screen = self.root.get_screen("community")
                grid = screen.ids.get("icon_grid")  # IconGrid in KV file

                if grid:
                    grid.clear_widgets()
                    for friend in friends:
                        grid.add_widget(OneLineListItem(text=friend))
            else:
                print("Failed to load friends:", response.status_code)

        except Exception as e:
            print("Error fetching community data:", str(e))



if __name__ == "__main__":
    MindfulApp().run()
