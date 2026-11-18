
from flask import Flask, request
from datetime import datetime, timezone
import json
import os
import time
import ntplib
import threading
import requests

#CONTROL_SERVER = "http://172.31.232.42:5000"
CONTROL_SERVER = "http://localhost:5000"


app = Flask(__name__)

# =========================
# CONFIG EXPERIMENTO
# =========================

experiment_name = input("Nombre del experimento: ")

output_dir = f"results/{experiment_name}"
os.makedirs(output_dir, exist_ok=True)

OUTPUT_FILE = f"{output_dir}/notifications.jsonl"

file_lock = threading.Lock()
start_time = None

def esperar_inicio():
    print("Esperando orden de inicio...")

    while True:
        try:
            r = requests.get(f"{CONTROL_SERVER}/status", timeout=1)
            status = r.json()

            if status["start"]:
                print("Orden recibida. Iniciando servidor...")
                return

        except Exception as e:
            print("Esperando inicio:", e)

        time.sleep(0.1)

# =========================
# NTP OFFSET
# =========================

def calcular_offset_local(ip_servidor, puerto=123):
    cliente = ntplib.NTPClient()

    try:
        respuesta = cliente.request(
            ip_servidor,
            port=puerto,
            version=3
        )
        return respuesta.offset

    except Exception as e:
        print(f"Error sincronizando NTP: {e}")
        return 0.0


#mi_offset = calcular_offset_local("172.31.232.59", 123)

#print(f"Offset consumidor: {mi_offset*1000:.3f} ms")


def now():
    return datetime.fromtimestamp(
        time.time(), 
        #+ mi_offset,
        tz=timezone.utc
    ).isoformat(timespec="milliseconds").replace("+00:00", "Z")


# =========================
# ENDPOINT NOTIFICACIONES
# =========================
@app.route("/notify", methods=["POST"])
def notify():
    global start_time

    received_at = now()

    try:
        data = request.get_json()
        entities = data.get("data", [])

        with file_lock:

            # Guardar inicio con la primera notificación
            if entities and start_time is None:

                start_time = received_at

                experiment_info = {
                    "experiment": experiment_name,
                    "start_time": start_time,
                    "duration": 60
                }

                with open(f"{output_dir}/experiment.json", "w") as f:
                    json.dump(experiment_info, f, indent=4)

                print("Primera notificación:", start_time)

            # Guardar todas las notificaciones
            for entity in entities:

                record = {
                    "entity_id": entity.get("id"),
                    "dateObserved": entity.get(
                        "dateObserved", {}
                    ).get("value"),
                    "receivedAt": received_at
                }

                with open(OUTPUT_FILE, "a") as f:
                    json.dump(record, f)
                    f.write("\n")

    except Exception as e:
        print("Error processing notification:", e)
        return "Error", 400

    return "", 200

# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    esperar_inicio()
    app.run(host="0.0.0.0", port=5006)