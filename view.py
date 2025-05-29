import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class ToggleStopButton(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # Toggle Button
        self.toggle_button = QPushButton("Start")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border: 2px solid #243689;
                border-radius: 15px;
                background-color: #000000;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #B2B5D3;
            }
        """)
        self.layout.addWidget(self.toggle_button)

        # Stop Button
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border: 2px solid #FF0000;
                border-radius: 15px;
                background-color: #FF0000;
                color: white;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #808080;
                border-color: #808080;
            }
        """)
        self.stop_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.stop_button)

        # Connect signals
        self.toggle_button.toggled.connect(self.on_toggle)
        self.stop_button.clicked.connect(self.on_stop)

    def on_toggle(self, checked):
        if checked:
            self.toggle_button.setText("Running")
            self.stop_button.setEnabled(True)  # Enable stop button when toggled on
        else:
            self.toggle_button.setText("Start")
            self.stop_button.setEnabled(False)  # Disable stop button when toggled off

    def on_stop(self):
        # Execute the stop functionality
        asyncio.run(self.set_done())
        self.toggle_button.setChecked(False)  # Reset the toggle button

    async def set_done(self):
        # Placeholder for async stop functionality
        print("Stop functionality executed")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Toggle and Stop Button Example")
        self.setGeometry(100, 100, 300, 100)

        # Create an instance of ToggleStopButton
        self.toggle_stop_button = ToggleStopButton()
        self.setCentralWidget(self.toggle_stop_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Execute the application
    sys.exit(app.exec())