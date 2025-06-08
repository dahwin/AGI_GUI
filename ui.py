from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QThread, Signal,
    QSize, QTime, QUrl, Qt, QPropertyAnimation, QEasingCurve,QProcess)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QTextCursor)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QListView, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget, QTextBrowser, QListWidget, QSplitter)
from PySide6.QtGui import QMovie
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient, QBrush, QPainterPath
from PySide6.QtCore import Qt, QPropertyAnimation, QRectF, Property
import json
import subprocess
import os
import time
import requests
from engine import EngineWindow
from ui_uilts import *
from others import  get_user_data_path
import sys
import httpx
import asyncio
import nest_asyncio
nest_asyncio.apply()


def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)
def resource_path(relative_path):

     return relative_path
a_p = '/usr/local/bin/asset/'
ubuntu = False

STYLE_SHEET = """
QWidget {
    background-color: transparent;
    color: white;
    font-family: Arial, sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #000000, stop:1 #B2B5D3);
}

#side_panel {
    background-color: rgba(0, 0, 0, 0.5);
    border-right: 1px solid #243689;
}

#main_content {
    background-color: transparent;
}

#send_btn, #engine_btn {
    padding: 10px 20px;
    border: 2px solid #243689; /* Add blue border */
    border-radius: 15px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #000000, stop:1 #B2B5D3);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

#send_btn:hover, #engine_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #000000, stop:1 #B2B5D3);
}

QLineEdit, QTextEdit, QDateEdit, QComboBox {
    padding: 10px;
    border: 2px solid #4287f5;
    border-radius: 15px;
    background-color: rgba(0, 0, 0, 0.7); /* Ensure background is dark */
    color: white;
    margin-bottom: 10px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: url(path_to_your_down_arrow_icon);
    width: 12px;
    height: 12px;
}

QPushButton {
    padding: 10px 20px;
    border: none;
    border-radius: 15px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #000000, stop:1 #B2B5D3);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                         stop:0 #B2B5D3, stop:1 #000000);
}

QRadioButton, QCheckBox {
    color: white;
}

QTextBrowser {
    background-color: transparent;
}

QTextBrowser::chunk {
    background-color: #000000;
}




QScrollBar:vertical {
    border: none;
    background: #000000;  /* Changed to black */
    width: 10px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: #219FD5;  /* Kept blue */
    min-height: 0px;
}

QScrollBar::add-line:vertical {
    border: none;
    background: #000000;  /* Changed to black */
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    border: none;
    background: #000000;  /* Changed to black */
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}



QTextBrowser {
    border: none;
    background-color: transparent;
}

QTextBrowser:focus {
    outline: none;
}

QTextBrowser::selection {
    background-color: rgba(33, 159, 213, 0.3);
}

#force_stop_btn {
    background-color: #FF0000;
    color: white;
    font-weight: bold;
    border-radius: 15px;
    padding: 10px 20px;
    margin-top: 5px;
}

#force_stop_btn:hover {
    background-color: #CC0000;
}
"""



def set_input_state(self, enabled: bool):
    """Enable or disable input controls while processing."""
    self.input_textEdit.setEnabled(enabled)
    self.send_btn.setEnabled(enabled)
    self.file_btn.setEnabled(enabled)
    self.model_combo.setEnabled(enabled)
    self.action_toggle.setEnabled(enabled)


class AnimatedSplitter(QSplitter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHandleWidth(2)
        self.splitterMoved.connect(self.handle_splitter_moved)
        self.animation = QPropertyAnimation(self, b"sizes")
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(300)  # 300ms animation duration

    def handle_splitter_moved(self, pos, index):
        if not self.animation.state() == QPropertyAnimation.Running:
            self.animation.setStartValue(self.sizes())
            self.animation.setEndValue(self.sizes())
            self.animation.start()

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(800, 600)
        
        # Set up the central widget and main layout
        self.centralwidget = QWidget(MainWindow)
        self.main_layout = QHBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a QSplitter for resizable panels
        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        # Create the side panel
        self.side_panel = QWidget()
        self.side_panel.setObjectName("side_panel")
        self.setup_side_panel()

        # Create the main content area
        self.main_content = QWidget()
        self.setup_main_content()

        # Add side panel and main content to the splitter
        self.splitter.addWidget(self.side_panel)
        self.splitter.addWidget(self.main_content)

        # Create "More" and "Less" icons
        self.more_icon = QPushButton()
        self.more_icon.setObjectName("more_icon")
        self.more_icon.setIcon(QIcon(resource_path("more.png")))
        self.more_icon.setIconSize(QSize(24, 24))
        self.more_icon.setFixedSize(QSize(40, 40))
        self.main_layout.addWidget(self.more_icon)

        self.less_icon = QPushButton()
        self.less_icon.setObjectName("less_icon")
        self.less_icon.setIcon(QIcon(resource_path("less.png")))
        self.less_icon.setIconSize(QSize(24, 24))
        self.less_icon.setFixedSize(QSize(40, 40))
        self.less_icon.hide()  # Initially hidden
        self.main_layout.addWidget(self.less_icon)

        # Connect icons to toggle side panel
        self.more_icon.clicked.connect(self.toggle_side_panel)
        self.less_icon.clicked.connect(self.toggle_side_panel)

        MainWindow.setCentralWidget(self.centralwidget)
        
        # Set up the menu bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setStyleSheet(STYLE_SHEET)

        # Initially hide the side panel
        self.side_panel.hide()




    def toggle_side_panel(self):
        if self.side_panel.isVisible():
            self.side_panel.hide()
            self.less_icon.hide()
            self.more_icon.show()
        else:
            self.side_panel.show()
            self.more_icon.hide()
            self.less_icon.show()
    def setup_side_panel(self):
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setSpacing(10)
        side_layout.setContentsMargins(10, 10, 10, 10)
        
        # 14 QPushButtons
        button_names = ["API","Popular Models",
            "(IL) Extension", "Engine Settings"
        ]
        
        for name in button_names:
            btn = QPushButton(name)
            btn.setObjectName(f"{name.lower().replace(' ', '_')}_btn")
            side_layout.addWidget(btn)
            if name == "Engine Settings":
                btn.clicked.connect(self.show_engine_window)
        
        # Your Account button with user logo
        self.account_btn = QPushButton("Account")
        self.account_btn.setObjectName("account_btn")
        user_icon = QIcon(resource_path("user.png"))  # Make sure to have a user icon SVG in your asset folder
        self.account_btn.setIcon(user_icon)
        self.account_btn.setIconSize(QSize(24, 24))
        self.account_btn.clicked.connect(self.show_account_info)
        side_layout.addWidget(self.account_btn)

    def show_account_info(self):
        # Create a new window to display account information
        self.account_window = QWidget()
        self.account_window.setWindowTitle("Account Information")
        self.account_window.setGeometry(100, 100, 400, 300)
        self.account_window.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QLabel {
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        # Get user data from cache
        try:
            with open(get_user_data_path('user_data_cache.json'), 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User data not found.")
            return

        # Create layout
        layout = QVBoxLayout()

        # Add animated title
        title_label = GradientAnimatedLabel("Account Information")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Create a frame for user info
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)

        # Display user information
        for key, value in user_data.items():
            if key in ['first_name', 'last_name', 'email']:
                label = QLabel(f"{key.replace('_', ' ').title()}: {value}")
                label.setFont(QFont("Arial", 12))
                info_layout.addWidget(label)

        layout.addWidget(info_frame)

        # Add logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setIcon(QIcon(resource_path("logout.png")))  # Assuming you have a logout icon
        logout_btn.setIconSize(QSize(20, 20))
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn, alignment=Qt.AlignCenter)

        self.account_window.setLayout(layout)
        self.account_window.show()
    def logout(self):
        # Delete user data cache and token
        try:
            os.remove(get_user_data_path('user_data_cache.json'))
            os.remove(get_user_data_path('user_token.json'))
        except FileNotFoundError:
            pass

        # Close the account window
        self.account_window.close()

        # Restart the application
        QApplication.quit()
        QProcess.startDetached(QApplication.applicationFilePath(), QApplication.arguments())


    def setup_main_content(self):
        self.main_content.setObjectName("main_content")
        
        content_layout = QVBoxLayout(self.main_content)
        content_layout.setSpacing(10)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create a horizontal layout to center the text browser
        center_layout = QHBoxLayout()
        
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_layout.addItem(left_spacer)
        
        # Chat display area
        self.text_browser = QTextBrowser()
        self.text_browser.setObjectName("chat_display")
        self.text_browser.setMaximumWidth(800)
        self.text_browser.setMinimumWidth(800)
        
        center_layout.addWidget(self.text_browser)
        
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        center_layout.addItem(right_spacer)
        
        content_layout.addLayout(center_layout)
        
        # Upload animation
        self.upload_animation = CleanLoadingAnimation(self.main_content)
        content_layout.addWidget(self.upload_animation)
        self.upload_animation.hide()  # Initially hidden
            
        # Input area
        input_layout = QHBoxLayout()
        
        left_input_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        input_layout.addItem(left_input_spacer)
        
        # Create a vertical layout for buttons
        button_layout = QVBoxLayout()
        
        # Create the clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_text_browser)
        button_layout.addWidget(self.clear_button)
        
        # Create force stop button
        self.force_stop_button = QPushButton("Force Stop")
        self.force_stop_button.setObjectName("force_stop_btn")
        self.force_stop_button.setStyleSheet("""
            QPushButton#force_stop_btn {
                background-color: #FF0000;
                color: white;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 20px;
                margin-top: 5px;
            }
            QPushButton#force_stop_btn:hover {
                background-color: #CC0000;
            }
        """)
        self.force_stop_button.hide()
        button_layout.addWidget(self.force_stop_button)
        
        # Add button layout to input layout
        input_layout.addLayout(button_layout)

        # Create the action toggle button and label
        self.action_label = GradientLabel("Action")
        self.action_toggle = ToggleButton()

        # Create a layout for the action control
        action_layout = QVBoxLayout()
        action_layout.addWidget(self.action_label)
        action_layout.addWidget(self.action_toggle)
        action_layout.setSpacing(5)
        action_layout.setContentsMargins(0, 0, 10, 0)

        # Add the action control to the input layout
        input_layout.addLayout(action_layout)

        self.input_textEdit = QTextEdit()
        self.input_textEdit.setObjectName("input_textEdit")
        self.input_textEdit.setPlaceholderText("Say Something")
        self.input_textEdit.setMaximumHeight(100)
        self.input_textEdit.setMaximumWidth(850)
        self.input_textEdit.setMinimumWidth(850)
        input_layout.addWidget(self.input_textEdit)
        
        self.send_btn = QPushButton()
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setIcon(QIcon(resource_path("send.svg")))
        self.send_btn.setIconSize(QSize(24, 24))
        self.send_btn.setFixedSize(QSize(40, 40))
        input_layout.addWidget(self.send_btn)
        
        # Add file selection button
        self.file_btn = QPushButton("Select Files")
        self.file_btn.setObjectName("file_btn")
        input_layout.addWidget(self.file_btn)

        # Add model selection combo box
        self.model_combo = QComboBox()
        self.model_combo.setObjectName("model_combo")
        self.model_combo.addItems([
            "SoulDubu-v1",
        ])
        # Set default model
        self.model_combo.setCurrentText("SoulDubu-v1")
        input_layout.addWidget(self.model_combo)

        right_input_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        input_layout.addItem(right_input_spacer)
        
        content_layout.addLayout(input_layout)

    def start_upload_animation(self):
        self.upload_animation.startAnimation()

    def stop_upload_animation(self):
        self.upload_animation.stopAnimation()

    def stop_upload_animation(self):
        if hasattr(self, 'upload_animation_timer'):
            self.upload_animation_timer.stop()
        self.upload_animation.hide()

    def clear_text_browser(self):
        self.text_browser.clear()

    def show_side_panel(self):
        # Add the side panel to the layout
        self.main_layout.insertWidget(0, self.side_panel)
        self.side_panel.show()  # Show the side panel
        self.more_icon.hide()  # Hide the "More" icon

        # Create a "Less" icon to hide the side panel
        self.less_icon = QPushButton()
        self.less_icon.setObjectName("less_icon")
        self.less_icon.setIcon(QIcon(resource_path("less.png")))
        self.less_icon.setIconSize(QSize(24, 24))
        self.less_icon.setFixedSize(QSize(40, 40))
        self.main_layout.addWidget(self.less_icon)

        # Connect the "Less" icon to a slot that hides the side panel
        self.less_icon.clicked.connect(self.hide_side_panel)

    def hide_side_panel(self):
        # Remove the side panel from the layout
        self.main_layout.removeWidget(self.side_panel)
        self.side_panel.hide()
        self.less_icon.hide()  # Hide the "Less" icon
        self.more_icon.show()  # Show the "More" icon

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("QueenDahyun")
    
    def show_engine_window(self):
        self.engine_window = EngineWindow()
        self.engine_window.show()
