from flask import Flask, request
from datetime import datetime
import json
import ntplib
import time
import requests

app = Flask(__name__)

LOG_FILE = "latencies.jsonl"

CONTROL_SERVER = "172.31.232.42:5000"  # servidor maestro

def esperar_inicio():
    print("Esperando orden de inicio...")

    while True:
        try:
            r = requests.get(f"http://{CONTROL_SERVER}/status", timeout=1)

            if r.json()["start"]:
                print("Orden recibida. Iniciando...")
                return

        except Exception:
            pass

        time.sleep(0.1)

def calcular_offset_local(ip_servidor, puerto=123):
    cliente = ntplib.NTPClient()
    try:
        respuesta = cliente.request(ip_servidor, port=puerto, version=3)
        return respuesta.offset
    except:
        return 0.0


mi_offset = calcular_offset_local("172.31.232.59", 123)
print(f"Offset consumidor: {mi_offset*1000:.3f} ms")

def parse_time(ts):
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", ""))

@app.route("/notify", methods=["POST"])
def notify():

    received_at = datetime.utcfromtimestamp(
    time.time() + mi_offset
    )
    data = request.json

    try:
        entity = data["data"][0]

        print("\n========== NOTIFICACIÓN ==========")
        print(f"Entidad: {entity['id']}")

        print("\n--- DATA RECIBIDO ---")
        print(json.dumps(entity, indent=2, ensure_ascii=False))

        # =========================
        # EXTRAER dateObserved
        # =========================
        date_observed = None

        if "dateObserved" in entity:
            date_observed = entity["dateObserved"]["value"]

        if date_observed:
            observed_at = datetime.fromisoformat(date_observed.replace("Z", ""))

            end_to_end_latency = (received_at - observed_at).total_seconds()

            print("\n--- LATENCIAS ---")
            print(f"dateObserved (sensor): {observed_at}")
            print(f"receivedAt (consumer): {received_at}")
            print("--------------------------------")
            print(f"End-to-End latency : {end_to_end_latency:.3f} s")

            # =========================
            # LOG JSONL
            # =========================
            record = {
                "entity": entity["id"],
                "dateObserved": observed_at.isoformat() + "Z",
                "receivedAt": received_at.isoformat() + "Z",
                "total_latency": end_to_end_latency
            }

            with open(LOG_FILE, "a") as f:
                json.dump(record, f)
                f.write("\n")

        print("================================\n")

    except Exception as e:
        print("Error calculando latencias:", e)

    return "", 204


if __name__ == "__main__":
    esperar_inicio()
    app.run(host="0.0.0.0", port=5002)
