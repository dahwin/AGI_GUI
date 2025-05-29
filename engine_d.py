from PySide6.QtCore import QSize, Qt, QEvent
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QPushButton,
    QFileDialog
)
from PySide6.QtWidgets import QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QFormLayout,QSlider
# app = QApplication([])
class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(0)
        # Set background color to #DDE1F9
        self.setStyleSheet("background-color: #DDE1F9;")
        self.setFixedHeight(55)  # Set the height of the title bar

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setStyleSheet(
            """font-weight: bold;
               color: black
            """
        )
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if title := parent.windowTitle():
            self.title.setText(title)
        title_bar_layout.addWidget(self.title)

        # Min button
        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)

        # Add buttons
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(53, 53))
            button.setStyleSheet(
                """QToolButton {
                     background-color: #DDE1F9;
                     border: none;
                }
                QToolButton:hover {
                     background-color: lightgray;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def apply_dark_mode(self):
        self.setStyleSheet("background-color: #353535; color: white;")
        for button in [self.min_button, self.normal_button, self.max_button, self.close_button]:
            button.setStyleSheet(
                """QToolButton {
                     background-color: #353535;
                     border: none;
                     color: white;
                }
                QToolButton:hover {
                     background-color: #454545;
                }
                """
            )
        self.title.setStyleSheet(
            """font-weight: bold;
               color: white
            """
        )

    def apply_light_mode(self):
        self.setStyleSheet("background-color: #DDE1F9; color: black;")
        for button in [self.min_button, self.normal_button, self.max_button, self.close_button]:
            button.setStyleSheet(
                """QToolButton {
                     background-color: #DDE1F9;
                     border: none;
                     color: black;
                }
                QToolButton:hover {
                     background-color: lightgray;
                }
                """
            )
        self.title.setStyleSheet(
            """font-weight: bold;
               color: black
            """
        )

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTabWidgetDemo Demo")
        self.resize(800, 500)  # Set initial size for the window
        self.tab_widget = QTabWidget(self)
        
        # Transformers & Vllm
        self.widget_transformers = QWidget()
        self.widget_vllm = QWidget()
        self.setup_transformers_tab()

        self.setup_vllm_tab()



        # Appearance
        self.widget_appearance = QWidget()
        appearance_layout = QVBoxLayout(self.widget_appearance)
        self.dark_mode_button = QPushButton("Dark Mode")
        self.light_mode_button = QPushButton("Light Mode")
        self.wallpaper_button = QPushButton("Set Wallpaper from PC")
        appearance_layout.addWidget(self.dark_mode_button)
        appearance_layout.addWidget(self.light_mode_button)
        appearance_layout.addWidget(self.wallpaper_button)

        self.dark_mode_button.clicked.connect(self.enable_dark_mode)
        self.light_mode_button.clicked.connect(self.enable_light_mode)
        self.wallpaper_button.clicked.connect(self.set_wallpaper)

        self.tab_widget.addTab(self.widget_transformers, "TransFormers")
        self.tab_widget.addTab(self.widget_vllm, "VLLM")
        self.tab_widget.addTab(self.widget_appearance, "Appearance")

        # Apply styles to the tabs
        self.tab_widget.setStyleSheet('''
            QTabWidget::pane {
                border: 1px solid #FAF8FF;
                border-radius: 6px;
                background: white;
            }
            QTabBar::tab {
                background-color: #DDE1F9;
                border: 1px solid #FAF8FF;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                font-size: 14px;
                color: black;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #DDE1F9, stop: 1 #FAF8FF);
            }
        ''')

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def setup_transformers_tab(self):
        form_layout = QFormLayout()
        # Add QLabel at the beginning
        transformers_label = QLabel("TransFormers engine")
        transformers_label.setStyleSheet("font-size: 16pt;")  # Set font size using CSS
        form_layout.addRow(transformers_label)
        # Add an empty row for space
        form_layout.addRow(QLabel(""))  # Empty QLabel

        # Model ID
        self.model_id_input = QLineEdit()
        self.model_id_input.setText("meta-llama/Meta-Llama-3-8B-Instruct")  # Set default value
        form_layout.addRow("Model ID:", self.model_id_input)

        # Formate
        self.Formate_input = QComboBox()
        self.Formate_input.addItems(["original", "awq", "gptq"])  # Add more options as needed
        form_layout.addRow("Formate:", self.Formate_input)

        # Max New Tokens
        self.max_new_tokens_input = QSpinBox()
        self.max_new_tokens_input.setRange(1, 204800000)
        self.max_new_tokens_input.setValue(512)
        form_layout.addRow("Max New Tokens:", self.max_new_tokens_input)

        # Temperature
        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(80)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.temperature_slider.valueChanged.connect(lambda value: self.temperature_label.setText(f"Temperature: {value / 100:.2f}"))
        self.temperature_label = QLabel(f"Temperature: {self.temperature_slider.value() / 100:.2f}")
        form_layout.addRow(self.temperature_label, self.temperature_slider)

        # Top P
        self.top_p_slider = QSlider(Qt.Orientation.Horizontal)
        self.top_p_slider.setRange(0, 100)
        self.top_p_slider.setValue(95)
        self.top_p_slider.setTickInterval(1)
        self.top_p_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.top_p_slider.valueChanged.connect(lambda value: self.top_p_label.setText(f"Top P: {value / 100:.2f}"))
        self.top_p_label = QLabel(f"Top P: {self.top_p_slider.value() / 100:.2f}")
        form_layout.addRow(self.top_p_label, self.top_p_slider)

        # Top K
        self.top_k_slider = QSlider(Qt.Orientation.Horizontal)
        self.top_k_slider.setRange(0, 100)  # Ensure the range covers the full spectrum you need
        self.top_k_slider.setValue(50)
        self.top_k_slider.setTickInterval(10)  # Adjust tick interval if needed
        self.top_k_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.top_k_slider.valueChanged.connect(lambda value: self.top_k_label.setText(f"Top K: {value}"))
        self.top_k_label = QLabel(f"Top K: {self.top_k_slider.value()}")
        form_layout.addRow(self.top_k_label, self.top_k_slider)


        # System_Instruction
        self.System_Instruction_input = QLineEdit()
        self.System_Instruction_input.setText("Enter your default system instruction here.")  # Set default text
        form_layout.addRow("System Instruction:", self.System_Instruction_input)

        self.widget_transformers.setLayout(form_layout)





    def setup_vllm_tab(self):
        form_layout = QFormLayout()

        # Add QLabel at the beginning
        transformers_label = QLabel("VLLM engine")
        transformers_label.setStyleSheet("font-size: 16pt;")  # Set font size using CSS
        form_layout.addRow(transformers_label)
        # Add an empty row for space
        form_layout.addRow(QLabel(""))  # Empty QLabel

        # Model ID
        self.model_id_input = QLineEdit()
        self.model_id_input.setText("meta-llama/Meta-Llama-3-8B-Instruct")  # Set default value
        form_layout.addRow("Model ID:", self.model_id_input)

        # Formate
        self.Formate_input = QComboBox()
        self.Formate_input.addItems(["original", "awq", "gptq"])  # Add more options as needed
        form_layout.addRow("Formate:", self.Formate_input)

        # Max New Tokens
        self.max_new_tokens_input = QSpinBox()
        self.max_new_tokens_input.setRange(1, 2048000)
        self.max_new_tokens_input.setValue(512)
        form_layout.addRow("Max New Tokens:", self.max_new_tokens_input)

        # Temperature
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0.0, 1.0)
        self.temperature_input.setDecimals(2)
        self.temperature_input.setSingleStep(0.01)
        self.temperature_input.setValue(0.8)
        form_layout.addRow("Temperature:", self.temperature_input)

        # Top P
        self.top_p_input = QDoubleSpinBox()
        self.top_p_input.setRange(0.0, 1.0)
        self.top_p_input.setDecimals(2)
        self.top_p_input.setSingleStep(0.01)
        self.top_p_input.setValue(0.95)
        form_layout.addRow("Top P:", self.top_p_input)

        # Top K
        self.top_k_input = QSpinBox()
        self.top_k_input.setRange(0, 1000)
        self.top_k_input.setValue(50)
        form_layout.addRow("Top K:", self.top_k_input)

        # System_Instruction
        self.System_Instruction_input = QLineEdit()
        self.System_Instruction_input.setText("Enter your default system instruction here.")  # Set default text
        form_layout.addRow("System Instruction:", self.System_Instruction_input)

        self.widget_transformers.setLayout(form_layout)
    def print_default_tran_model_params(self,new_text):
        print("Default Transformers Parameters:")
        print(f"Model ID: {new_text}")




    def enable_dark_mode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(dark_palette)
        
        self.tab_widget.setStyleSheet('''
            QTabWidget::pane {
                border: 1px solid #2A2A2A;
                border-radius: 6px;
                background: #353535;
            }
            QTabBar::tab {
                background-color: #353535;
                border: 1px solid #2A2A2A;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                font-size: 14px;
                color: white;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #505050, stop: 1 #353535);
            }
        ''')

        self.widget_transformers.setStyleSheet("background-color: #353535; color: white;")
        self.widget_vllm.setStyleSheet("background-color: #353535; color: white;")
        self.widget_appearance.setStyleSheet("background-color: #353535; color: white;")
        self.dark_mode_button.setStyleSheet("background-color: #505050; color: white;")
        self.light_mode_button.setStyleSheet("background-color: #505050; color: white;")
        self.wallpaper_button.setStyleSheet("background-color: #505050; color: white;")

    def enable_light_mode(self):
        app.setPalette(app.style().standardPalette())
        
        self.tab_widget.setStyleSheet('''
            QTabWidget::pane {
                border: 1px solid #FAF8FF;
                border-radius: 6px;
                background: white;
            }
            QTabBar::tab {
                background-color: #DDE1F9;
                border: 1px solid #FAF8FF;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 2px;
                font-size: 14px;
                color: black;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                  stop: 0 #DDE1F9, stop: 1 #FAF8FF);
            }
        ''')

        self.widget_transformers.setStyleSheet("background-color: white; color: black;")
        self.widget_vllm.setStyleSheet("background-color: white; color: black;")
        self.widget_appearance.setStyleSheet("background-color: white; color: black;")
        self.dark_mode_button.setStyleSheet("background-color: #DDE1F9; color: black;")
        self.light_mode_button.setStyleSheet("background-color: #DDE1F9; color: black;")
        self.wallpaper_button.setStyleSheet("background-color: #DDE1F9; color: black;")

    def set_wallpaper(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.setStyleSheet(f"background-image: url({file_path}); background-position: center; background-repeat: no-repeat;")

class Engine_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Title Bar with Tabs")
        self.resize(800, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)

        self.widget = Widget()

        work_space_layout = QVBoxLayout()
        work_space_layout.setContentsMargins(11, 11, 11, 11)
        work_space_layout.addWidget(self.widget)

        central_widget_layout = QVBoxLayout()
        central_widget_layout.setContentsMargins(0, 0, 0, 0)
        central_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        central_widget_layout.addWidget(self.title_bar)
        central_widget_layout.addLayout(work_space_layout)

        central_widget.setLayout(central_widget_layout)
        self.setCentralWidget(central_widget)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.initial_pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.initial_pos is not None:
            self.window().move(self.window().pos() + event.pos() - self.initial_pos)

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

    def apply_dark_mode(self):
        self.title_bar.apply_dark_mode()
        self.widget.enable_dark_mode()

    def apply_light_mode(self):
        self.title_bar.apply_light_mode()
        self.widget.enable_light_mode()

if __name__ == "__main__":
    app = QApplication([])
    window = Engine_MainWindow()
    window.show()
    app.exec()
