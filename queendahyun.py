import sys
import os
import threading
import subprocess
import signal
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QWidget
from PySide6.QtGui import QColor, QIcon
from others import get_user_data_path
# Import your custom modules
from ui_splash_screen import Ui_SplashScreen
from main_process import MyMainWindow
# ,sendurl
from desktop_singin import FuturisticAuthWindow

# Remove process and thread globals
# process = None
# thread = None



class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # Set up progress bar animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)
        
        self.counter = 0
        self.ui.label_description.setText("<strong>WELCOME</strong> TO Advanced AI Agent")
        QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> Checking AI Model"))
        QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> UI"))
        
        self.show()

    def progress(self):
        self.ui.progressBar.setValue(self.counter)

        if self.counter > 100:
            self.timer.stop()
            # self.main = MyMainWindow()
            # self.main.show()
            if self.is_user_logged_in():
                self.main = MyMainWindow()
                self.main.show()
            else:
                self.auth_window = FuturisticAuthWindow()
                self.auth_window.show()
            self.close()

        self.counter += 1

    def is_user_logged_in(self):
        return os.path.exists(get_user_data_path('user_token.json'))

    def on_login_successful(self):
        self.auth_window.close()
        self.main = MyMainWindow()
        self.main.show()

def main():
    # global thread, process  # No longer needed
    app = QApplication(sys.argv)
    
    # Set app icon
    app_icon = QIcon("queendahyun.png")
    app.setWindowIcon(app_icon)
    
    # Start the subprocess when the app opens (REMOVED)
    # thread = threading.Thread(target=run_executable)
    # thread.start()
    
    # Create and show the splash screen
    window = SplashScreen()
    
    # Set up clean-up function to be called when the app is about to quit
    # app.aboutToQuit.connect(cleanup)  # No longer needed
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()