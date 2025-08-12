import subprocess
import time
from datetime import datetime

# Defintionen
start_times = ["00:00", "12:00"]

# Checken, ob aktuell eine Startzeit ist, wenn ja: Kamera starten und entsprechend abspeichern
while True:
    # Zeit holen
    time_now = datetime.now().strftime("%H:%M")
    date_now = datetime.now().date()

    if time_now in start_times:
        # Dateiname
        if time_now == "00:00":
            file_name = f"{date_now}_1.mp4"
        elif time_now == "12:00":
            file_name = f"{date_now}_2.mp4"
        else:
            file_name = f"error_{date_now}_{time_now}.mp4"

        # Kamerastart über Terminal
        command = f"./minimal_pylon -f 10 -q 15 -n 70000 -c 2 -w 2200 -h 1600 -x 500 -y 500 -e 30000 -g1 10.0 -g2 8.8 -o {file_name}"

        try:
            print(f"Starte Aufnahme: {file_name}")
            subprocess.run(command, shell=True)
            print("Aufnahme abgeschlossen.")
        except subprocess.CalledProcessError as e:
            print(f"Fehler bei Aufnahme: {e}")
        time.sleep(6000)
    else:
        time.sleep(30)
