import subprocess
import time

while True:
    process = subprocess.Popen(["uvicorn", "main:app", "--reload", "--host", "192.168.1.12"])
    process.wait()
    time.sleep(3)