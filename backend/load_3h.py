import schedule
import time
import subprocess

#ce script ne semble pas fonctionner apres dockerisation

print("chargement de la database 10h 13H 16H 19H 22H 01H 04H 07H")

def run_batch_script():
    print("Chargement des villes if not exist")
    subprocess.run(["python3.11", "loading_cities.py"])
    print("Exécution du script main.py...")
    subprocess.run(["python3.11", "main.py"])

hours_to_schedule = ["10:00", "13:00", "15:20", "16:00", "19:00", "22:00", "01:00", "04:00", "07:00"]

for hour in hours_to_schedule:
    schedule.every().day.at(hour).do(run_batch_script)

while True:
    schedule.run_pending()
    time.sleep(30) 