import os
import time

local_path = os.path.abspath(".")
print(local_path)
os.system(f"python {local_path}\\main.py")
time.sleep(5)