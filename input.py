import os
import sys
import requests
from datetime import datetime

SESSION = {"session": "SESSION_KEY"}

if len(sys.argv) > 1:
    day = sys.argv[1].strip()
else:
    day = str(int(datetime.now().strftime("%d")))

data = requests.get(f"https://adventofcode.com/2022/day/{day}/input", \
                    cookies=SESSION).content.decode("utf-8")

folder = f"day{day.zfill(2)}"

if not os.path.exists(folder):
    os.mkdir(folder)

with open(f"{folder}/input", "w") as f:
    f.write(data)

print("epic win")
