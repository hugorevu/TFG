from flask import Flask, request
from datetime import datetime
import json
import ntplib
import time
import requests
import statistics
import threading
import numpy as np
import os

app = Flask(__name__)

experiment_name = input("Nombre del experimento: ")

output_dir = f"results/{experiment_name}"
os.makedirs(output_dir, exist_ok=True)

LOG_FILE = f"{output_dir}/latencies.jsonl"
STATS_FILE = f"{output_dir}/latency_stats.json"

CONTROL_SERVER = "172.31.232.42:5000"

TEST_DURATION = 60
WARMUP_SAMPLES = 100

latencies = []
start_time = None
experiment_started = False
experiment_finished = False

warmup_count = 0
warmup_done = False


# =========================
# START CONTROL
# =========================
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

# =========================
# FINAL EXPERIMENTO
# =========================
def stop_experiment():
    global experiment_finished

    time.sleep(TEST_DURATION)
    experiment_finished = True

    if not latencies:
        return

    stats = {
        "count": len(latencies),
        "mean": float(np.mean(latencies)),
        "median": float(np.median(latencies)),
        "min": float(np.min(latencies)),
        "max": float(np.max(latencies)),
        "std": float(np.std(latencies)) if len(latencies) > 1 else 0.0,
        "p95": float(np.percentile(latencies, 95)),
        "p99": float(np.percentile(latencies, 99))
    }

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

    print("\n========== ESTADÍSTICAS FINALES ==========")
    print(json.dumps(stats, indent=4))

    print("\nExperimento finalizado. Cerrando servidor...")
    os._exit(0)


# =========================
# ENDPOINT NOTIFY
# =========================
@app.route("/notify", methods=["POST"])
def notify():
    global warmup_count, warmup_done, experiment_finished

    if experiment_finished:
        return "", 204

    received_at = datetime.utcfromtimestamp(time.time() + mi_offset)
    data = request.json

    try:
        entity = data["data"][0]

        date_observed = entity.get("dateObserved", {}).get("value", None)
        if not date_observed:
            return "", 204

        observed_at = datetime.fromisoformat(date_observed.replace("Z", ""))

        # =========================
        # WARMUP
        # =========================
        if not warmup_done:
            warmup_count += 1

            if warmup_count >= WARMUP_SAMPLES:
                warmup_done = True
                print("\nWARMUP completado. Iniciando medición...\n")

                # IMPORTANTE: empezar timer aquí
                threading.Thread(target=stop_experiment, daemon=True).start()

            return "", 204

        # =========================
        # MEDICIÓN REAL
        # =========================
        latency = (received_at - observed_at).total_seconds()
        latencies.append(latency)

        record = {
            "entity": entity["id"],
            "dateObserved": observed_at.isoformat() + "Z",
            "receivedAt": received_at.isoformat() + "Z",
            "total_latency": latency
        }

        with open(LOG_FILE, "a") as f:
            json.dump(record, f)
            f.write("\n")

    except Exception as e:
        print("Error:", e)

    return "", 204

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    esperar_inicio()
    app.run(host="0.0.0.0", port=5002)
