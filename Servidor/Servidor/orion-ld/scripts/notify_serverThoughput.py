from flask import Flask, request
from datetime import datetime
import json
import ntplib
import time
import threading
import requests
import os

app = Flask(__name__)

# =========================
# CONFIG EXPERIMENTO
# =========================

experiment_name = input("Nombre del experimento: ")

output_dir = f"resultsThrouhput/{experiment_name}"
os.makedirs(output_dir, exist_ok=True)
LOG_FILE = f"{output_dir}/metrics.jsonl"

TEST_DURATION = 60  # segundos
WARMUP_SAMPLES = 100

msg_count = 0
warmup_count = 0

warmup_done = False
start_time = None
experiment_finished = False


CONTROL_SERVER = "172.31.232.42:5000"

def esperar_inicio():
    print("Esperando orden de inicio...")

    while True:
        try:
            r = requests.get(f"http://{CONTROL_SERVER}/status", timeout=1)

            if r.json()["start"]:
                print("Orden recibida. Iniciando experimento...")
                return

        except Exception:
            pass

        time.sleep(0.1)

# =========================
# NTP OFFSET
# =========================
def calcular_offset_local(ip_servidor, puerto=123):
    cliente = ntplib.NTPClient()
    try:
        respuesta = cliente.request(ip_servidor, port=puerto, version=3)
        return respuesta.offset
    except:
        return 0.0

mi_offset = calcular_offset_local("172.31.232.59", 123)
print(f"Offset consumidor: {mi_offset*1000:.3f} ms")

def now():
    return datetime.utcfromtimestamp(time.time() + mi_offset)

# =========================
# ESTADO EXPERIMENTO
# =========================
msg_count = 0
start_time = None
experiment_finished = False

# =========================
# FINAL EXPERIMENTO
# =========================
def stop_experiment():
    global experiment_finished, msg_count

    time.sleep(TEST_DURATION)
    experiment_finished = True

    throughput = msg_count / TEST_DURATION

    result = {
        "total_messages": msg_count,
        "duration": TEST_DURATION,
        "throughput_msgs_s": throughput,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(LOG_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print("\n==============================")
    print("EXPERIMENTO FINALIZADO")
    print(f"Mensajes totales: {msg_count}")
    print(f"Throughput: {throughput:.2f} msgs/s")
    print(f"Guardado en: {LOG_FILE}")
    print("==============================")

    print("\nExperimento finalizado. Cerrando servidor...")
    os._exit(0)

# =========================
# ENDPOINT
# =========================
@app.route("/notify", methods=["POST"])
def notify():
    global msg_count, warmup_count, warmup_done, start_time, experiment_finished

    if experiment_finished:
        return "", 204

    data = request.json

    try:
        entity = data["data"][0]

        # =========================
        # WARMUP
        # =========================
        if not warmup_done:
            warmup_count += 1

            if warmup_count == 1:
                print("WARMUP iniciado...")

            if warmup_count >= WARMUP_SAMPLES:
                warmup_done = True
                msg_count = 0
                start_time = time.time()

                print("WARMUP completado. Iniciando medición...")

                threading.Thread(
                    target=stop_experiment,
                    daemon=True
                ).start()

            return "", 204

        # =========================
        # MEDICIÓN REAL
        # =========================
        msg_count += 1

        print(f"{msg_count} | {entity['id']}")

    except Exception as e:
        print("Error:", e)

    return "", 204
# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    esperar_inicio()
    app.run(host="0.0.0.0", port=5001)
