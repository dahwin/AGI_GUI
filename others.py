from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QStackedWidget, QMessageBox, QSizePolicy,
                             QDateEdit, QCalendarWidget, QRadioButton, QButtonGroup, 
                             QComboBox, QCompleter, QCheckBox)
from PySide6.QtCore import Qt, QPropertyAnimation,  QDate, QSettings, QTimer, QThread, Signal, QObject,Property
from PySide6.QtGui import QLinearGradient, QColor, QPainter, QPen, QFont, QPixmap, QIcon
import asyncio
from aiohttp import web
import urllib.parse
import requests
from PySide6.QtCore import QThread,QThreadPool, QRunnable
import socket
import psutil
import os
import sys

def get_user_data_path(filename):
    """
    Returns the full, platform-specific path to a file in the 
    application's user data directory. Creates the directory if it doesn't exist.
    
    - Windows: C:\\Users\\<user>\\AppData\\Roaming\\QueenDahyun
    - macOS:   /Users/<user>/Library/Application Support/QueenDahyun
    - Linux:   /home/<user>/.local/share/QueenDahyun
    """
    app_name = "QueenDahyun"
    
    # Determine the base path based on the operating system
    if sys.platform == "win32":
        # Windows
        base_path = os.environ.get('APPDATA', os.path.expanduser('~'))
    elif sys.platform == "darwin":
        # macOS
        base_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
    else:
        # Linux and other platforms (XDG standard)
        base_path = os.environ.get('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        
    # Create a specific folder for your app inside the base path
    app_folder = os.path.join(base_path, app_name)
    
    # Ensure this folder exists
    os.makedirs(app_folder, exist_ok=True)
    
    # Return the full path to the requested file
    return os.path.join(app_folder, filename)





def check_port(port):
    # Check if the port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"Port {port} is open.")
        
        # Find the process using the port
        for proc in psutil.process_iter(['pid', 'name']):
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    
                    return True, proc.info['name'], proc.info['pid']
    else:
        print(f"Port {port} is not open.")
        return False,False,False


class UserProfileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("User Profile")
        self.title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.name_label = QLabel()
        self.email_label = QLabel()
        self.dob_label = QLabel()
        self.gender_label = QLabel()
        self.country_label = QLabel()

        for label in [self.name_label, self.email_label, self.dob_label, self.gender_label, self.country_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)

        self.setLayout(layout)

    def update_profile(self, user_data):
        self.name_label.setText(f"Name: {user_data['first_name']} {user_data['last_name']}")
        self.email_label.setText(f"Email: {user_data['email']}")
        self.dob_label.setText(f"Date of Birth: {user_data['date_of_birth']}")
        self.gender_label.setText(f"Gender: {user_data['gender']}")
        self.country_label.setText(f"Country: {user_data['country']}")



class GradientLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.gradient_position = 0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    @Property(float)
    def gradientPosition(self):
        return self.gradient_position

    @gradientPosition.setter
    def gradientPosition(self, pos):
        self.gradient_position = pos
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor('#51d3da'))
        gradient.setColorAt(0.5, QColor('#c165dd'))
        gradient.setColorAt(1, QColor('#ff44b7'))
        gradient.setStart(self.gradient_position * self.width(), 0)
        gradient.setFinalStop(self.width(), 0)

        painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
        painter.drawText(self.rect(), self.alignment(), self.text())

