import requests
import mimetypes
import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                           QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl,
                           Qt, QEvent, QThread, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                          QFontDatabase, QIcon, QKeySequence, QLinearGradient,
                          QPalette, QPainter, QPixmap, QRadialGradient, QTextCursor) # Added QTextCursor
from PySide6.QtWidgets import *
import httpx # Keep for potential future use or if any part still needs it, though primary new APIs use requests/aiohttp
import asyncio
from ui import * # Assuming your ui.py (Ui_MainWindow, etc.) is correctly set up
import re
# import requests # Already imported

# --- New UI Automation Imports ---
import aiohttp
from io import BytesIO
import time
from PIL import Image
from mss import mss
import pyautogui
# import nest_asyncio # Generally not needed when QThread manages its own asyncio loop
import json
import pyperclip
import base64
# from PIL import Image # Already imported
# import io # Already imported as BytesIO

# --- Global Configuration ---
base = "https://agi.queendahyun.site"
USER_NAME = "dahwin@queendahyun.site" # For UI Automation and Multi-turn Chat

# --- UI Automation Specific Globals & Setup ---
pyautogui.PAUSE = 0.01
CAPTURE_INTERVAL = 0.05  # Seconds
COMPRESSION_QUALITY = 75 # Adjusted for potentially faster processing
RESIZE_FACTOR = 0.75     # Adjusted for potentially faster processing
USE_JPEG = True

# UI Automation state (will be managed by the worker)
# running_automation = True # This will be an instance variable in the worker
# capture_count = 0
# sent_count = 0

mouse_icon = None
icon_width, icon_height = 0, 0
try:
    # Try to load from common locations or specify an absolute path if needed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mouse_icon_path = os.path.join(script_dir, "mouse_icon.png")
    if not os.path.exists(mouse_icon_path) and 'a_p' in globals() and os.path.exists(os.path.join(a_p, "mouse_icon.png")): # Fallback if a_p is defined
        mouse_icon_path = os.path.join(a_p, "mouse_icon.png")
    
    if os.path.exists(mouse_icon_path):
        mouse_icon = Image.open(mouse_icon_path).convert("RGBA").resize((26, 26), Image.Resampling.NEAREST)
        icon_width, icon_height = mouse_icon.size
        print(f"Mouse icon '{mouse_icon_path}' loaded successfully.")
    else:
        print(f"Warning: Mouse icon 'mouse_icon.png' not found. Searched in: {script_dir}. Continuing without it.")
except Exception as e:
    print(f"Warning: Error loading mouse icon: {e}. Continuing without it.")

# Assuming monitor detection or fixed size. For dynamic, you might need screeninfo or similar
try:
    # Get primary monitor size using pyautogui, mss might also have ways
    screen_width, screen_height = pyautogui.size()
    monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
    print(f"Monitor size detected: {screen_width}x{screen_height}")
except Exception as e:
    print(f"Could not detect screen size using PyAutoGUI, defaulting. Error: {e}")
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080} # Default

# --- UI Automation Helper Functions ---
def capture_screenshot_automation(): # Renamed to avoid conflict if any other capture_screenshot exists
    with mss() as sct:
        sct_img = sct.grab(monitor)
        # Create PIL image, ensuring correct channel order if needed (mss usually provides RGB)
        img = Image.frombytes("RGB", (sct_img.width, sct_img.height), sct_img.rgb, "raw", "BGR")

        if mouse_icon:
            try:
                mouse_x_abs, mouse_y_abs = pyautogui.position()
                # Ensure mouse coordinates are within the captured monitor area
                mouse_x_relative = mouse_x_abs - monitor["left"]
                mouse_y_relative = mouse_y_abs - monitor["top"]

                icon_pos_x = mouse_x_relative - icon_width // 2
                icon_pos_y = mouse_y_relative - icon_height // 2

                # Check if the icon position is valid before pasting
                if (0 <= icon_pos_x < img.width - icon_width and
                        0 <= icon_pos_y < img.height - icon_height):
                    img.paste(mouse_icon, (icon_pos_x, icon_pos_y), mouse_icon) # Use mouse_icon directly as mask for RGBA
            except Exception as e:
                print(f"Error pasting mouse icon: {e}")
        return img

def optimize_image_automation(img: Image.Image):
    if RESIZE_FACTOR < 1.0:
        new_width = int(img.width * RESIZE_FACTOR)
        new_height = int(img.height * RESIZE_FACTOR)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img_format = "JPEG" if USE_JPEG else "PNG"
    content_type = "image/jpeg" if USE_JPEG else "image/png"
    img_byte_arr = BytesIO()

    if img_format == "JPEG":
        if img.mode == "RGBA": # JPEG doesn't support alpha
            img = img.convert("RGB")
        img.save(img_byte_arr, format=img_format, quality=COMPRESSION_QUALITY, optimize=True)
    else: # PNG
        img.save(img_byte_arr, format=img_format, optimize=True, compress_level=6) # compress_level for PNG

    img_byte_arr.seek(0)
    return img_byte_arr, content_type

def type_text_automation(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    # pyautogui.typewrite(text) # typewrite can be slow or miss characters

def mouse_and_keyboard_action_automation(data_str: str):
    x_match = re.search(r'x=(\d+)', data_str)
    y_match = re.search(r'y=(\d+)', data_str)
    action_match = re.search(r'action=([\w-]+)', data_str)

    if x_match and y_match and action_match:
        x = int(x_match.group(1))
        y = int(y_match.group(1))
        action = action_match.group(1).lower()

        print(f"Executing Action: {action}, Position: x={x}, y={y}")
        if action == "left-click":
            pyautogui.click(x, y)
        elif action == "right-click":
            pyautogui.rightClick(x, y)
        elif action == "double-click":
            pyautogui.doubleClick(x, y)
        elif action == "move":
            pyautogui.moveTo(x, y)
        elif action == "enter": # Assuming this means press Enter key, not related to x,y
            pyautogui.press('enter')
        else:
            print(f"Unknown action: {action}")
        time.sleep(0.5) # Small delay after action
        return f"Action: {action} at ({x},{y})"
    else:
        print("Could not parse coordinates or action from input:", data_str)
        return f"Parse Error: {data_str}"


def remove_user_session_automation(username):
    url = f"{base}/remove-user-session"
    data = {"username": username}
    try:
        response = requests.post(url, data=data)
        print(f"Remove session response for {username}: {response.status_code}, {response.text}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error removing session for {username}: {e}")
        return {"success": False, "error": str(e)}

# --- QueenDahyunChatClient Class ---
class QueenDahyunChatClient:
    def __init__(self, username, server_url=base):
        self.username = username
        self.server_url = server_url
        self.turn_count = 0 # Internal tracking, server manages session turns

    def chat(self, prompt, file_paths=None, progress_callback=None, chunk_callback=None, finished_callback=None):
        self.turn_count += 1
        # print(f"\nTURN {self.turn_count} - User: {self.username}")

        data = {'username': self.username, 'prompt': prompt}
        files_to_upload = []
        file_handles = []

        try:
            if file_paths:
                if isinstance(file_paths, str): file_paths = [file_paths]
                
                valid_file_paths = []
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        valid_file_paths.append(file_path)
                    else:
                        if progress_callback: progress_callback(f"Error: File not found - {file_path}")
                
                if not valid_file_paths: # If all files were missing
                    if progress_callback: progress_callback("No valid files to upload.")
                    # Potentially call finished_callback with an error or handle upstream
                    if finished_callback: finished_callback()
                    return

                # print(f"📎 Uploading {len(valid_file_paths)} file(s): {', '.join([os.path.basename(f) for f in valid_file_paths])}")
                if progress_callback: progress_callback(f"Preparing to send {len(valid_file_paths)} file(s)...")

                for i, file_path in enumerate(valid_file_paths):
                    f = open(file_path, 'rb')
                    file_handles.append(f)
                    # Use mimetypes to guess content type, fallback to octet-stream
                    content_type, _ = mimetypes.guess_type(file_path)
                    if content_type is None:
                        content_type = 'application/octet-stream'
                    files_to_upload.append((f'file{i}', (os.path.basename(file_path), f, content_type)))
                
                response = requests.post(f"{self.server_url}/chat", files=files_to_upload, data=data, stream=True, timeout=300)
            else:
                # print("💬 Sending text-only prompt...")
                if progress_callback: progress_callback("Sending text-only prompt...")
                response = requests.post(f"{self.server_url}/chat", data=data, stream=True, timeout=300)

            if response.status_code == 200:
                # print(f"🤖 AI Response:")
                for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                    if chunk and chunk_callback:
                        chunk_callback(chunk)
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                # print(f"❌ {error_msg}")
                if chunk_callback: chunk_callback(f"\nSERVER ERROR: {error_msg}\n")
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Network Error during chat: {str(e)}"
            # print(f"❌ {error_msg}")
            if chunk_callback: chunk_callback(f"\nNETWORK ERROR: {error_msg}\n")
        except Exception as e:
            error_msg = f"An unexpected error occurred during chat: {str(e)}"
            # print(f"❌ {error_msg}")
            if chunk_callback: chunk_callback(f"\nUNEXPECTED ERROR: {error_msg}\n")
        finally:
            for f_handle in file_handles:
                f_handle.close()
            if finished_callback:
                finished_callback()

    def clear_session(self):
        try:
            response = requests.post(f"{self.server_url}/clear-session", data={"username": self.username})
            if response.status_code == 200:
                print(f"✅ Session cleared for {self.username}")
                self.turn_count = 0
                return True, "Session cleared"
            else:
                msg = f"❌ Error clearing session: {response.status_code} - {response.text}"
                print(msg)
                return False, msg
        except Exception as e:
            msg = f"❌ Exception clearing session: {e}"
            print(msg)
            return False, msg


# --- Worker for QueenDahyunChatClient ---
class ChatServiceWorker(QObject):
    message_received = Signal(str)
    stream_finished = Signal()
    status_update = Signal(str) # For upload status etc.

    def __init__(self, username):
        super().__init__()
        self.client = QueenDahyunChatClient(username)
        self._running = True

    def process_chat(self, prompt, file_paths):
        if not self._running: return

        self.client.chat(
            prompt,
            file_paths,
            progress_callback=lambda msg: self.status_update.emit(msg),
            chunk_callback=lambda chunk: self.message_received.emit(chunk) if self._running else None,
            finished_callback=lambda: self.stream_finished.emit() if self._running else None
        )
    
    def stop(self):
        self._running = False
        # Note: requests stream might not be interruptible mid-chunk easily without closing connection
        # The callbacks check self._running before emitting.

class ChatServiceThread(QThread):
    def __init__(self, username, prompt, file_paths):
        super().__init__()
        self.username = username
        self.prompt = prompt
        self.file_paths = file_paths
        
        self.worker = ChatServiceWorker(username)
        self.message_received = self.worker.message_received
        self.stream_finished = self.worker.stream_finished
        self.status_update = self.worker.status_update
        self.worker.moveToThread(self) # Move worker to this thread

    def run(self):
        self.worker.process_chat(self.prompt, self.file_paths)

    def stop(self):
        self.worker.stop()
        # self.wait() # Wait can block if the requests call is stuck. Consider timeout.


# --- Worker for UI Automation ---
class UIAutomationWorker(QObject):
    message_received = Signal(str) # For AI text responses
    automation_status = Signal(str) # For status like "Clicked X,Y", "Typing..."
    automation_finished = Signal(str) # With a final message
    automation_started = Signal()

    def __init__(self, username):
        super().__init__()
        self.username = username
        self._running = False
        self.refined_prompt = ""
        self.capture_count = 0
        self.sent_count = 0

    async def get_refined_prompt(self, initial_prompt):
        self.automation_status.emit("Taking initial screenshot for prompt refinement...")
        pil_image = capture_screenshot_automation()
        buffered = BytesIO()
        
        # Convert to RGB if RGBA, as JPEG doesn't support alpha
        if pil_image.mode == 'RGBA':
            pil_image = pil_image.convert('RGB')
            
        pil_image.save(buffered, format="JPEG", quality=COMPRESSION_QUALITY) # Ensure JPEG for this endpoint
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        payload = {"image_base64": image_base64, "prompt": initial_prompt}
        
        self.automation_status.emit(f"Sending to {base}/get_better for prompt refinement...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{base}/get_better", json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.refined_prompt = result.get("better_command", "")
                        if self.refined_prompt:
                            self.automation_status.emit(f"Refined prompt: {self.refined_prompt}")
                            return True
                        else:
                            self.automation_status.emit("Error: Did not receive refined prompt.")
                            self.message_received.emit("Error: Could not get refined prompt from server.\n" + result.get("error", ""))
                            return False
                    else:
                        error_text = await response.text()
                        self.automation_status.emit(f"Error getting refined prompt: {response.status} - {error_text[:200]}")
                        self.message_received.emit(f"Error: Server returned {response.status} for prompt refinement.\n{error_text[:200]}")
                        return False
        except Exception as e:
            self.automation_status.emit(f"Exception during prompt refinement: {e}")
            self.message_received.emit(f"Exception during prompt refinement: {str(e)}")
            return False

    async def send_screenshot_and_act(self, session: aiohttp.ClientSession, img: Image.Image):
        ai_full_response_text = ""
        action_taken_msg = ""
        try:
            img_bytes, content_type = optimize_image_automation(img)
            form = aiohttp.FormData()
            form.add_field('file', img_bytes, filename='s.jpg' if USE_JPEG else 's.png', content_type=content_type)
            form.add_field('username', self.username)
            form.add_field('prompt', self.refined_prompt) # Use the refined prompt

            async with session.post(f"{base}/action_gui/", data=form, timeout=aiohttp.ClientTimeout(total=190)) as response:
                # Read the first line for metadata
                first_line_bytes = await response.content.readline()
                if not first_line_bytes:
                    self.automation_status.emit("Error: Empty response from /action_gui/ (no metadata).")
                    return {"success": False, "error": "Empty response (no metadata)"}

                processed_metadata = {}
                try:
                    metadata_str = first_line_bytes.decode('utf-8').strip()
                    processed_metadata = json.loads(metadata_str)
                except Exception as e:
                    self.automation_status.emit(f"Error decoding/processing metadata: '{metadata_str[:100]}'. Error: {e}")
                    return {"success": False, "error": f"Metadata error: {e}"}

                # self.automation_status.emit(f"Server Metadata: {processed_metadata}")
                
                if processed_metadata.get("Done", False):
                    self.automation_status.emit("Server indicated task is Done.")
                    self._running = False # Signal to stop the loop

                if "instruction_data" in processed_metadata:
                    ins_d = processed_metadata['instruction_data']
                    action_taken_msg = mouse_and_keyboard_action_automation(ins_d)
                    self.automation_status.emit(action_taken_msg)

                if processed_metadata.get("streaming_ai_response") and self._running:
                    # self.automation_status.emit("Receiving AI response stream...")
                    async for line_bytes in response.content: # Server sends lines ending with \n
                        if line_bytes and self._running:
                            try:
                                decoded_chunk = line_bytes.decode('utf-8').rstrip('\n')
                                if decoded_chunk.startswith("AI_STREAM_ERROR:"):
                                    self.message_received.emit(f"\n{decoded_chunk}\n")
                                    continue
                                # self.message_received.emit(decoded_chunk) # Emit for display
                                type_text_automation(decoded_chunk) # Type it out
                                ai_full_response_text += decoded_chunk
                            except UnicodeDecodeError:
                                self.message_received.emit(f"[Decode Error for line: {line_bytes!r}]")
                    if ai_full_response_text:
                         self.automation_status.emit(f"AI typed: '{ai_full_response_text[:50]}...'")


                if response.status == 200 and processed_metadata.get("success", False):
                    return processed_metadata
                elif response.status != 200:
                    error_text = await response.text()
                    self.automation_status.emit(f"Error: Server returned {response.status}. Response: {error_text[:200]}")
                    return {"success": False, "status_code": response.status, "error_detail": error_text}
                else: # Success False in metadata
                    self.automation_status.emit(f"Server indicated failure: {processed_metadata.get('message', 'Unknown error')}")
                    return processed_metadata

        except Exception as e:
            self.automation_status.emit(f"send_screenshot_and_act error: {type(e).__name__} - {e}")
            return {"success": False, "error": str(e)}

    async def run_automation_loop(self, initial_prompt):
        self.automation_started.emit()
        self._running = True
        self.capture_count = 0
        self.sent_count = 0

        if not await self.get_refined_prompt(initial_prompt):
            self.automation_finished.emit("Failed to start: Could not get refined prompt.")
            self._running = False
            return

        if not self.refined_prompt:
            self.automation_finished.emit("Failed to start: Refined prompt is empty.")
            self._running = False
            return
            
        self.automation_status.emit(f"Starting automation with prompt: {self.refined_prompt}")

        async with aiohttp.ClientSession() as session:
            while self._running:
                try:
                    start_capture_time = time.time()
                    img = capture_screenshot_automation()
                    capture_time = time.time() - start_capture_time
                    self.capture_count += 1

                    # self.automation_status.emit(f"Captured screenshot #{self.capture_count} ({capture_time:.3f}s)")
                    
                    start_send_time = time.time()
                    result = await self.send_screenshot_and_act(session, img)
                    send_process_time = time.time() - start_send_time

                    if result and result.get("success", False):
                        self.sent_count += 1
                        status_msg = (f"Screen #{self.sent_count} OK. "
                                      f"Cap: {capture_time:.3f}s, Send/Proc: {send_process_time:.3f}s. "
                                      f"Msg: {result.get('message', 'N/A')}. Done: {result.get('Done', False)}")
                        # self.automation_status.emit(status_msg) # Too verbose for main status
                        if result.get("Done", False):
                            self._running = False # Server says done
                    else:
                        self.automation_status.emit(f"Failed to send/process screenshot. Result: {result}")
                        await asyncio.sleep(1) # Wait a bit after failure

                    if self._running:
                        elapsed_total_cycle_time = time.time() - start_capture_time
                        sleep_duration = CAPTURE_INTERVAL - elapsed_total_cycle_time
                        if sleep_duration > 0:
                            await asyncio.sleep(sleep_duration)
                
                except pyautogui.FailSafeException:
                    self.automation_status.emit("PyAutoGUI FailSafe triggered. Stopping automation.")
                    self._running = False
                except Exception as e:
                    self.automation_status.emit(f"Automation loop error: {e}")
                    self._running = False # Stop on other critical errors
                    await asyncio.sleep(0.5)
        
        self.automation_finished.emit("Automation loop finished.")
        # Call cleanup here if it's tied to this specific automation run ending
        # remove_user_session_automation(self.username) # Or handle cleanup globally on app exit

    def stop(self):
        self.automation_status.emit("Stop request received. Finishing current cycle...")
        self._running = False

class UIAutomationThread(QThread):
    def __init__(self, username, initial_prompt):
        super().__init__()
        self.username = username
        self.initial_prompt = initial_prompt
        
        self.worker = UIAutomationWorker(username)
        # Forward signals
        self.message_received = self.worker.message_received
        self.automation_status = self.worker.automation_status
        self.automation_finished = self.worker.automation_finished
        self.automation_started = self.worker.automation_started
        self.worker.moveToThread(self)

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.worker.run_automation_loop(self.initial_prompt))
        except Exception as e:
            print(f"Error in UIAutomationThread run: {e}")
            self.worker.automation_finished.emit(f"Thread error: {e}")
        finally:
            if 'loop' in locals() and loop.is_running():
                loop.call_soon_threadsafe(loop.stop) # Gracefully stop the loop
            # loop.close() # Close might happen too soon if tasks are pending

    def stop_automation(self): # Renamed from stop to avoid QThread.stop() confusion
        self.worker.stop()
        # self.wait(5000) # Wait for thread to finish, with timeout


# --- Main Window ---
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals after UI is set up
        self.ui.send_btn.clicked.connect(self.send_user_message)
        # self.ui.send_btn.clicked.connect(self.hide_download_completion_widgets) # If this method exists
        self.ui.force_stop_button.clicked.connect(self.force_stop_current_action)
        self.ui.force_stop_button.hide() # Hide initially

        self.chat_service_thread = None
        self.ui_automation_thread = None
        self.selected_file_paths = [] # Store local paths of selected files

        self.ui.input_textEdit.setAcceptRichText(False) # Usually plain text for prompts
        self.ui.input_textEdit.installEventFilter(self)

        self.closeEvent = self.custom_close_event

        # self.accumulated_ai_response = "" # Not needed if displaying chunks directly
        self.ui.file_btn.clicked.connect(self.select_files_for_chat)

        self.upload_status_label = QLabel("") # For file selection status
        self.ui.main_content.layout().addWidget(self.upload_status_label) # Add it to layout

        self.active_animations = 0 # For managing loading animation

        # Initialize chat client for the user (used by ChatServiceWorker)
        # self.chat_client = QueenDahyunChatClient(USER_NAME) # Worker will have its own

        # For ubuntu/a_p path logic - ensure these are defined if you use them
        global ubuntu, a_p
        ubuntu = os.name == 'posix' # Example: True if on Linux/macOS
        a_p = os.path.dirname(os.path.abspath(__file__)) # Example: application path

    def select_files_for_chat(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")
        if file_dialog.exec_():
            self.selected_file_paths = file_dialog.selectedFiles()
            self.upload_status_label.setText(f"{len(self.selected_file_paths)} file(s) selected.")
            self.ui.text_browser.append("--- Files Selected ---")
            for file_path in self.selected_file_paths:
                self.display_uploaded_file(os.path.basename(file_path), file_path) # Pass full path
            self.ui.text_browser.append("--- End Files ---")


    def display_uploaded_file(self, file_name, full_path): # Added full_path
        text_browser = self.ui.text_browser
        
        user_image_path = os.path.join(a_p, "user.png") if ubuntu else "user.png"
        if not os.path.exists(user_image_path): user_image_path = "" # Handle missing

        if text_browser:
            temp_user_img_path = ""
            if user_image_path and os.path.exists(user_image_path):
                pixmap = QPixmap(user_image_path)
                scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                temp_user_img_path = os.path.join(a_p, "temp_user_image.png") # Save in accessible place
                scaled_pixmap.save(temp_user_img_path, "PNG")

            upload_message = f"""<img src='{temp_user_img_path}' width='40' height='40' style='border-radius: 20px;'> <b>File selected:</b><br>"""
            
            # Handle different file types
            if full_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                temp_preview_path = os.path.join(a_p, f"temp_preview_{file_name}")
                try:
                    pixmap = QPixmap(full_path)
                    scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    scaled_pixmap.save(temp_preview_path, "PNG") # Or appropriate format
                    upload_message += f"<span style='font-size: 12pt;'>{file_name}</span><br>"
                    upload_message += f"<img src='{temp_preview_path}' width='100' height='100'>"
                except Exception as e:
                    print(f"Error creating preview for {file_name}: {e}")
                    upload_message += f"<span style='font-size: 12pt;'>{file_name} (Preview not available)</span>"

            elif full_path.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv')):
                upload_message += f"<span style='font-size: 12pt;'>{file_name}</span><br>"
                # QTextBrowser doesn't directly support <video> or <audio>.
                # You might link to it or show an icon.
                upload_message += f"<i>Video file (preview not supported in chat): {file_name}</i>"
            
            elif full_path.lower().endswith(('.mp3', '.wav', '.ogg', '.aac')):
                upload_message += f"<span style='font-size: 12pt;'>{file_name}</span><br>"
                upload_message += f"<i>Audio file (preview not supported in chat): {file_name}</i>"
            else:
                upload_message += f"<span style='font-size: 12pt;'>{file_name}</span>"

            upload_message += "<br><br>"
            text_browser.append(upload_message)
            text_browser.verticalScrollBar().setValue(text_browser.verticalScrollBar().maximum())

    def set_input_state(self, enabled: bool):
        self.ui.input_textEdit.setEnabled(enabled)
        self.ui.send_btn.setEnabled(enabled)
        self.ui.file_btn.setEnabled(enabled)
        self.ui.model_combo.setEnabled(enabled) # Keep for consistency, though not used by new APIs
        self.ui.action_toggle.setEnabled(enabled)
        if enabled:
            self.ui.force_stop_button.hide()
            self.stop_processing_animation()
        else:
            self.start_processing_animation()
            # Show stop button only if an action/automation is running
            if self.ui_automation_thread and self.ui_automation_thread.isRunning():
                 self.ui.force_stop_button.show()


    def send_user_message(self):
        user_input = self.ui.input_textEdit.toPlainText().strip()
        if not user_input: return

        self.set_input_state(False)
        self.display_user_message(user_input)

        if self.ui.action_toggle.is_on(): # UI Automation Mode
            if self.ui_automation_thread and self.ui_automation_thread.isRunning():
                self.ui_automation_thread.stop_automation() # Stop previous if any
                self.ui_automation_thread.wait()

            self.ui_automation_thread = UIAutomationThread(USER_NAME, user_input)
            self.ui_automation_thread.automation_started.connect(self.handle_automation_start)
            self.ui_automation_thread.automation_status.connect(self.display_automation_status)
            self.ui_automation_thread.message_received.connect(self.display_ai_response_from_automation) # Could be different display
            self.ui_automation_thread.automation_finished.connect(self.handle_automation_finish)
            self.ui_automation_thread.start()
            self.ui.force_stop_button.show()

        else: # Multi-turn Chat Mode
            if self.chat_service_thread and self.chat_service_thread.isRunning():
                self.chat_service_thread.stop()
                self.chat_service_thread.wait()

            self.start_ai_response_display() # Prepare QueenDahyun avatar etc.
            self.chat_service_thread = ChatServiceThread(USER_NAME, user_input, self.selected_file_paths)
            self.chat_service_thread.status_update.connect(self.display_chat_status)
            self.chat_service_thread.message_received.connect(self.append_ai_response_chunk)
            self.chat_service_thread.stream_finished.connect(self.handle_chat_finish)
            self.chat_service_thread.start()

        # self.hide_download_completion_widgets() # If exists
        self.ui.input_textEdit.clear()
        self.selected_file_paths = [] # Clear after sending
        self.upload_status_label.clear()


    def start_processing_animation(self):
        self.active_animations += 1
        self.ui.upload_animation.show()
        if hasattr(self.ui.upload_animation, 'timer') and self.ui.upload_animation.timer:
            self.ui.upload_animation.timer.start()

    def stop_processing_animation(self):
        self.active_animations -= 1
        if self.active_animations <= 0:
            self.active_animations = 0
            if hasattr(self.ui.upload_animation, 'stopAnimation'):
                 self.ui.upload_animation.stopAnimation()
            else: # Fallback for simpler animation widgets
                 self.ui.upload_animation.hide()


    def custom_close_event(self, event):
        print("Closing application...")
        if hasattr(self.ui, 'upload_animation') and hasattr(self.ui.upload_animation, 'stopAnimation'):
            self.ui.upload_animation.stopAnimation()

        if self.chat_service_thread and self.chat_service_thread.isRunning():
            print("Stopping chat service thread...")
            self.chat_service_thread.stop()
            self.chat_service_thread.wait(2000) # Wait a bit

        if self.ui_automation_thread and self.ui_automation_thread.isRunning():
            print("Stopping UI automation thread...")
            self.ui_automation_thread.stop_automation()
            self.ui_automation_thread.wait(3000) # Wait a bit
            # Perform final cleanup for UI automation user session
            print(f"Performing final UI automation session cleanup for {USER_NAME}...")
            # Run in a blocking way or a short-lived thread if it's network IO
            # For simplicity here, direct call (might hang GUI briefly)
            remove_user_session_automation(USER_NAME)


        # Clear chat session on server
        client_temp = QueenDahyunChatClient(USER_NAME)
        print(f"Clearing chat session for {USER_NAME}...")
        client_temp.clear_session()

        super().closeEvent(event)


    def eventFilter(self, obj, event):
        if obj is self.ui.input_textEdit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                if event.modifiers() & Qt.ShiftModifier:
                    self.ui.input_textEdit.insertPlainText('\n')
                    return True
                else:
                    self.send_user_message()
                    return True
        return super().eventFilter(obj, event)

    def display_user_message(self, user_input):
        text_browser = self.ui.text_browser
        user_image_path = os.path.join(a_p, "user.png") if ubuntu else "user.png"
        if not os.path.exists(user_image_path): user_image_path = ""

        temp_user_img_path = ""
        if user_image_path:
            pixmap = QPixmap(user_image_path)
            scaled_pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            temp_user_img_path = os.path.join(a_p, "temp_user_image_display.png")
            scaled_pixmap.save(temp_user_img_path, "PNG")
        
        user_message = f"""
        <table style='margin-bottom: 10px; width: 100%;'>
            <tr>
                <td style='vertical-align: top; width: 40px;'>
                    <img src='{temp_user_img_path}' width='40' height='40' style='border-radius: 20px;'>
                </td>
                <td style='vertical-align: top; padding-left: 10px;'>
                    <b>User:</b><br>
                    <div style='margin-top: 5px; white-space: pre-wrap; word-wrap: break-word;'>
                        <span style='font-size: 12pt;'>{user_input.replace("<", "<").replace(">", ">")}</span>
                    </div>
                </td>
            </tr>
        </table>"""
        text_browser.append(user_message) # append handles scroll to bottom

    def start_ai_response_display(self): # For chat mode
        queendahyun_image_path = os.path.join(a_p, "queendahyun.png") if ubuntu else "queendahyun.png"
        if not os.path.exists(queendahyun_image_path): queendahyun_image_path = ""
        
        temp_qd_img_path = ""
        if queendahyun_image_path:
            pixmap = QPixmap(queendahyun_image_path)
            scaled_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation) # Slightly smaller
            temp_qd_img_path = os.path.join(a_p, "temp_queendahyun_display.png")
            scaled_pixmap.save(temp_qd_img_path, "PNG")

        ai_message_header = f"""
        <table style='margin-bottom: 10px; width: 100%;'>
            <tr>
                <td style='vertical-align: top; width: 50px;'>
                    <img src='{temp_qd_img_path}' width='50' height='50' style='border-radius: 10px;'>
                </td>
                <td style='vertical-align: top; padding-left: 10px;'>
                    <b>QueenDahyun:</b><br>
                    <div style='margin-top: 5px; white-space: pre-wrap; word-wrap: break-word; font-size: 12pt;' id='ai_response_content'>""" # Added id
        
        self.ui.text_browser.append(ai_message_header) # Append header
        self._ai_response_started = True


    def append_ai_response_chunk(self, chunk): # For chat mode
        if not hasattr(self, '_ai_response_started') or not self._ai_response_started:
            self.start_ai_response_display()

        # Sanitize chunk for HTML if not already done by server
        # For plain text, this is safer:
        # safe_chunk = chunk.replace("&", "&").replace("<", "<").replace(">", ">").replace("\n", "<br>")
        # self.ui.text_browser.insertHtml(safe_chunk) # insertHtml at cursor
        
        # If server sends plain text and we want QTextBrowser to handle newlines:
        self.ui.text_browser.insertPlainText(chunk)
        self.ui.text_browser.verticalScrollBar().setValue(self.ui.text_browser.verticalScrollBar().maximum())
        self.stop_processing_animation() # Stop animation on first chunk

    def finalize_ai_response_display(self): # For chat mode
        if hasattr(self, '_ai_response_started') and self._ai_response_started:
            closing_div = "</div></td></tr></table>"
            self.ui.text_browser.append(closing_div) # Append closing tags
            self._ai_response_started = False


    def display_chat_status(self, status):
        self.upload_status_label.setText(f"Chat: {status}")

    def handle_chat_finish(self):
        self.finalize_ai_response_display()
        self.set_input_state(True)
        self.upload_status_label.setText("Chat finished.")

    # --- UI Automation Specific Handlers ---
    def handle_automation_start(self):
        self.upload_status_label.setText("UI Automation: Starting...")
        self.display_automation_status("Attempting to start UI automation...")
        # Avatar for automation messages (can be same as QueenDahyun or a different one)
        # For simplicity, let's use a generic system message style
        self.ui.text_browser.append("<hr><b>--- UI Automation Log ---</b>")


    def display_automation_status(self, status):
        # self.upload_status_label.setText(f"Automation: {status}")
        # Display important status messages in the chat log too
        self.ui.text_browser.append(f"<i>{status.replace('<', '<').replace('>', '>')}</i>")
        self.ui.text_browser.verticalScrollBar().setValue(self.ui.text_browser.verticalScrollBar().maximum())


    def display_ai_response_from_automation(self, chunk):
        # This is for AI text that might be typed or just logged
        # For now, just log it as part of automation status
        # self.display_automation_status(f"AI output: {chunk}")
        # If it's meant to be displayed like a chat message:
        if not hasattr(self, '_automation_ai_response_started') or not self._automation_ai_response_started:
            # You can use a similar start_ai_response_display or a modified one for automation
            queendahyun_image_path = os.path.join(a_p, "queendahyun.png") if ubuntu else "queendahyun.png"
            # ... (load image, create header) ...
            ai_message_header = f"""
            <table style='margin-bottom: 10px; width: 100%;'><tr><td style='vertical-align: top; width: 50px;'>
            <img src='{os.path.join(a_p, "temp_queendahyun_display.png")}' width='50' height='50' style='border-radius: 10px;'>
            </td><td style='vertical-align: top; padding-left: 10px;'><b>QueenDahyun (Automation):</b><br>
            <div style='margin-top: 5px; white-space: pre-wrap; word-wrap: break-word; font-size: 12pt;'>"""
            self.ui.text_browser.append(ai_message_header)
            self._automation_ai_response_started = True
        
        self.ui.text_browser.insertPlainText(chunk) # Assuming plain text chunks
        self.ui.text_browser.verticalScrollBar().setValue(self.ui.text_browser.verticalScrollBar().maximum())
        self.stop_processing_animation()


    def handle_automation_finish(self, message):
        if hasattr(self, '_automation_ai_response_started') and self._automation_ai_response_started:
            self.ui.text_browser.append("</div></td></tr></table>") # Close AI message table
            self._automation_ai_response_started = False

        self.ui.text_browser.append(f"<b>--- UI Automation Ended: {message} ---</b><hr>")
        self.set_input_state(True)
        self.upload_status_label.setText(f"Automation: {message}")
        self.ui.force_stop_button.hide()
        # Optionally call remove_user_session here if not done on global close
        # remove_user_session_automation(USER_NAME)


    def force_stop_current_action(self):
        self.upload_status_label.setText("Force stop requested...")
        if self.ui_automation_thread and self.ui_automation_thread.isRunning():
            self.display_automation_status("Force stopping UI automation...")
            self.ui_automation_thread.stop_automation()
            # The thread's finish signal will call handle_automation_finish
            # Cleanup of session can be done there or on app close.
            # For immediate effect:
            # QTimer.singleShot(100, lambda: remove_user_session_automation(USER_NAME)) # Run slightly after stop
        elif self.chat_service_thread and self.chat_service_thread.isRunning():
            self.display_chat_status("Force stopping chat...")
            self.chat_service_thread.stop()
            # Stream_finished will call handle_chat_finish
        else:
            self.upload_status_label.setText("No action running to stop.")
            self.set_input_state(True) # Ensure UI is re-enabled


