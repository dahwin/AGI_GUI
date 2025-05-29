## ==> SPLASH SCREEN
from ui_splash_screen import *

## ==> MAIN WINDOW
from ui import *
from ui import again
import threading
import subprocess
import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, QThread, Signal,QMetaObject)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QGraphicsDropShadowEffect,QMessageBox
import re
import requests
from feature import is_feature_enabled, setup,install,dahyun_check_file,close_wsl_window,wsl_update_download,wsl_update_install
import subprocess
tex = ''
result_list = is_feature_enabled()
if "False" in f"""{result_list}""":
    tex+="False"
    print(tex)
else:
    tex+="True"
    print(tex)
def run_wsl_command(command):
    try:
        subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)

    except subprocess.CalledProcessError as e:
        print(f"Error running WSL command: {e}")
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
        # if again == True:
        #     text = dahyun_check_file(selected_option)
        #     if "File exists" in text:

        #         print("File exists")
        #         # run_wsl_command("python3 /root/server/server.py")
        #         # time.sleep(5)
        #         url = 'http://127.0.0.1:8000/llm'
        #         print(f"selected_option: {selected_option}")
        #         data = {'name': f'{selected_option}'}  # Include the 'name' field in the JSON data
        #         response = requests.post(url, json=data)
        #         print(response.json())

        # Define the URL of your FastAPI application
        url = 'http://127.0.0.1:8000/name'


        data = {'dahwin': f"""{prompt}"""}  # Include the 'name' field in the JSON data

        # Send a POST request
        response = requests.post(url, json=data)

        # Assuming response.content is of type bytes
        ai_response_bytes = response.content

        try:
            # Decode the bytes to a string with 'utf-8' encoding
            ai_response_str = ai_response_bytes.decode('utf-8')

            # Use regex to extract the value associated with "AI Response"
            match = re.search(r'"AI Response":"([^"]+)"', ai_response_str)
            if match:
                response_text = match.group(1)
                print(response_text)
            else:
                print("AI Response not found in the string.")
        except UnicodeDecodeError as e:
            print(f"Error decoding AI response: {e}")
            response_text = "Error decoding AI response"

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


        self.closeEvent = self.custom_close_event
    def custom_close_event(self, event):
        # Call the close_wsl_window function
        close_wsl_window()

        # Call the original closeEvent to handle the standard closing behavior
        super().closeEvent(event)
    def hide_download_completion_widgets(self):
        try:
            self.ui.download_compelete.setParent(None)
            self.ui.additional_label_3.setParent(None)
            self.ui.downloading.setParent(None)
            self.ui.must_download_button.setParent(None)
        except:
            pass
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
def show_restart_message():
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Information)
    message_box.setText("You have to install QueenDahyun Environment.\nYou must restart the PC after installing the environment!")

    # Set style sheet for customization
    message_box.setStyleSheet("background-color: black; color: white; font-weight: bold; font-size: 16px;")

    # Increase the size of the QMessageBox
    message_box.setGeometry(800, 400, 800, 400)

    # Add "OK" and "Cancel" buttons
    message_box.addButton(QMessageBox.Ok)
    message_box.addButton(QMessageBox.Cancel)

    result = message_box.exec_()

    if result == QMessageBox.Ok:
        print("User clicked OK")

        # Create a QDialog to show the GIF
        gif_dialog = QDialog()
        gif_dialog.setWindowTitle("Set UP...")
        gif_dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)

        layout = QVBoxLayout(gif_dialog)

        # Create a QLabel to display the GIF
        gif_label = QLabel(gif_dialog)
        movie = QMovie("load.gif")
        gif_label.setMovie(movie)
        movie.start()

        layout.addWidget(gif_label)

        # Adjust the size and position of the dialog
        gif_dialog.setGeometry(400, 200, 400, 200)
        gif_dialog.setModal(True)

        gif_dialog.show()

        # Run the necessary functions in the background
        threading.Thread(target=wsl_update_download).start()
        threading.Thread(target=wsl_update_install).start()
        threading.Thread(target=setup, args=(result_list,)).start()

        # # Close the dialog after a certain duration (adjust as needed)
        QTimer.singleShot(10000, gif_dialog.accept)

    elif result == QMessageBox.Cancel:
        print("User clicked Cancel")
        run_wsl_command("pkill -f server.py")
        sys.exit(0)  # Terminate the application

def run_server():
    run_wsl_command("python3 /root/server/server.py")

def run_additional_code():
    # Code from the provided script
    app = QApplication(sys.argv)

    if  "False" in tex:
        # Display the restart message box
        show_restart_message()

    # Create and show the SplashScreen
    window = SplashScreen()

    sys.exit(app.exec_())


# Create two threads for running the server and additional code
server_thread = threading.Thread(target=run_server)
additional_code_thread = threading.Thread(target=run_additional_code)

# Start the threads
server_thread.start()
additional_code_thread.start()

# Wait for both threads to finish
server_thread.join()
additional_code_thread.join()