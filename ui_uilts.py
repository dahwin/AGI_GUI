from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QSizePolicy, QApplication,
                               QMainWindow, QSplitter, QMessageBox)
from PySide6.QtGui import (QFont, QIcon, QPainter, QColor, QPen, QBrush, 
                           QLinearGradient, QPainterPath, QTextCursor)
from PySide6.QtCore import (Qt, QSize, QUrl, QPropertyAnimation, QEasingCurve, 
                            QRectF, Property, QPointF,QTimer)
import math
# from PySide6.QtWebEngineWidgets import QWebEngineView
STYLE_SHEET = """
QWidget {
    background-color: transparent;
    color: white;
    font-family: Arial, sans-serif;
}

QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #000000, stop:1 #2E0619);
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
                                stop:0 #000000, stop:1 #2E0619);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

#send_btn:hover, #engine_btn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1c1c1c, stop:1 #2E0619);
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
                                stop:0 #000000, stop:1 #2E0619);
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1c1c1c, stop:1 #026390);
}

QRadioButton, QCheckBox {
    color: white;
}
"""

color_0 = "B2B5D3"
color_1 = "1c1c1c"
color = "219FD5"



class CleanLoadingAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)  # Maintain thin, elegant height
        
        self.colors = [
            QColor("#4285F4"),  # Blue
            QColor("#4285F4"),  # Blue
            QColor("#4285F4"),  # Blue
            QColor("#4285F4"),  # Blue
        ]
        self.dots = []
        self.phase = 0
        self.dot_count = 50  # Increased number of dots for longer area
        
        # Custom lengths for each dot (you can modify these values)
        # self.dot_lengths = [2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2]
        self.dot_lengths = [2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2,2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2,2,2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2,2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2,2]
        # Initialize animation dots with proper spacing and custom lengths
        
        # Initialize animation dots with proper spacing and custom lengths
        total_length = sum(self.dot_lengths)
        current_position = 0
        for i in range(self.dot_count):
            dot = {
                'position': current_position,
                'color': self.colors[i % len(self.colors)],
                'scale': 0.0,
                'phase_offset': i * (math.pi / (self.dot_count/2)),
                'length': self.dot_lengths[i]
            }
            self.dots.append(dot)
            current_position += (self.width() * self.dot_lengths[i] / total_length)
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(16)  # 60 FPS
        
        # Subtle background gradient
        self.gradient = QLinearGradient(0, 0, self.width(), 0)
        self.gradient.setColorAt(0, QColor(248, 249, 250, 30))
        self.gradient.setColorAt(0.5, QColor(245, 246, 247, 40))
        self.gradient.setColorAt(1, QColor(241, 243, 244, 30))

    def updateAnimation(self):
        self.phase += 0.3  # Slightly slower base speed for smoother appearance
        
        total_length = sum(self.dot_lengths)
        current_position = 0
        for i, dot in enumerate(self.dots):
            # Calculate smooth scaling effect
            dot['scale'] = (math.sin(self.phase + dot['phase_offset']) + 1) / 2
            
            # Update position with smooth movement (left to right only)
            dot['position'] = (self.phase * 50 + current_position) % self.width()
            current_position += (self.width() * self.dot_lengths[i] / total_length)
        
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw subtle background
        painter.setBrush(QBrush(self.gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 2, 2)
        
        # Draw dots with clean fade effect
        for dot in self.dots:
            # Calculate size based on scale and length
            size = 3 + (dot['scale'] * 3)  # Base size
            length = dot['length'] * 2  # Adjust this multiplier to control the overall length effect
            
            # Create clean gradient for each dot
            center = QPointF(dot['position'], self.height() / 2)
            
            # Draw glow effect first
            glow_size = size * length
            glow_gradient = QLinearGradient(
                dot['position'] - glow_size, self.height() / 2,
                dot['position'] + glow_size, self.height() / 2
            )
            
            glow_color = QColor(dot['color'])
            glow_color.setAlpha(int(30 * dot['scale']))
            glow_gradient.setColorAt(0, Qt.transparent)
            glow_gradient.setColorAt(0.5, glow_color)
            glow_gradient.setColorAt(1, Qt.transparent)
            
            painter.setBrush(QBrush(glow_gradient))
            painter.drawRoundedRect(
                dot['position'] - glow_size,
                self.height() / 2 - size * 1.5,
                glow_size * 2,
                size * 3,
                size,
                size
            )
            
            # Draw main dot (elongated)
            painter.setPen(Qt.NoPen)
            color = QColor(dot['color'])
            color.setAlpha(int(255 * (0.4 + 0.6 * dot['scale'])))
            painter.setBrush(color)
            painter.drawRoundedRect(
                dot['position'] - size * length / 2,
                self.height() / 2 - size,
                size * length,
                size * 2,
                size,
                size
            )
            
            # Draw highlight
            highlight_color = QColor(dot['color'])
            highlight_color.setAlpha(int(100 * dot['scale']))
            painter.setBrush(highlight_color)
            highlight_size = size * 0.4
            painter.drawEllipse(
                QPointF(dot['position'] - size * length / 4, self.height() / 2 - size * 0.2),
                highlight_size,
                highlight_size
            )
    def startAnimation(self):
        self.show()
        self.timer.start()
    
    def stopAnimation(self):
        self.timer.stop()
        self.hide()



# class MultiLineUploadAnimation(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedHeight(20)
#         self.lines = []
#         self.colors = [
#             QColor("#2196F3"),  # Bright Blue
#             QColor("#4CAF50"),  # Vibrant Green
#             QColor("#F44336"),  # Material Red
#             QColor("#1976D2"),  # Deep Blue
#         ]
        
#         # Initialize animation lines
#         for i in range(4):
#             line = {
#                 'progress': -100 + (i * -25),  # Stagger start positions
#                 'color': self.colors[i],
#                 'opacity': QColor(self.colors[i].red(), 
#                                 self.colors[i].green(),
#                                 self.colors[i].blue(), 
#                                 180)  # Add some transparency
#             }
#             self.lines.append(line)
        
#         # Animation timer
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.updateAnimation)
#         self.animation_speed = 5
        
#         # Gradient background
#         self.gradient = QLinearGradient(0, 0, self.width(), 0)
#         self.gradient.setColorAt(0, QColor(52, 73, 94, 50))
#         self.gradient.setColorAt(1, QColor(44, 62, 80, 50))
        
#     def startAnimation(self):
#         self.show()
#         self.timer.start(30)  # Update every 30ms
        
#     def stopAnimation(self):
#         self.timer.stop()
#         self.hide()
        
#     def updateAnimation(self):
#         for line in self.lines:
#             line['progress'] += self.animation_speed
#             if line['progress'] > self.width() + 100:  # Reset position
#                 line['progress'] = -100
#         self.update()
        
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
        
#         # Draw background
#         painter.setBrush(QBrush(self.gradient))
#         painter.setPen(Qt.NoPen)
#         painter.drawRoundedRect(self.rect(), 10, 10)
        
#         # Draw animated lines
#         for line in self.lines:
#             # Create line gradient
#             line_gradient = QLinearGradient(
#                 line['progress'] - 50, 0,
#                 line['progress'] + 50, 0
#             )
            
#             # Gradient colors with fade effect
#             line_gradient.setColorAt(0, QColor(0, 0, 0, 0))
#             line_gradient.setColorAt(0.2, line['opacity'])
#             line_gradient.setColorAt(0.5, line['color'])
#             line_gradient.setColorAt(0.8, line['opacity'])
#             line_gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
#             # Draw line
#             painter.setPen(QPen(QBrush(line_gradient), 3, Qt.SolidLine, Qt.RoundCap))
#             painter.drawLine(
#                 line['progress'] - 50, self.height() / 2,
#                 line['progress'] + 50, self.height() / 2
#             )


class GradientAnimatedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setText(text)
        self.setMinimumHeight(40)
        self._gradient_position = 0.0

        self.gradient_animation = QPropertyAnimation(self, b"gradient_position", self)
        self.gradient_animation.setDuration(3000)  # 3 seconds for one complete cycle
        self.gradient_animation.setStartValue(0.0)
        self.gradient_animation.setEndValue(1.0)
        self.gradient_animation.setLoopCount(-1)  # Infinite loop
        self.gradient_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.gradient_animation.start()

    def setText(self, text):
        super().setText(text)
        self.adjustSize()

    def adjustSize(self):
        # Calculate width based on text length
        text_length = len(self.text())
        base_width = 120  # Width for 6 characters
        base_chars = 6
        
        if text_length <= base_chars:
            new_width = base_width
        else:
            # Linear interpolation
            extra_chars = text_length - base_chars
            extra_width = (base_width / base_chars) * extra_chars
            new_width = base_width + extra_width

        self.setMinimumWidth(int(new_width))

    def gradient_position(self):
        return self._gradient_position

    def set_gradient_position(self, pos):
        self._gradient_position = pos
        self.update()

    gradient_position = Property(float, gradient_position, set_gradient_position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw black rounded rectangle background
        painter.setPen(Qt.NoPen)
        # painter.setBrush(QColor(0, 0, 0))  # Black color
        painter.setBrush(QColor(255, 255, 255))  # White color
        painter.drawRoundedRect(self.rect(), 10, 10)  # 10px corner radius

        # Create gradient
        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), 0))
        
        # Calculate color positions based on animation progress
        pos1 = self._gradient_position
        pos2 = (self._gradient_position + 0.33) % 1.0
        pos3 = (self._gradient_position + 0.67) % 1.0

        gradient.setColorAt(pos1, QColor(255, 0, 0))  # Red
        gradient.setColorAt(pos2, QColor(128, 0, 128))  # Purple
        gradient.setColorAt(pos3, QColor(0, 0, 255))  # Blue

        # Set the gradient as the brush for the text
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QBrush(gradient), 1))

        # Draw text
        painter.setFont(QFont("Arial", 18, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())




# class GradientAnimatedLabel(QWebEngineView):
#     def __init__(self, text, parent=None):
#         super().__init__(parent)
#         self.setMinimumSize(120, 40)
#         self.setMaximumSize(200, 40)  # Set a maximum width
#         self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

#         html_content = f"""
#         <html>
#         <head>
#             <style>
#                 body {{
#                     margin: 0;
#                     padding: 0;
#                     display: flex;
#                     justify-content: center;
#                     align-items: center;
#                     height: 100vh;
#                     background-color: transparent;
#                 }}
#                 .gradient-text {{
#                     font-family: Arial, sans-serif;
#                     font-size: 18px;
#                     font-weight: bold;
#                     background: linear-gradient(to right, red, purple, blue);
#                     background-size: 200% auto;
#                     color: transparent;
#                     -webkit-background-clip: text;
#                     background-clip: text;
#                     animation: shine 3s linear infinite;
#                     display: inline-block;
#                 }}
#                 @keyframes shine {{
#                     to {{
#                         background-position: 200% center;
#                     }}
#                 }}
#             </style>
#         </head>
#         <body>
#             <div class="gradient-text">{text}</div>
#         </body>
#         </html>
#         """
#         self.setHtml(html_content)
#         self.setStyleSheet("background: transparent;")


class ToggleButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._toggle = False
        self._margin = 3
        self._thumb_radius = (self.height() - 2 * self._margin) / 2
        self._thumb_position = self._margin
        self._anim = QPropertyAnimation(self, b"thumb_position", self)
        self._anim.setDuration(200)

    def thumb_position(self):
        return self._thumb_position

    def set_thumb_position(self, pos):
        self._thumb_position = pos
        self.update()

    thumb_position = Property(float, thumb_position, set_thumb_position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track_color = QColor("#4CD964") if self._toggle else QColor("#E9E9EA")
        thumb_color = Qt.white
        text_color = Qt.white if self._toggle else QColor("#9B9B9B")

        # Draw track
        painter.setBrush(track_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        # Draw thumb
        painter.setBrush(thumb_color)
        painter.drawEllipse(QRectF(self._thumb_position, self._margin, self._thumb_radius * 2, self._thumb_radius * 2))

        # Draw text
        painter.setPen(QPen(text_color))
        painter.setFont(QFont("Arial", 8))
        text = "ON" if self._toggle else "OFF"
        text_width = painter.fontMetrics().horizontalAdvance(text)
        painter.drawText(self.width() / 2 - text_width / 2, self.height() / 2 + 5, text)

    def mouseReleaseEvent(self, event):
        self._toggle = not self._toggle
        self._anim.setStartValue(self._thumb_position)
        self._anim.setEndValue(self.width() - 2 * self._margin - self._thumb_radius * 2 if self._toggle else self._margin)
        self._anim.start()

    def is_on(self):
        return self._toggle

class GradientLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumSize(120, 40)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 32, 96))
        gradient.setColorAt(1, QColor(0, 0, 32))

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, self.width()-2, self.height()-2), 10, 10)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 50))
        painter.drawRoundedRect(3, 3, self.width()-2, self.height()-2, 10, 10)

        painter.fillPath(path, QBrush(gradient))

        painter.setPen(QPen(QColor(255, 255, 255, 30), 1))
        painter.drawPath(path)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())