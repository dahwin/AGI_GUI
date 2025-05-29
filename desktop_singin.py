#desktop_singin.py
import sys
import requests
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox, QSizePolicy,
                             QDateEdit, QCalendarWidget, QRadioButton, QButtonGroup, 
                             QComboBox, QCompleter, QCheckBox,QMainWindow)
from PySide6.QtCore import Qt, QPropertyAnimation,  QDate, QSettings, QTimer,QThread, Signal, QObject
from PySide6.QtGui import QLinearGradient, QColor, QPainter, QPen, QFont, QPixmap, QIcon
import re
import pycountry
from others import UserProfileWidget, GradientLabel, check_port
from main_process import MyMainWindow
from cryptography.fernet import Fernet
import os
import json
from datetime import datetime, timedelta
import asyncio
import threading
import socket
import psutil
from aiohttp import web
import urllib.parse
import webbrowser
import re
# Global variables
shutdown_event = threading.Event()
server_thread = None
online = True
port = 8080

weburl = "https://www.queendahyun.site"




API_BASE_URL = 'https://www.queendahyun.site/api' if online else 'http://127.0.0.1:8000/api'
# API_BASE_URL = f'{webapi}/api' if online else 'http://127.0.0.1:8000/api'
print(API_BASE_URL)
# Get a list of all country names
countries = [country.name for country in pycountry.countries]
countries.sort()
import os
import subprocess

async def handle(request):
    query_string = request.query_string
    query_components = urllib.parse.parse_qs(query_string)
    if 'data' in query_components:
        received_data = query_components['data'][0]
        print(f"Received data: {received_data}")
        request.app['token'] = received_data
        request.app['received_token'].set()
    return web.Response(text='OK')

def run_server(port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = web.Application()
    app['received_token'] = asyncio.Event()
    app['token'] = None
    app.add_routes([web.get('/', handle)])
    
    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, 'localhost', port)
    
    try:
        loop.run_until_complete(site.start())
        print(f"Server successfully started on port {port}")
        
        loop.run_until_complete(app['received_token'].wait())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Shutting down server...")
        loop.run_until_complete(site.stop())
        loop.run_until_complete(runner.cleanup())
        loop.close()
        print("Server has been shut down.")
    
    return app['token']

def start_server_thread(port):
    global server_thread
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.start()
    return server_thread

def stop_server():
    global server_thread
    if server_thread is not None and server_thread.is_alive():
        print("Initiating server shutdown...")
        shutdown_event.set()
        server_thread.join()  # Wait for the server thread to finish
        print("Server thread has been closed.")
    else:
        print("No server is running.")
class GoogleSignInThread(QThread):
    token_received = Signal(str)

    def run(self):
        token = run_server(port)
        if token:
            self.token_received.emit(token)
        else:
            print("Failed to receive token from Google Sign-in")
class UserDataFetcher(QObject):
    user_data_fetched = Signal(dict)
    fetch_error = Signal(str)

    def fetch_user_data(self, access_token):
        user_url = f"{API_BASE_URL}/user"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(user_url, headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                self.user_data_fetched.emit(user_data)
            else:
                self.fetch_error.emit(f"Failed to fetch user data. Status code: {response.status_code}")
        except requests.RequestException as e:
            self.fetch_error.emit(f"Network error: {str(e)}")

class FuturisticAuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.access_token = None
        self.settings = QSettings("YourCompany", "FuturisticAuthApp")
        self.encryption_key = self.get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self.token_file = "user_token.json"
        self.offline_mode = False
        self.google_signin_thread = None
        is_open, process_name, pid = check_port(port)
        self.user_data_fetcher = UserDataFetcher()
        self.user_data_fetcher.user_data_fetched.connect(self.on_user_data_fetched)
        self.user_data_fetcher.fetch_error.connect(self.on_fetch_error)

        if is_open:
            self.initPortInUseUI(process_name, pid)
        else:
            self.initUI()
            self.check_saved_login()
            self.setup_refresh_timer()

    def show_main_window(self):
        self.main = MyMainWindow()
        self.main.show()
        self.hide()  # Hide the login window instead of closing it
    def get_or_create_encryption_key(self):
        key = self.settings.value("encryption_key")
        if not key:
            key = Fernet.generate_key()
            self.settings.setValue("encryption_key", key)
        return key
    def initPortInUseUI(self,process_name,pid):
        self.setWindowTitle('Port In Use')
        self.resize(400, 200)

        layout = QVBoxLayout()
        message = QLabel(f"Port {port} is open.\nPort {port} is being used by process {process_name} (PID: {pid}) \n Please Stop That Process")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("color: white; font-size: 14px;")

        layout.addWidget(message)
        self.setLayout(layout)

    def initUI(self):
        self.setWindowTitle('Futuristic Auth App')
        self.resize(400, 600)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Center container
        center_container = QWidget()
        center_container.setFixedWidth(350)
        center_layout = QVBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image
        image_label = QLabel()
        pixmap = QPixmap("dahyun.png")  # Make sure this image exists in your directory
        scaled_pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Header
        self.header = GradientLabel('Welcome')
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(QFont('Arial', 24, QFont.Weight.Bold))

        # Stacked widget for login, signup
        self.stacked_widget = QStackedWidget()
        self.login_widget = self.create_login_widget()
        self.signup_widget = self.create_signup_widget()
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.signup_widget)

        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.hide()

        # Add widgets to center layout
        center_layout.addWidget(image_label)
        center_layout.addWidget(self.header)
        center_layout.addWidget(self.stacked_widget)
        center_layout.addWidget(self.logout_button)

        # Add center container to main layout
        main_layout.addWidget(center_container, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        # Start gradient animation
        self.start_gradient_animation()

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
                color: white;
                font-family: Arial;
            }
            QLineEdit, QDateEdit, QComboBox {
                padding: 10px;
                border: 2px solid #4287f5;
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                margin-bottom: 10px;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #000000, stop:1 #4287f5);
                color: white;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1c1c1c, stop:1 #5a9aff);
            }
            QRadioButton, QCheckBox {
                color: white;
            }
        """)


    def create_login_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.remember_me = QCheckBox("Remember Me")

        login_button = QPushButton("Log In")
        login_button.clicked.connect(self.login)

        switch_to_signup = QPushButton("Don't have an account? Sign Up")
        switch_to_signup.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Add Google Sign-in button
        google_signin_button = QPushButton("Sign in with Google")
        google_signin_button.setIcon(QIcon("google.png"))
        google_signin_button.clicked.connect(self.start_google_signin)

        layout.addWidget(self.login_email)
        layout.addWidget(self.login_password)
        layout.addWidget(self.remember_me)
        layout.addWidget(login_button)
        layout.addWidget(google_signin_button)
        layout.addWidget(switch_to_signup)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        widget.setLayout(layout)
        return widget

    def create_signup_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # First Name and Last Name
        name_layout = QHBoxLayout()
        self.signup_first_name = QLineEdit()
        self.signup_first_name.setPlaceholderText("First Name")
        self.signup_last_name = QLineEdit()
        self.signup_last_name.setPlaceholderText("Last Name")
        name_layout.addWidget(self.signup_first_name)
        name_layout.addWidget(self.signup_last_name)
        layout.addLayout(name_layout)

        # Date of Birth
        dob_layout = QHBoxLayout()
        dob_label = QLabel("Date of Birth:")
        dob_label.setStyleSheet("color: white;")
        self.signup_dob = QDateEdit()
        self.signup_dob.setDisplayFormat("yyyy-MM-dd")
        self.signup_dob.setCalendarPopup(True)
        self.signup_dob.setMaximumDate(QDate.currentDate())
        self.signup_dob.setDate(QDate.currentDate().addYears(-18))
        self.signup_dob.dateChanged.connect(self.update_dob_display)
        dob_layout.addWidget(dob_label)
        dob_layout.addWidget(self.signup_dob)
        layout.addLayout(dob_layout)

        # Gender
        gender_layout = QHBoxLayout()
        gender_label = QLabel("Gender:")
        gender_label.setStyleSheet("color: white;")
        self.gender_group = QButtonGroup()
        for gender in ["Male", "Female", "Other"]:
            radio = QRadioButton(gender)
            self.gender_group.addButton(radio)
            gender_layout.addWidget(radio)
        layout.addWidget(gender_label)
        layout.addLayout(gender_layout)

        # Country
        country_layout = QHBoxLayout()
        country_label = QLabel("Country:")
        country_label.setStyleSheet("color: white;")
        self.signup_country = QComboBox()
        self.signup_country.addItems(countries)
        self.signup_country.setEditable(True)
        self.signup_country.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        completer = QCompleter(countries)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.signup_country.setCompleter(completer)
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.signup_country)
        layout.addLayout(country_layout)

        self.signup_email = QLineEdit()
        self.signup_email.setPlaceholderText("Email")
        layout.addWidget(self.signup_email)

        self.signup_password = QLineEdit()
        self.signup_password.setPlaceholderText("Password")
        self.signup_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.signup_password)

        signup_button = QPushButton("Sign Up")
        signup_button.clicked.connect(self.signup)
        layout.addWidget(signup_button)

        switch_to_login = QPushButton("Already have an account? Log In")
        switch_to_login.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(switch_to_login)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setLayout(layout)
        return widget

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        for i in range(100):
            r = int(10 + (47-10) * i/100)
            g = int(14 + (6-14) * i/100)
            b = int(36 + (24-36) * i/100)
            gradient.setColorAt(i/100, QColor(r, g, b))

        painter.fillRect(self.rect(), gradient)

    def start_gradient_animation(self):
        self.animation = QPropertyAnimation(self.header, b'gradientPosition')
        self.animation.setDuration(3000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setLoopCount(-1)
        self.animation.start()

    def update_dob_display(self):
        selected_date = self.signup_dob.date()
        self.signup_dob.setStyleSheet(self.signup_dob.styleSheet() + f"QDateEdit {{ color: white; }}")
        print(f"Selected date: {selected_date.toString('yyyy-MM-dd')}")  # For debugging

    def login(self):
        login_url = f"{API_BASE_URL}/token"
        login_data = {
            "username": self.login_email.text(),
            "password": self.login_password.text()
        }
        try:
            response = requests.post(login_url, data=login_data)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                if self.remember_me.isChecked():
                    self.save_token_locally(self.access_token)
                self.fetch_user_data()
                QMessageBox.information(self, "Success", "Login successful!")
            elif response.status_code == 401:
                QMessageBox.warning(self, "Error", "Incorrect username or password.")
            else:
                QMessageBox.warning(self, "Error", f"Login failed. Status code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Unable to connect to the server. Error: {str(e)}")
            self.try_offline_login()
    def save_token_locally(self, token):
        token_data = {
            "access_token": token,
            "expiry": (datetime.now() + timedelta(days=30)).isoformat()
        }
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def check_saved_login(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            expiry = datetime.fromisoformat(token_data['expiry'])
            if datetime.now() < expiry:
                self.access_token = token_data['access_token']
                self.fetch_user_data()
            else:
                os.remove(self.token_file)

    def try_offline_login(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            self.access_token = token_data['access_token']
            self.offline_mode = True
            self.load_cached_user_data()
        else:
            QMessageBox.warning(self, "Error", "No saved login found. Please connect to the internet and try again.")
    def start_google_signin(self):
        self.google_signin_thread = GoogleSignInThread()
        self.google_signin_thread.token_received.connect(self.on_google_token_received)
        self.google_signin_thread.start()
        webbrowser.open(f"{weburl}/singing_google")

    def on_google_token_received(self, token):
        self.access_token = token
        self.save_token_locally(self.access_token)
        self.fetch_user_data()

    def fetch_user_data(self):
        if self.offline_mode:
            self.load_cached_user_data()
            return

        self.user_data_thread = QThread()
        self.user_data_fetcher.moveToThread(self.user_data_thread)
        self.user_data_thread.started.connect(lambda: self.user_data_fetcher.fetch_user_data(self.access_token))
        self.user_data_thread.start()


    def on_user_data_fetched(self, user_data):
        self.current_user = user_data
        self.cache_user_data(self.current_user)
        self.show_main_window()
        self.user_data_thread.quit()
        self.user_data_thread.wait()


    def on_fetch_error(self, error_message):
        QMessageBox.warning(self, "Error", error_message)
        self.user_data_thread.quit()
        self.user_data_thread.wait()

    def cache_user_data(self, user_data):
        with open('user_data_cache.json', 'w') as f:
            json.dump(user_data, f)

    def load_cached_user_data(self):
        try:
            with open('user_data_cache.json', 'r') as f:
                self.current_user = json.load(f)
            self.user_profile_widget.update_profile(self.current_user)
            self.stacked_widget.setCurrentWidget(self.user_profile_widget)
            self.logout_button.show()
            if self.offline_mode:
                QMessageBox.information(self, "Offline Mode", "You are currently in offline mode. Some features may be limited.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No cached user data found. Please connect to the internet and log in again.")

    def logout(self):
        self.current_user = None
        self.access_token = None
        self.offline_mode = False
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        if os.path.exists('user_data_cache.json'):
            os.remove('user_data_cache.json')
        if hasattr(self, 'main_window'):
            self.main_window.close()
        self.show()  # Show the login window again
        self.stacked_widget.setCurrentWidget(self.login_widget)
        QMessageBox.information(self, "Success", "Logged out successfully!")

    def signup(self):
        if not self.validate_signup_inputs():
            return

        signup_url =f"{API_BASE_URL}/signup"
        signup_data = {
            "first_name": self.signup_first_name.text(),
            "last_name": self.signup_last_name.text(),
            "date_of_birth": self.signup_dob.date().toString("yyyy-MM-dd"),
            "gender": self.gender_group.checkedButton().text() if self.gender_group.checkedButton() else "",
            "country": self.signup_country.currentText(),
            "email": self.signup_email.text(),
            "password": self.signup_password.text()
        }
        try:
            response = requests.post(signup_url, json=signup_data)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Signup successful! You can now log in.")
                self.stacked_widget.setCurrentIndex(0)  # Switch to login page
            elif response.status_code == 400:
                error_detail = response.json().get("detail", "Unknown error")
                QMessageBox.warning(self, "Error", f"Signup failed. {error_detail}")
            else:
                QMessageBox.warning(self, "Error", f"Signup failed. Status code: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"Unable to connect to the server. Error: {str(e)}")

    def validate_signup_inputs(self):
        if not self.signup_first_name.text() or not self.signup_last_name.text():
            QMessageBox.warning(self, "Error", "Please enter both first and last name.")
            return False

        if self.signup_dob.date() >= QDate.currentDate():
            QMessageBox.warning(self, "Error", "Please enter a valid date of birth.")
            return False

        if not self.gender_group.checkedButton():
            QMessageBox.warning(self, "Error", "Please select a gender.")
            return False

        if not self.signup_country.currentText():
            QMessageBox.warning(self, "Error", "Please select a country.")
            return False

        email = self.signup_email.text()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Error", "Please enter a valid email address.")
            return False

        password = self.signup_password.text()
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters long.")
            return False
        if not re.search(r"[A-Z]", password):
            QMessageBox.warning(self, "Error", "Password must contain at least one uppercase letter.")
            return False
        if not re.search(r"[a-z]", password):
            QMessageBox.warning(self, "Error", "Password must contain at least one lowercase letter.")
            return False
        if not re.search(r"\d", password):
            QMessageBox.warning(self, "Error", "Password must contain at least one number.")
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            QMessageBox.warning(self, "Error", "Password must contain at least one special character.")
            return False

        return True

    def setup_refresh_timer(self):
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_token)
        self.refresh_timer.start(24 * 60 * 60 * 1000)  # Refresh every 24 hours

    def refresh_token(self):
        if not self.offline_mode and self.access_token:
            refresh_url = f"{API_BASE_URL}/refresh_token"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = requests.post(refresh_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data['access_token']
                    self.save_token_locally(self.access_token)
                else:
                    print("Failed to refresh token")
            except requests.RequestException:
                print("Network error while refreshing token")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseSoftwareOpenGL)
    window = FuturisticAuthWindow()
    window.show()
    sys.exit(app.exec())