# "dahyun+darwin=dahwin"
# from PySide6.QtGui import QMovie
# import threading
# import subprocess
# import sys
# from PySide6.QtCore import QTimer
# import platform
# from PySide6 import QtCore, QtGui, QtWidgets
# from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent, QThread, Signal,QMetaObject)
# from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
# from PySide6.QtWidgets import *
# from PySide6.QtWidgets import QGraphicsDropShadowEffect,QMessageBox
# import re
# import requests

# import subprocess
# def run_wsl_command(command):
#     try:
#         subprocess.run(["wsl", "bash", "-c", command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
#     except subprocess.CalledProcessError as e:
#         print(f"Error running WSL command: {e}")



# class SetupDialog(QDialog):
#     def __init__(self, parent=None):
#         super(SetupDialog, self).__init__(parent)
#         self.setWindowTitle("QueenDahyun Set UP .......")

#         layout = QGridLayout(self)

#         # Create a QLabel to display the GIF
#         gif_label = QLabel(self)
#         movie = QMovie("./asset/load.gif")
#         if movie.isValid():
#             gif_label.setMovie(movie)
#             movie.start()
#         else:
#             print("Error loading GIF file.")

#         # Create a QLabel for the text
#         text_label = QLabel("QueenDahyun Set UP .......", self)
#         text_label.setAlignment(Qt.AlignCenter)
#         text_label.setStyleSheet("font-weight: bold; font-size: 16px;")

#         # Add widgets to the layout
#         layout.addWidget(gif_label, 1, 0, 1, 1)  # Center the GIF horizontally
#         layout.addWidget(text_label, 1, 0, 1, 2)  # Center the text

#         # Adjust the size of the dialog
#         self.resize(400, 400)  # Adjust the size as needed
#         self.setModal(True)

# # ... (Remaining code)

# class MY_QD_setup(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         tex = ''

#         # if "False" in f"""{result_list}""":
#         #     tex += "False"
#         #     print(tex)
#         # else:
#         #     tex += "True"
#         #     print(tex)

#         if tex == "False":
#             self.show_restart_message()

#     def show_restart_message(self):
#         message_box = QMessageBox()
#         message_box.setIcon(QMessageBox.Information)
#         message_box.setText("You have to install QueenDahyun Environment.\nYou must restart the PC after installing the environment!")

#         # Set style sheet for customization
#         message_box.setStyleSheet("background-color: black; color: white; font-weight: bold; font-size: 16px;")

#         # Increase the size of the QMessageBox
#         message_box.setGeometry(800, 400, 800, 400)

#         # Add "OK" and "Cancel" buttons
#         message_box.addButton(QMessageBox.Ok)
#         message_box.addButton(QMessageBox.Cancel)

#         result = message_box.exec_()

#         if result == QMessageBox.Ok:
#             print("User clicked OK")

#             # Create an instance of the SetupDialog
#             setup_dialog = SetupDialog(self)


#             # Use QTimer to close the dialog after a certain duration
#             QTimer.singleShot(5000000, lambda: setup_dialog.accept())

#             # Show the SetupDialog
#             setup_dialog.exec_()

#         elif result == QMessageBox.Cancel:
#             print("User clicked Cancel")
#             run_wsl_command("pkill -f server.py")

# def QD_Setup():
#     app = QApplication(sys.argv)
#     main_window = MY_QD_setup()
#     main_window.show()
#     sys.exit(app.exec_())