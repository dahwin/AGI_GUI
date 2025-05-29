import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QGraphicsDropShadowEffect

## ==> SPLASH SCREEN
from ui_splash_screen import *

## ==> MAIN WINDOW
from ui import *

class ChatThread(QThread):
    message_received = Signal(str)

    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input

    def run(self):
        try:
            api_response = self.chat(self.user_input)
            self.message_received.emit(api_response)
        except Exception as e:
            print(f"Error in ChatThread: {e}")

    def chat(self, prompt):

        # Define the URL of your FastAPI application
        url = 'http://127.0.0.1:8000/name'


        data = {'dahwin': f"""{prompt}"""}  # Include the 'name' field in the JSON data

        # Send a POST request
        response = requests.post(url, json=data)

        # Assuming response.content is of type bytes
        ai_response_bytes = response.content

        # Decode the bytes to a string
        ai_response_str = ai_response_bytes.decode('utf-8')  # You may need to adjust the encoding based on your response

        # Use regex to extract the value associated with "AI Response"
        match = re.search(r'"AI Response":"([^"]+)"', ai_response_str)
        if match:
            response_text = match.group(1)
            print(response_text)
        else:
            print("AI Response not found in the string.")
        return response_text

## ==> GLOBALS
counter = 0


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        

        # Connect the send button click event to a custom method
        self.ui.send_btn.clicked.connect(self.send_user_message)
        self.ui.send_btn.clicked.connect(self.hide_download_completion_widgets)

        # Create an instance of ChatThread
        self.chat_thread = ChatThread("")

        # Connect the message_received signal to the display_ai_response method
        self.chat_thread.message_received.connect(self.display_ai_response)

        # Connect the Enter key press event to the send_user_message method
        self.ui.input_textEdit.setAcceptRichText(True)
        self.ui.input_textEdit.installEventFilter(self)
        # Connect the toggle_dark_mode method to the Dark mode button click event
        self.ui.pushButton_8.clicked.connect(self.ui.toggle_dark_mode)
    def hide_download_completion_widgets(self):
        self.ui.download_compelete.setParent(None)
        self.ui.additional_label_3.setParent(None)
        self.ui.downloading.setParent(None)
        self.ui.must_download_button.setParent(None)
    def eventFilter(self, obj, event):
        if obj is self.ui.input_textEdit and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Return:
            self.send_user_message()
            return True
        return super().eventFilter(obj, event)


    def send_user_message(self):
        # Get user input from the text edit
        user_input = self.ui.input_textEdit.toPlainText()

        # Display the user message immediately
        self.display_user_message(user_input)

        # Update the ChatThread's user_input
        self.chat_thread.user_input = user_input
        self.hide_download_completion_widgets()
        # Start the ChatThread
        if not self.chat_thread.isRunning():
            self.chat_thread.start()

    def display_user_message(self, user_input):
        # Access the QTextBrowser widget directly from the UI
        text_browser = self.ui.text_browser

        if text_browser:
            # Insert the user's message with logo into the QTextBrowser
            user_message = f"""<img src='user.png' width='40' height='40' style='border-radius: 20px;'> <b>user:</b><br><span style='font-size: 14pt;'>{user_input}</span><br><br>"""
            text_browser.append(user_message)

            # Set the scroll bar to the maximum value
            text_browser.verticalScrollBar().setValue(text_browser.verticalScrollBar().maximum())

    def display_ai_response(self, ai_response):
        # Access the QTextBrowser widget directly from the UI
        text_browser = self.ui.text_browser

        if text_browser:
            print("Original AI Response:", ai_response)
            # Remove newline characters from the AI response
            ai_response1 = ai_response.replace('\\n', '')
            print("Modified AI Response:", ai_response1)

            # Insert the AI response with logo into the QTextBrowser
            ai_message = f"""<img src='queendahyun.png' width='40' height='40' style='border-radius: 20px;'> <b>QueenDahyun:</b><br><span style='font-size: 14pt;'>{ai_response1}</span><br><br>"""
            text_browser.append(ai_message)

            # Set the scroll bar to the maximum value
            text_browser.verticalScrollBar().setValue(text_browser.verticalScrollBar().maximum())



# SPLASH SCREEN
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        ## UI ==> INTERFACE CODES
        ########################################################################

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


        ## DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO Advanced AI Agent")

        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> Checking Ai Model"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> UI"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):

        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MyMainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec())




