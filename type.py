# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QScrollArea, QFrame
# from PySide6.QtCore import Qt, QSize
# from PySide6.QtGui import QPixmap, QPalette, QColor

# class YouTubeLikeUI(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("YouTube-Like UI")
#         self.setGeometry(100, 100, 800, 600)

#         # Main Layout
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)
#         main_layout = QVBoxLayout(main_widget)

#         # Header
#         header = QWidget()
#         header_layout = QHBoxLayout(header)
#         header.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5f6d, stop:1 #ffc371); padding: 10px;")

#         logo = QLabel("YouTube")
#         logo.setStyleSheet("font-size: 24px; color: white; font-weight: bold;")
#         header_layout.addWidget(logo)

#         search_bar = QLineEdit()
#         search_bar.setPlaceholderText("Search")
#         search_bar.setStyleSheet("background: white; border-radius: 15px; padding: 5px 10px;")
#         header_layout.addWidget(search_bar)

#         search_button = QPushButton("Search")
#         search_button.setStyleSheet("background: #ff5f6d; color: white; border-radius: 15px; padding: 5px 10px;")
#         header_layout.addWidget(search_button)

#         main_layout.addWidget(header)

#         # Video List
#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_area.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff5f6d, stop:1 #ffc371);")

#         scroll_widget = QWidget()
#         scroll_layout = QVBoxLayout(scroll_widget)

#         for i in range(10):
#             video_frame = QFrame()
#             video_frame.setStyleSheet("background: white; border-radius: 10px; margin: 10px; padding: 10px;")
#             video_layout = QVBoxLayout(video_frame)

#             thumbnail = QLabel()
#             thumbnail.setPixmap(QPixmap("thumbnail.jpg").scaled(120, 90, Qt.KeepAspectRatio))
#             video_layout.addWidget(thumbnail)

#             title = QLabel(f"Video Title {i+1}")
#             title.setStyleSheet("font-size: 16px; font-weight: bold;")
#             video_layout.addWidget(title)

#             channel = QLabel("Channel Name")
#             channel.setStyleSheet("font-size: 14px; color: gray;")
#             video_layout.addWidget(channel)

#             scroll_layout.addWidget(video_frame)

#         scroll_area.setWidget(scroll_widget)
#         main_layout.addWidget(scroll_area)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = YouTubeLikeUI()
#     window.show()
#     sys.exit(app.exec())










# from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QToolBar, QFileDialog
# from PySide6.QtGui import QIcon, QColor, QPalette, QAction
# from PySide6.QtCore import Qt

# class ExcelLikeUI(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Excel-like UI")
#         self.setGeometry(100, 100, 800, 600)

#         # Set gradient background
#         palette = self.palette()
#         gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1e3c72, stop:1 #2a5298);"
#         palette.setColor(QPalette.Window, QColor(gradient))
#         self.setPalette(palette)

#         # Central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)

#         # Toolbar
#         toolbar = QToolBar()
#         self.addToolBar(toolbar)

#         new_action = QAction(QIcon("icons/new.png"), "New", self)
#         open_action = QAction(QIcon("icons/open.png"), "Open", self)
#         save_action = QAction(QIcon("icons/save.png"), "Save", self)

#         toolbar.addAction(new_action)
#         toolbar.addAction(open_action)
#         toolbar.addAction(save_action)

#         new_action.triggered.connect(self.new_file)
#         open_action.triggered.connect(self.open_file)
#         save_action.triggered.connect(self.save_file)

#         # Table widget
#         self.table = QTableWidget()
#         self.table.setRowCount(100)
#         self.table.setColumnCount(26)
#         self.table.setHorizontalHeaderLabels([chr(i) for i in range(65, 91)])
#         self.table.setVerticalHeaderLabels([str(i) for i in range(1, 101)])

#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

#         layout.addWidget(self.table)

#     def new_file(self):
#         self.table.clearContents()

#     def open_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)")
#         if file_name:
#             with open(file_name, 'r') as file:
#                 data = file.readlines()
#                 self.table.setRowCount(len(data))
#                 for row, line in enumerate(data):
#                     items = line.strip().split(',')
#                     for col, item in enumerate(items):
#                         self.table.setItem(row, col, QTableWidgetItem(item))

#     def save_file(self):
#         file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv);;All Files (*)")
#         if file_name:
#             with open(file_name, 'w') as file:
#                 for row in range(self.table.rowCount()):
#                     row_data = []
#                     for col in range(self.table.columnCount()):
#                         item = self.table.item(row, col)
#                         if item:
#                             row_data.append(item.text())
#                         else:
#                             row_data.append("")
#                     file.write(",".join(row_data) + "\n")

# if __name__ == "__main__":
#     app = QApplication([])
#     window = ExcelLikeUI()
#     window.show()
#     app.exec()








# import matplotlib.pyplot as plt
# import numpy as np

# # Create a figure and a set of subplots
# fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# # Generate some data
# x = np.linspace(0, 10, 100)
# y = np.sin(x)

# # Plot the data on the first subplot
# axs[0, 0].plot(x, y, color='blue', linewidth=2)
# axs[0, 0].set_title('Sine Wave')

# # Plot a histogram on the second subplot
# axs[0, 1].hist(np.random.randn(100), bins=20, color='green', alpha=0.5)
# axs[0, 1].set_title('Histogram')

# # Plot a scatter plot on the third subplot
# axs[1, 0].scatter(x, y, color='red', s=50)
# axs[1, 0].set_title('Scatter Plot')

# # Plot a bar chart on the fourth subplot
# axs[1, 1].bar(x, y, color='purple', width=0.5)
# axs[1, 1].set_title('Bar Chart')

# # Set the overall title of the figure
# fig.suptitle('Beautiful Visualization with Matplotlib')

# # Show the figure
# plt.show()


















# import sys
# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QScrollArea, QGridLayout, QGraphicsOpacityEffect
# from PySide6.QtGui import QIcon, QPixmap, QFont
# from PySide6.QtCore import Qt, QTimer, QPropertyAnimation

# # Sample Data
# sample_videos = [
#     {"title": "Video 1", "channel": "Channel A", "views": "1M views", "date": "1 week ago"},
#     {"title": "Video 2", "channel": "Channel B", "views": "500k views", "date": "2 days ago"},
#     {"title": "Video 3", "channel": "Channel C", "views": "2M views", "date": "3 months ago"},
#     {"title": "Video 4", "channel": "Channel D", "views": "3M views", "date": "1 year ago"},
#     {"title": "Video 5", "channel": "Channel E", "views": "4M views", "date": "6 months ago"},
#     {"title": "Video 6", "channel": "Channel F", "views": "5M views", "date": "1 month ago"},
# ]

# class ThumbnailWidget(QWidget):
#     def __init__(self, title, channel, views, date):
#         super().__init__()
#         self.initUI(title, channel, views, date)

#     def initUI(self, title, channel, views, date):
#         layout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(5)

#         thumbnail = QLabel()
#         thumbnail.setPixmap(QPixmap("thumbnail.png").scaled(200, 112, Qt.KeepAspectRatioByExpanding))
#         thumbnail.setAlignment(Qt.AlignCenter)
#         layout.addWidget(thumbnail)

#         title_label = QLabel(title)
#         title_label.setFont(QFont("Arial", 10, QFont.Bold))
#         title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#         layout.addWidget(title_label)

#         channel_label = QLabel(channel)
#         channel_label.setFont(QFont("Arial", 9))
#         channel_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#         layout.addWidget(channel_label)

#         views_date_label = QLabel(f"{views} • {date}")
#         views_date_label.setFont(QFont("Arial", 8))
#         views_date_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#         layout.addWidget(views_date_label)

#         self.setLayout(layout)

#         # Hover effect
#         self.effect = QGraphicsOpacityEffect(opacity=1)
#         self.setGraphicsEffect(self.effect)
#         self.animation = QPropertyAnimation(self.effect, b"opacity")
#         self.animation.setDuration(200)
#         self.animation.setStartValue(1)
#         self.animation.setEndValue(0.7)
#         self.setMouseTracking(True)

#     def enterEvent(self, event):
#         self.animation.setDirection(QPropertyAnimation.Forward)
#         self.animation.start()

#     def leaveEvent(self, event):
#         self.animation.setDirection(QPropertyAnimation.Backward)
#         self.animation.start()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("YouTube-like Desktop App")
#         self.setGeometry(100, 100, 1200, 800)
#         self.setStyleSheet("""
#             QMainWindow {
#                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #FF0000, stop:1 #282828);
#                 color: white;
#             }
#             QPushButton, QLabel, QLineEdit {
#                 background-color: transparent;
#                 color: white;
#             }
#             QPushButton:hover, QLabel:hover, QLineEdit:hover {
#                 color: #FF0000;
#             }
#             QScrollBar:vertical {
#                 width: 12px;
#             }
#             QScrollBar::handle:vertical {
#                 background: #555;
#                 border-radius: 6px;
#             }
#             QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
#                 height: 0px;
#             }
#             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
#                 background: none;
#             }
#             QListWidget {
#                 background: transparent;
#                 border: none;
#             }
#             QListWidget::item:selected {
#                 background: #333;
#             }
#         """)
#         self.initUI()

#     def initUI(self):
#         main_widget = QWidget()
#         main_layout = QHBoxLayout()
#         main_widget.setLayout(main_layout)

#         # Left Sidebar
#         sidebar = QListWidget()
#         sidebar.addItem("Home")
#         sidebar.addItem("Trending")
#         sidebar.addItem("Subscriptions")
#         sidebar.addItem("Library")
#         sidebar.addItem("History")
#         sidebar.addItem("Your Videos")
#         sidebar.addItem("Watch Later")
#         sidebar.addItem("Liked Videos")
#         sidebar.addItem("Subscribed Channels")
#         sidebar.setFont(QFont("Arial", 10, QFont.Bold))
#         sidebar.setFixedWidth(200)
#         sidebar.setStyleSheet("""
#             QListWidget {
#                 background: transparent;
#                 border: none;
#             }
#             QListWidget::item {
#                 padding: 10px;
#             }
#             QListWidget::item:hover {
#                 background: #333;
#             }
#             QListWidget::item:selected {
#                 background: #FF0000;
#             }
#         """)

#         main_layout.addWidget(sidebar)

#         # Main Content Area
#         content_area = QWidget()
#         content_layout = QVBoxLayout()
#         content_area.setLayout(content_layout)

#         # Navigation Bar
#         nav_bar = QWidget()
#         nav_layout = QHBoxLayout()
#         nav_layout.setContentsMargins(10, 10, 10, 10)
#         nav_layout.setSpacing(20)

#         youtube_logo = QLabel()
#         youtube_logo.setPixmap(QPixmap("youtube_logo.png").scaled(90, 30, Qt.KeepAspectRatio))
#         nav_layout.addWidget(youtube_logo)

#         search_bar = QLineEdit()
#         search_bar.setPlaceholderText("Search")
#         search_bar.setFixedWidth(400)
#         search_icon = QPushButton(QIcon("search_icon.png"), "")
#         search_icon.setFixedSize(30, 30)
#         search_layout = QHBoxLayout()
#         search_layout.addWidget(search_bar)
#         search_layout.addWidget(search_icon)
#         search_widget = QWidget()
#         search_widget.setLayout(search_layout)
#         nav_layout.addWidget(search_widget)

#         user_profile = QPushButton(QIcon("profile_icon.png"), "")
#         user_profile.setFixedSize(30, 30)
#         nav_layout.addWidget(user_profile)

#         upload_video = QPushButton("UPLOAD")
#         upload_video.setFixedSize(100, 30)
#         upload_video.setStyleSheet("""
#             QPushButton {
#                 background-color: #FF0000;
#                 border: none;
#                 border-radius: 5px;
#             }
#             QPushButton:hover {
#                 background-color: #CC0000;
#             }
#         """)
#         nav_layout.addWidget(upload_video)

#         notifications_bell = QPushButton(QIcon("bell_icon.png"), "")
#         notifications_bell.setFixedSize(30, 30)
#         nav_layout.addWidget(notifications_bell)

#         nav_bar.setLayout(nav_layout)
#         content_layout.addWidget(nav_bar)

#         # Video Grid Layout
#         video_grid = QWidget()
#         video_grid_layout = QGridLayout()
#         video_grid.setLayout(video_grid_layout)

#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_area.setWidget(video_grid)
#         content_layout.addWidget(scroll_area)

#         # Adding sample videos
#         row = 0
#         col = 0
#         for video in sample_videos:
#             thumbnail = ThumbnailWidget(video["title"], video["channel"], video["views"], video["date"])
#             video_grid_layout.addWidget(thumbnail, row, col)
#             col += 1
#             if col == 3:
#                 col = 0
#                 row += 1

#         main_layout.addWidget(content_area)
#         self.setCentralWidget(main_widget)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
























