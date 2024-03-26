import schedule
import time
import subprocess

def run_batch_script():
    print("Exécution du script main.py...")
    subprocess.run(["python3.11", "main.py"])

hours_to_schedule = ["10:00", "13:00", "16:00", "19:00", "22:00", "01:00", "04:00", "07:00"]

for hour in hours_to_schedule:
    schedule.every().day.at(hour).do(run_batch_script)

while True:
    schedule.run_pending()
    time.sleep(300) 