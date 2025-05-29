STYLE_SHEET = f"""""""""
QWidget {
    background-color: transparent;
    color: white;
    font-family: Arial, sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #219FD5, stop:1 #B2B5D3);
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
                             stop:0 #219FD5, stop:1 #B2B5D3);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

#send_btn:hover, #engine_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #219FD5, stop:1 #B2B5D3);
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
                              stop:0 #4D6C80, stop:1 #26B2F3);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                         stop:0 #219FD5, stop:1 #B2B5D3);
}

QRadioButton, QCheckBox {
    color: white;
}
"""""""""