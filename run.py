import subprocess
import threading
import time

process = None

def run_executable():
    global process
    executable_path = r"fastserver.exe"
    process = subprocess.Popen([executable_path])

thread = threading.Thread(target=run_executable)
thread.start()

print(f"next process")
for i in range(100):
    time.sleep(1)
    print('dahyun+darwin=dahwin')


process.terminate()  # Terminate the subprocess
thread.join()  # Wait for the thread to finish


# taskkill /im fastserver.exe /f
# taskkill /im queendahyunserver.exe /f