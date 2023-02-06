import subprocess
import sys
import time

client = subprocess.Popen([sys.executable, 'ru_vpn.py'])
time.sleep(10)

client3 = subprocess.Popen([sys.executable, 'time_manager.py'])
time.sleep(5)
client.wait()