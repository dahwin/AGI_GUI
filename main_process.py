import requests
import mimetypes
import os
import asyncio
import aiohttp
import re
import base64
import json
import pyautogui
import pyperclip
import time
from io import BytesIO
from PIL import Image
from mss import mss
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, 
                           QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, 
                           Qt, QEvent, QThread, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, 
                          QFontDatabase, QIcon, QKeySequence, QLinearGradient, 
                          QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
import httpx
from ui import *

base = "https://agi.queendahyun.site"

class QueenDahyunChatClient:
    def __init__(self, username):
        self.username = username
        self.server_url = base
        self.turn_count = 0
        
    def chat(self, prompt, file_paths=None):
        self.turn_count += 1
        data = {'username': self.username, 'prompt': prompt}
        
        files = []
        if file_paths:
            if isinstance(file_paths, str):
                file_paths = [file_paths]
            
            missing_files = [f for f in file_paths if not os.path.exists(f)]
            if missing_files:
                return "Error: Missing files: " + ", ".join(missing_files)
            
            files = []
            for i, file_path in enumerate(file_paths):
                files.append(('files', (os.path.basename(file_path), open(file_path, 'rb'))))
        
        try:
            response = requests.post(f"{self.server_url}/chat", files=files, data=data, stream=True)
            
            if response.status_code == 200:
                return response
            return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception: {str(e)}"

class UIAutomationWorker(QObject):
    progress = Signal(str)
    finished = Signal()
    
    CAPTURE_INTERVAL = 0.05
    COMPRESSION_QUALITY = 90
    RESIZE_FACTOR = 1.0
    USE_JPEG = True
    
    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt
        self.running = True
        self.capture_count = 0
        self.sent_count = 0
        
        # Load mouse icon if available
        self.mouse_icon = None
        try:
            mouse_icon_path = "mouse_icon.png"
            self.mouse_icon = Image.open(mouse_icon_path).resize((26, 26), Image.Resampling.NEAREST)
        except Exception:
            pass
        
        # Get screen dimensions
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        self.monitor = {"top": 0, "left": 0, "width": rect.width(), "height": rect.height()}
    
    def capture_screenshot(self):
        with mss() as sct:
            sct_img = sct.grab(self.monitor)
            img = Image.frombytes("RGB", (sct_img.width, sct_img.height), sct_img.bgra, "raw", "BGRX")
            
            if self.mouse_icon:
                try:
                    mouse_x_abs, mouse_y_abs = pyautogui.position()
                    icon_pos_x = mouse_x_abs - self.mouse_icon.width // 2
                    icon_pos_y = mouse_y_abs - self.mouse_icon.height // 2
                    
                    if (0 <= icon_pos_x < img.width - self.mouse_icon.width and 
                        0 <= icon_pos_y < img.height - self.mouse_icon.height):
                        img.paste(self.mouse_icon, (icon_pos_x, icon_pos_y), 
                                 self.mouse_icon if self.mouse_icon.mode == 'RGBA' else None)
                except Exception:
                    pass
            return img
    
    def optimize_image(self, img):
        if self.RESIZE_FACTOR < 1.0:
            new_width = int(img.width * self.RESIZE_FACTOR)
            new_height = int(img.height * self.RESIZE_FACTOR)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        img_format = "JPEG" if self.USE_JPEG else "PNG"
        content_type = "image/jpeg" if self.USE_JPEG else "image/png"
        img_byte_arr = BytesIO()
        
        if img_format == "JPEG":
            if img.mode == "RGBA": 
                img = img.convert("RGB")
            img.save(img_byte_arr, format=img_format, quality=self.COMPRESSION_QUALITY, optimize=True)
        else:
            img.save(img_byte_arr, format=img_format, optimize=True)
            
        img_byte_arr.seek(0)
        return img_byte_arr, content_type

    def mouse_and_keyboard_action(self, data_str):
        x_match = re.search(r'x=(\d+)', data_str)
        y_match = re.search(r'y=(\d+)', data_str)
        action_match = re.search(r'action=([\w-]+)', data_str)
        
        if x_match and y_match and action_match:
            x = int(x_match.group(1))
            y = int(y_match.group(1))
            action = action_match.group(1).lower()
            
            if action == "left-click":
                pyautogui.click(x, y)
            elif action == "right-click":
                pyautogui.rightClick(x, y)
            elif action == "double-click":
                pyautogui.doubleClick(x, y)
            elif action == "move":
                pyautogui.moveTo(x, y)
            elif action == "enter":
                pyautogui.press('enter')
            time.sleep(0.5)
    
    def type_text(self, text):
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    
    async def run_automation(self):
        # Get improved prompt
        try:
            img = self.capture_screenshot()
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            payload = {"image_base64": image_base64, "prompt": self.prompt}
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{base}/get_better", json=payload) as response:
                    result = await response.json()
                    better_prompt = result["better_command"]
        except Exception as e:
            self.progress.emit(f"Error getting better prompt: {str(e)}")
            better_prompt = self.prompt
        
        async with aiohttp.ClientSession() as session:
            while self.running:
                try:
                    img = self.capture_screenshot()
                    img_bytes, content_type = self.optimize_image(img)
                    
                    form = aiohttp.FormData()
                    form.add_field('file', img_bytes, 
                                  filename='s.jpg' if self.USE_JPEG else 's.png', 
                                  content_type=content_type)
                    form.add_field('username', "dahwin@queendahyun.site")
                    form.add_field('prompt', better_prompt)
                    
                    async with session.post(f"{base}/action_gui/", data=form, 
                                          timeout=aiohttp.ClientTimeout(total=190)) as response:
                        metadata_bytes = await response.content.readline()
                        if not metadata_bytes:
                            continue
                            
                        try:
                            metadata = json.loads(metadata_bytes.decode('utf-8').strip())
                            
                            if metadata.get("Done", False):
                                self.running = False
                            
                            if "instruction_data" in metadata:
                                self.mouse_and_keyboard_action(metadata["instruction_data"])
                            
                            if metadata.get("streaming_ai_response"):
                                async for line_bytes in response.content:
                                    if line_bytes and self.running:
                                        decoded = line_bytes.decode('utf-8').rstrip('\n')
                                        self.type_text(decoded)
                                        self.progress.emit(decoded)
                        except Exception as e:
                            self.progress.emit(f"Error processing response: {str(e)}")
                            
                    await asyncio.sleep(self.CAPTURE_INTERVAL)
                except Exception as e:
                    self.progress.emit(f"Automation error: {str(e)}")
                    await asyncio.sleep(1)
    
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run_automation())
        loop.close()
        self.finished.emit()
    
    def stop(self):
        self.running = False

class ChatThread(QThread):
    message_received = Signal(str)
    finished = Signal()
    error_occurred = Signal(str)
    
    def __init__(self, username, prompt, file_paths=None):
        super().__init__()
        self.username = username
        self.prompt = prompt
        self.file_paths = file_paths if file_paths else []
        self._running = True
        
    def run(self):
        client = QueenDahyunChatClient(self.username)
        response = client.chat(self.prompt, self.file_paths)
        
        if isinstance(response, str):
            self.error_occurred.emit(response)
            self.finished.emit()
            return
            
        try:
            for chunk in response.iter_content(chunk_size=1024):
                if not self._running:
                    break
                    
                if chunk:
                    decoded = chunk.decode('utf-8', errors='ignore')
                    self.message_received.emit(decoded)
        except Exception as e:
            self.error_occurred.emit(f"Error during streaming: {str(e)}")
        finally:
            self.finished.emit()
    
    def stop(self):
        self._running = False

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect signals
        self.ui.send_btn.clicked.connect(self.send_user_message)
        self.ui.force_stop_button.clicked.connect(self.force_stop_action)
        self.ui.input_textEdit.installEventFilter(self)
        self.ui.file_btn.clicked.connect(self.select_files)
        
        # Initialize state
        self.uploaded_file_paths = []
        self.chat_thread = None
        self.ui_automation_worker = None
        self.ui_automation_thread = None
        self.active_animations = 0
        
        # Status label for uploads
        self.upload_status_label = QLabel("")
        self.ui.main_content.layout().addWidget(self.upload_status_label)

    def select_files(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.uploaded_file_paths = selected_files
            self.update_upload_status()
            self.display_uploaded_files(selected_files)

    def update_upload_status(self):
        count = len(self.uploaded_file_paths)
        self.upload_status_label.setText(f"{count} file{'s' if count != 1 else ''} ready for upload")

    def display_uploaded_files(self, files):
        text_browser = self.ui.text_browser
        if not text_browser:
            return
            
        user_image_path = "user.png"
        if not os.path.exists(user_image_path):
            user_image_path = ":/images/user.png"  # Fallback to resource if available
            
        pixmap = QPixmap(user_image_path)
        if pixmap.isNull():
            pixmap = QPixmap(40, 40)
            pixmap.fill(Qt.blue)
        
        scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_path = "temp_user_image.png"
        scaled_pixmap.save(temp_path, "PNG")
        
        upload_message = f"""
        <table style='margin-bottom: 20px; width: 100%;'>
            <tr>
                <td style='vertical-align: top; width: 40px;'>
                    <img src='{temp_path}' width='40' height='40' style='border-radius: 20px;'>
                </td>
                <td style='vertical-align: top; padding-left: 10px;'>
                    <b>User uploaded files:</b><br>
                    <div style='margin-top: 5px;'>
        """
        
        for file in files:
            file_name = os.path.basename(file)
            upload_message += f"<span style='font-size: 12pt;'>{file_name}</span><br>"
            
        upload_message += "</div></td></tr></table>"
        text_browser.append(upload_message)
        text_browser.verticalScrollBar().setValue(text_browser.verticalScrollBar().maximum())

    def send_user_message(self):
        user_input = self.ui.input_textEdit.toPlainText().strip()
        if not user_input:
            return
            
        self.display_user_message(user_input)
        self.set_input_state(False)
        self.start_processing_animation()

        if self.ui.action_toggle.is_on():
            self.start_ui_automation(user_input)
        else:
            self.start_chat(user_input)
            
        self.ui.input_textEdit.clear()
        self.uploaded_file_paths = []
        self.upload_status_label.clear()

    def start_ui_automation(self, prompt):
        self.ui_automation_worker = UIAutomationWorker(prompt)
        self.ui_automation_worker.progress.connect(self.display_automation_progress)
        self.ui_automation_worker.finished.connect(self.handle_automation_complete)
        
        self.ui_automation_thread = QThread()
        self.ui_automation_worker.moveToThread(self.ui_automation_thread)
        self.ui_automation_thread.started.connect(self.ui_automation_worker.run)
        self.ui_automation_thread.start()
        
        self.ui.force_stop_button.show()

    def start_chat(self, prompt):
        self.chat_thread = ChatThread("dahwin@queendahyun.site", prompt, self.uploaded_file_paths)
        self.chat_thread.message_received.connect(self.display_ai_response)
        self.chat_thread.finished.connect(self.handle_chat_complete)
        self.chat_thread.error_occurred.connect(self.display_error)
        self.chat_thread.start()

    def display_automation_progress(self, message):
        self.ui.text_browser.append(f"<b>Automation:</b> {message}")
        self.ui.text_browser.verticalScrollBar().setValue(
            self.ui.text_browser.verticalScrollBar().maximum()
        )

    def display_user_message(self, message):
        text_browser = self.ui.text_browser
        if not text_browser:
            return
            
        user_image_path = "user.png"
        if not os.path.exists(user_image_path):
            user_image_path = ":/images/user.png"
            
        pixmap = QPixmap(user_image_path)
        if pixmap.isNull():
            pixmap = QPixmap(40, 40)
            pixmap.fill(Qt.blue)
            
        scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        temp_path = "temp_user_image.png"
        scaled_pixmap.save(temp_path, "PNG")
        
        user_message = f"""
        <table style='margin-bottom: 20px; width: 100%;'>
            <tr>
                <td style='vertical-align: top; width: 40px;'>
                    <img src='{temp_path}' width='40' height='40' style='border-radius: 20px;'>
                </td>
                <td style='vertical-align: top; padding-left: 10px;'>
                    <b>User:</b><br>
                    <div style='margin-top: 5px;'>
                        <span style='font-size: 14pt;'>{message}</span>
                    </div>
                </td>
            </tr>
        </table>"""
        
        text_browser.append(user_message)
        text_browser.verticalScrollBar().setValue(text_browser.verticalScrollBar().maximum())

    def display_ai_response(self, response_chunk):
        text_browser = self.ui.text_browser
        if not text_browser:
            return
            
        cursor = text_browser.textCursor()
        cursor.movePosition(QTextCursor.End)
        text_browser.setTextCursor(cursor)
        text_browser.insertPlainText(response_chunk)
        text_browser.ensureCursorVisible()

    def display_error(self, error):
        self.ui.text_browser.append(f"<span style='color: red;'>Error: {error}</span>")
        self.handle_chat_complete()

    def handle_automation_complete(self):
        self.set_input_state(True)
        self.ui.force_stop_button.hide()
        self.ui_automation_worker = None
        self.ui_automation_thread = None
        self.stop_processing_animation()

    def handle_chat_complete(self):
        self.set_input_state(True)
        self.stop_processing_animation()

    def force_stop_action(self):
        if self.chat_thread and self.chat_thread.isRunning():
            self.chat_thread.stop()
            self.chat_thread.wait()
            
        if self.ui_automation_worker:
            self.ui_automation_worker.stop()
            
        self.set_input_state(True)
        self.ui.force_stop_button.hide()
        self.stop_processing_animation()

    def set_input_state(self, enabled):
        self.ui.input_textEdit.setEnabled(enabled)
        self.ui.send_btn.setEnabled(enabled)
        self.ui.file_btn.setEnabled(enabled)
        self.ui.model_combo.setEnabled(enabled)
        self.ui.action_toggle.setEnabled(enabled)

    def start_processing_animation(self):
        self.active_animations += 1
        self.ui.upload_animation.show()
        self.ui.upload_animation.timer.start()

    def stop_processing_animation(self):
        self.active_animations = 0
        self.ui.upload_animation.stopAnimation()

    def eventFilter(self, obj, event):
        if obj is self.ui.input_textEdit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                if event.modifiers() & Qt.ShiftModifier:
                    cursor = self.ui.input_textEdit.textCursor()
                    cursor.insertText('\n')
                    return True
                else:
                    self.send_user_message()
                    return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        self.force_stop_action()
        super().closeEvent(event)