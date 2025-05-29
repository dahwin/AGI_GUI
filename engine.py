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
    QFileDialog,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
    QFormLayout,
    QSlider,
    QRadioButton
)
global engine_name, model_id,formate,max_new_token,temperature,top_p,top_k,do_sample,max_time, system_instruction,close
engine_name=None
model_id = None
formate = None
max_new_token = None
temperature = None
top_p = None
top_k = None
do_sample = None
max_time = None
system_instruction = None
close = False


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.initial_pos = None
        self.parent = parent  # Save a reference to the parent window
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(0)
        self.setStyleSheet("background-color: #DDE1F9;")
        self.setFixedHeight(55)

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

        self.min_button = QToolButton(self)
        min_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        self.max_button = QToolButton(self)
        max_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.toggle_max_restore)

        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        self.normal_button = QToolButton(self)
        normal_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.toggle_max_restore)
        self.normal_button.setVisible(False)

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

        parent.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.window_state_changed(obj.windowState())
        return super().eventFilter(obj, event)

    def toggle_max_restore(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.globalPosition().toPoint() - self.initial_pos
            self.parent.move(self.parent.pos() + delta)
            self.initial_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None

class Widget(QWidget):
    def __init__(self):
        super().__init__()
        global engine_name, model_id,formate,max_new_token,temperature,top_p,top_k,do_sample,max_time, system_instruction,close

        self.setWindowTitle("QTabWidgetDemo Demo")
        self.resize(800, 500)
        self.tab_widget = QTabWidget(self)

        self.widget_transformers = QWidget()
        self.widget_vllm = QWidget()
        self.setup_transformers_tab()
        self.setup_vllm_tab()

        self.tab_widget.addTab(self.widget_transformers, "TransFormers")
        self.tab_widget.addTab(self.widget_vllm, "VLLM")

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

        # Add Activate section
        self.activate_group = QWidget()
        activate_layout = QHBoxLayout(self.activate_group)

        self.transformers_radio = QRadioButton("Transformers")
        self.vllm_radio = QRadioButton("VLLM")

        close=False
        if engine_name!=None:
            
            if "transformers" in engine_name:
                self.transformers_radio.setChecked(True)  
            if "vllm" in engine_name:
                self.vllm_radio.setChecked(True)  
        else:
            self.transformers_radio.setChecked(True)  # Default Transformers is active

        activate_layout.addWidget(self.transformers_radio)
        activate_layout.addWidget(self.vllm_radio)
        layout.addWidget(self.activate_group)

        # Connect radio buttons to update active tab
        self.transformers_radio.toggled.connect(self.update_active_tab)
        self.vllm_radio.toggled.connect(self.update_active_tab)
    
    def setup_transformers_tab(self):
        form_layout = QFormLayout()
        # transformers_label = QLabel("TransFormers engine")
        # transformers_label.setStyleSheet("font-size: 16pt;")
        # form_layout.addRow(transformers_label)
        form_layout.addRow(QLabel(""))

        self.model_id_input = QLineEdit()
        if model_id!=None:
            self.model_id_input.setText(model_id)
        else:
            self.model_id_input.setText("meta-llama/Meta-Llama-3-8B-Instruct")
        form_layout.addRow("Model ID:", self.model_id_input)

        self.Formate_input = QComboBox()
        if model_id!=None:
            l = ["original", "awq", "gptq"]
            l = [formate] + [item for item in l if item != formate]
            self.Formate_input.addItems(l)
        else:
            self.Formate_input.addItems(["original", "awq", "gptq"])
        form_layout.addRow("Formate:", self.Formate_input)

        self.max_new_tokens_input = QSpinBox()
        self.max_new_tokens_input.setRange(1, 204800000)
        if model_id!=None :
            self.max_new_tokens_input.setValue(max_new_token)
        else:
            self.max_new_tokens_input.setValue(512)
        form_layout.addRow("Max New Tokens:", self.max_new_tokens_input)

        self.temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.temperature_slider.setRange(0, 100)
        if model_id!=None :
            self.temperature_slider.setValue(temperature*100)
        else:
            self.temperature_slider.setValue(10)
        self.temperature_slider.setTickInterval(1)
        self.temperature_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.temperature_slider.valueChanged.connect(lambda value: self.temperature_label.setText(f"Temperature: {value / 100:.2f}"))
        self.temperature_label = QLabel(f"Temperature: {self.temperature_slider.value() / 100:.2f}")
        form_layout.addRow(self.temperature_label, self.temperature_slider)

        self.top_p_slider = QSlider(Qt.Orientation.Horizontal)
        self.top_p_slider.setRange(0, 100)
        if model_id!=None:
            self.top_p_slider.setValue(top_p*100)
        else:
            self.top_p_slider.setValue(95)
        self.top_p_slider.setTickInterval(1)
        self.top_p_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.top_p_slider.valueChanged.connect(lambda value: self.top_p_label.setText(f"Top P: {value / 100:.2f}"))
        self.top_p_label = QLabel(f"Top P: {self.top_p_slider.value() / 100:.2f}")
        form_layout.addRow(self.top_p_label, self.top_p_slider)

        self.top_k_slider = QSlider(Qt.Orientation.Horizontal)
        self.top_k_slider.setRange(0, 100)
        if model_id!=None:
            self.top_k_slider.setValue(top_k*100)
        else:
            self.top_k_slider.setValue(50)
        self.top_k_slider.setTickInterval(10)
        self.top_k_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.top_k_slider.valueChanged.connect(lambda value: self.top_k_label.setText(f"Top K: {value}"))
        self.top_k_label = QLabel(f"Top K: {self.top_k_slider.value()}")
        form_layout.addRow(self.top_k_label, self.top_k_slider)

        self.do_sample_input = QComboBox()
        if model_id!=None :
            l = ["True", "False"]
            l = [do_sample] + [item for item in l if item != do_sample]
            self.do_sample_input.addItems(l)
        else:
            self.do_sample_input.addItems(["True", "False"])
        form_layout.addRow("Do Sample:", self.do_sample_input)

        self.max_time_input = QDoubleSpinBox()
        self.max_time_input.setRange(0.0, 10.0)
        if model_id!=None:
            self.max_time_input.setValue(max_time)
        else:
            self.max_time_input.setValue(1.0)
        self.max_time_input.setSingleStep(0.01)
        form_layout.addRow("Max Time:", self.max_time_input)

        # System instruction section for Transformers tab
        if model_id!=None:
            self.system_instruction = QTextEdit(system_instruction)
        else:
            self.system_instruction = QTextEdit("Your Name is QueenDahyun! You are an AGI developed by QueenDahyunAGI")
        self.system_instruction.setAcceptRichText(False)
        self.system_instruction.setPlaceholderText("Enter system instruction here")
        self.system_instruction.setMaximumHeight(100)
        form_layout.addRow("System instruction:", self.system_instruction)

        self.widget_transformers.setLayout(form_layout)

        # Connecting signals to a slot to print the updated parameters
        self.model_id_input.textChanged.connect(self.print_updated_parameters)
        self.Formate_input.currentIndexChanged.connect(self.print_updated_parameters)
        self.max_new_tokens_input.valueChanged.connect(self.print_updated_parameters)
        self.temperature_slider.valueChanged.connect(self.print_updated_parameters)
        self.top_p_slider.valueChanged.connect(self.print_updated_parameters)
        self.top_k_slider.valueChanged.connect(self.print_updated_parameters)
        self.do_sample_input.currentIndexChanged.connect(self.print_updated_parameters)
        self.max_time_input.valueChanged.connect(self.print_updated_parameters)
        self.system_instruction.textChanged.connect(self.print_updated_parameters)


    def setup_vllm_tab(self):
        
        form_layout = QFormLayout()

        form_layout.addRow(QLabel(""))

        self.vllm_model_id_input = QLineEdit()
        if model_id!=None:
            print('yes')
            self.vllm_model_id_input.setText(model_id)
        else:
            self.vllm_model_id_input.setText("meta-llama/Meta-Llama-3-8B-Instruct")
        form_layout.addRow("Model ID:", self.vllm_model_id_input)

        self.vllm_Formate_input = QComboBox()
        if model_id!=None :
            l = ["original", "awq", "gptq"]
            l = [formate] + [item for item in l if item != formate]
            self.vllm_Formate_input.addItems(l)
        else:
            self.vllm_Formate_input.addItems(["gptq","original", "awq"])
        form_layout.addRow("Formate:", self.vllm_Formate_input)

        self.vllm_max_new_tokens_input = QSpinBox()
        self.vllm_max_new_tokens_input.setRange(1, 204800000)
        if model_id!=None :
            self.vllm_max_new_tokens_input.setValue(max_new_token)
        else:
            self.vllm_max_new_tokens_input.setValue(512)
        form_layout.addRow("Max New Tokens:", self.vllm_max_new_tokens_input)

        self.vllm_temperature_slider = QSlider(Qt.Orientation.Horizontal)
        self.vllm_temperature_slider.setRange(0, 100)
        if model_id!=None :
            self.vllm_temperature_slider.setValue(temperature*100)
        else:
            self.vllm_temperature_slider.setValue(10)
        self.vllm_temperature_slider.setTickInterval(1)
        self.vllm_temperature_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.vllm_temperature_slider.valueChanged.connect(lambda value: self.vllm_temperature_label.setText(f"Temperature: {value / 100:.2f}"))
        self.vllm_temperature_label = QLabel(f"Temperature: {self.vllm_temperature_slider.value() / 100:.2f}")
        form_layout.addRow(self.vllm_temperature_label, self.vllm_temperature_slider)

        self.vllm_top_p_slider = QSlider(Qt.Orientation.Horizontal)
        self.vllm_top_p_slider.setRange(0, 100)
        if model_id!=None :
            self.vllm_top_p_slider.setValue(top_p*100)
        else:
            self.vllm_top_p_slider.setValue(95)
        self.vllm_top_p_slider.setTickInterval(1)
        self.vllm_top_p_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.vllm_top_p_slider.valueChanged.connect(lambda value: self.vllm_top_p_label.setText(f"Top P: {value / 100:.2f}"))
        self.vllm_top_p_label = QLabel(f"Top P: {self.vllm_top_p_slider.value() / 100:.2f}")
        form_layout.addRow(self.vllm_top_p_label, self.vllm_top_p_slider)

        self.vllm_top_k_slider = QSlider(Qt.Orientation.Horizontal)
        self.vllm_top_k_slider.setRange(0, 100)
        if model_id!=None:
            self.vllm_top_k_slider.setValue(top_k*100)
        else:
            self.vllm_top_k_slider.setValue(50)
        self.vllm_top_k_slider.setTickInterval(10)
        self.vllm_top_k_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.vllm_top_k_slider.valueChanged.connect(lambda value: self.vllm_top_k_label.setText(f"Top K: {value}"))
        self.vllm_top_k_label = QLabel(f"Top K: {self.vllm_top_k_slider.value()}")
        form_layout.addRow(self.vllm_top_k_label, self.vllm_top_k_slider)

        self.vllm_do_sample_input = QComboBox()
        if model_id!=None :
            l = ["True", "False"]
            l = [do_sample] + [item for item in l if item != do_sample]
            self.vllm_do_sample_input.addItems(l)
        else:
            self.vllm_do_sample_input.addItems(["True", "False"])
        form_layout.addRow("Do Sample:", self.vllm_do_sample_input)

        self.vllm_max_time_input = QDoubleSpinBox()
        self.vllm_max_time_input.setRange(0.0, 10.0)
        if model_id!=None :
            self.vllm_max_time_input.setValue(max_time)
        else:
            self.vllm_max_time_input.setValue(1.0)
        self.vllm_max_time_input.setSingleStep(0.01)
        form_layout.addRow("Max Time:", self.vllm_max_time_input)

        # System instruction section for VLLM tab
        if model_id!=None:
            self.vllm_system_instruction = QTextEdit(system_instruction)
        else:
            self.vllm_system_instruction = QTextEdit("Your Name is QueenDahyun! You are an AGI developed by QueenDahyunAGI")
        self.vllm_system_instruction.setAcceptRichText(False)
        self.vllm_system_instruction.setPlaceholderText("Enter system instruction here")
        self.vllm_system_instruction.setMaximumHeight(100)
        form_layout.addRow("System instruction:", self.vllm_system_instruction)
        self.widget_vllm.setLayout(form_layout)

        # Connecting signals to a slot to print the updated parameters
        self.vllm_model_id_input.textChanged.connect(self.print_updated_parameters)
        self.vllm_Formate_input.currentIndexChanged.connect(self.print_updated_parameters)
        self.vllm_max_new_tokens_input.valueChanged.connect(self.print_updated_parameters)
        self.vllm_temperature_slider.valueChanged.connect(self.print_updated_parameters)
        self.vllm_top_p_slider.valueChanged.connect(self.print_updated_parameters)
        self.vllm_top_k_slider.valueChanged.connect(self.print_updated_parameters)
        self.vllm_do_sample_input.currentIndexChanged.connect(self.print_updated_parameters)
        self.vllm_max_time_input.valueChanged.connect(self.print_updated_parameters)
        self.vllm_system_instruction.textChanged.connect(self.print_updated_parameters)

    def update_active_tab(self):
        if self.transformers_radio.isChecked():
            self.tab_widget.setCurrentIndex(0)
        elif self.vllm_radio.isChecked():
            self.tab_widget.setCurrentIndex(1)

    def print_updated_parameters(self):
        print("Updated Parameters:")
        global engine_name, model_id,formate,max_new_token,temperature,top_p,top_k,do_sample,max_time, system_instruction,close


        if close!=True:

            if self.transformers_radio.isChecked():
                engine_name='transformers'
                print(f"Engine: {engine_name}")
                model_id = self.model_id_input.text()
                print(f"Model ID: {model_id}")
                formate = self.Formate_input.currentText()
                print(f"Formate: {formate}")
                max_new_token = self.max_new_tokens_input.value()
                print(f"Max New Tokens: {max_new_token}")
                temperature = self.temperature_slider.value() / 100
                print(f"Temperature: {temperature}")
                top_p = self.top_p_slider.value() / 100
                print(f"Top P: {top_p}")
                top_k = self.top_k_slider.value()
                print(f"Top K: {(top_k)}")
                do_sample = self.do_sample_input.currentText()
                print(f"Do Sample: {do_sample}")
                max_time = self.max_time_input.value()
                print(f"Max Time: {max_time}")
                system_instruction = self.system_instruction.toPlainText()
                print(f"Transformers System Instruction: {system_instruction}")

                model_id = model_id
                formate = formate
                max_new_token = max_new_token
                temperature = temperature
                top_p = top_p
                top_k = top_k
                do_sample = do_sample
                max_time = max_time
                system_instruction = system_instruction

            if self.vllm_radio.isChecked():
                
                engine_name='vllm'
                print(f"Engine: {engine_name}")
                model_id = self.vllm_model_id_input.text()
                print(f"Model ID: {model_id}")
                formate = self.vllm_Formate_input.currentText()
                print(f"Formate: {formate}")
                max_new_token=self.vllm_max_new_tokens_input.value()
                print(f"Max New Tokens: {max_new_token}")
                temperature = self.vllm_temperature_slider.value() / 100
                print(f"Temperature: {temperature}")
                top_p = self.vllm_top_p_slider.value() / 100
                print(f"Top P: {top_p}")
                top_k = self.vllm_top_k_slider.value()
                print(f"Top K: {top_k}")
                do_sample= self.vllm_do_sample_input.currentText()
                print(f"Do Sample: {do_sample}")
                max_time = self.vllm_max_time_input.value()
                print(f"Max Time: {max_time}")
                system_instruction = self.vllm_system_instruction.toPlainText()
                print(f"VLLM System Instruction: {system_instruction}")

                model_id = model_id
                formate = formate
                max_new_token = max_new_token
                temperature = temperature
                top_p = top_p
                top_k = top_k
                do_sample = do_sample
                max_time = max_time
                system_instruction = system_instruction
        else:
                
                print('else')
                print(f"Engine: {engine_name}")
                print(f"Model ID: {model_id}")

                print(f"Formate: {formate}")

                print(f"Max New Tokens: {max_new_token}")

                print(f"Temperature: {temperature}")

                print(f"Top P: {top_p}")

                print(f"Top K: {(top_k)}")

                print(f"Do Sample: {do_sample}")

                print(f"Max Time: {max_time}")

                print(f"Transformers System Instruction: {system_instruction}")
                

        
        return engine_name, model_id,formate,max_new_token,temperature,top_p,top_k,do_sample,max_time,system_instruction
    

    def enable_dark_mode(self):
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)
        self.findChild(CustomTitleBar).apply_dark_mode()

    def enable_light_mode(self):
        app.setStyle("Fusion")
        app.setPalette(app.style().standardPalette())
        self.findChild(CustomTitleBar).apply_light_mode()

    def set_wallpaper(self):
        wallpaper_path, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)")
        if wallpaper_path:
            self.setStyleSheet(f"QWidget {{ background-image: url({wallpaper_path}); background-position: center; }}")



from PySide6.QtCore import Qt

class EngineWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a custom title bar
        custom_title_bar = CustomTitleBar(self)  # Pass self as the parent widget

        # Set window flags to make the window frameless
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Set the central widget to a main widget
        main_widget = Widget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout to add the title bar and the main widget
        layout = QVBoxLayout()
        layout.addWidget(custom_title_bar)
        layout.addWidget(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Set the layout to the central widget of the EngineWindow
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    def closeEvent(self, event):
        global close
        close = True
        event.accept()  # Accept the event to close the window


if __name__ == "__main__":
    app = QApplication([])

    main_window = QMainWindow()
    custom_title_bar = CustomTitleBar(main_window)
    main_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    main_widget = Widget()
    main_window.setCentralWidget(main_widget)

    layout = QVBoxLayout()
    layout.addWidget(custom_title_bar)
    layout.addWidget(main_widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    main_frame = QWidget()
    main_frame.setLayout(layout)
    main_window.setCentralWidget(main_frame)

    main_window.resize(1024, 768)
    main_window.show()

    app.exec()











# # class EngineWindow(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         main_window = QMainWindow()
# #         custom_title_bar = CustomTitleBar(main_window)
# #         main_window.setWindowFlags(Qt.WindowType.FramelessWindowHint)

# #         main_widget = Widget()
# #         main_window.setCentralWidget(main_widget)

# #         layout = QVBoxLayout()
# #         layout.addWidget(custom_title_bar)
# #         layout.addWidget(main_widget)
# #         layout.setContentsMargins(0, 0, 0, 0)
# #         layout.setSpacing(0)

# #         main_frame = QWidget()
# #         main_frame.setLayout(layout)
# #         main_window.setCentralWidget(main_frame)

# #         main_window.resize(1024, 768)
# #         main_window.show()
