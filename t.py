import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from engine import EngineWindow

class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QSize(800, 600))
        
        # Set up the central widget and main layout
        self.centralwidget = QWidget(MainWindow)
        self.main_layout = QHBoxLayout(self.centralwidget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Set up the side panel
        self.setup_side_panel()
        
        # Set up the main content area
        self.setup_main_content()
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Set up the menu bar
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        MainWindow.setMenuBar(self.menubar)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    
    def setup_side_panel(self):
        self.side_panel = QWidget()
        self.side_panel.setObjectName("side_panel")
        self.side_panel.setMinimumWidth(250)
        self.side_panel.setMaximumWidth(300)
        
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setSpacing(10)
        side_layout.setContentsMargins(10, 10, 10, 10)
        
        # New chat button
        self.new_chat_btn = QPushButton("New Conversation")
        self.new_chat_btn.setObjectName("new_chat_btn")
        side_layout.addWidget(self.new_chat_btn)
        
        # Chat list
        self.chat_list = QListWidget()
        self.chat_list.setObjectName("chat_list")
        side_layout.addWidget(self.chat_list)
        
        # Menu items
        menu_items = ["Sponsor us", "Future Plan", "Log In"]
        for item in menu_items:
            btn = QPushButton(item)
            btn.setObjectName(f"{item.lower().replace(' ', '_')}_btn")
            side_layout.addWidget(btn)
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItem("QueenDahyun")
        self.model_combo.setObjectName("model_combo")
        side_layout.addWidget(self.model_combo)
        
        self.main_layout.addWidget(self.side_panel)
    
    def setup_main_content(self):
        self.main_content = QWidget()
        self.main_content.setObjectName("main_content")
        
        content_layout = QVBoxLayout(self.main_content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Chat display area
        self.chat_display = QTextBrowser()
        self.chat_display.setObjectName("chat_display")
        content_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setObjectName("input_text")
        self.input_text.setPlaceholderText("Say Something")
        self.input_text.setMaximumHeight(100)
        input_layout.addWidget(self.input_text)
        
        self.send_btn = QPushButton()
        self.send_btn.setObjectName("send_btn")
        self.send_btn.setIcon(QIcon("./asset/send.svg"))
        self.send_btn.setIconSize(QSize(24, 24))
        self.send_btn.setFixedSize(QSize(40, 40))
        input_layout.addWidget(self.send_btn)
        
        content_layout.addLayout(input_layout)
        
        # Engine button
        self.engine_btn = QPushButton("Engine || AI Models")
        self.engine_btn.setObjectName("engine_btn")
        self.engine_btn.clicked.connect(self.show_engine_window)
        content_layout.addWidget(self.engine_btn, alignment=Qt.AlignRight)
        
        self.main_layout.addWidget(self.main_content)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("QueenDahyun")
    
    def show_engine_window(self):
        self.engine_window = EngineWindow()
        self.engine_window.show()

# Set the style sheet
STYLE_SHEET = """
QWidget {
    font-family: Arial, sans-serif;
}

#side_panel {
    background-color: #2C3E50;
    color: white;
}

#new_chat_btn, #sponsor_us_btn, #future_plan_btn, #log_in_btn {
    background-color: #34495E;
    color: white;
    border: none;
    padding: 10px;
    text-align: left;
    border-radius: 5px;
}

#new_chat_btn:hover, #sponsor_us_btn:hover, #future_plan_btn:hover, #log_in_btn:hover {
    background-color: #4A6785;
}

#chat_list {
    background-color: transparent;
    color: white;
    border: none;
}

#chat_list::item {
    padding: 10px;
    border-radius: 5px;
}

#chat_list::item:selected {
    background-color: #4A6785;
}

#model_combo {
    background-color: #34495E;
    color: white;
    border: none;
    padding: 5px;
    border-radius: 5px;
}

#main_content {
    background-color: #ECF0F1;
}

#chat_display {
    background-color: white;
    border: 1px solid #BDC3C7;
    border-radius: 5px;
    padding: 10px;
}

#input_text {
    border: 1px solid #BDC3C7;
    border-radius: 5px;
    padding: 10px;
}

#send_btn {
    background-color: #3498DB;
    border: none;
    border-radius: 20px;
}

#send_btn:hover {
    background-color: #2980B9;
}

#engine_btn {
    background-color: #2ECC71;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
}

#engine_btn:hover {
    background-color: #27AE60;
}
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())