from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)

LOG_FILE = "latencies.jsonl"


@app.route("/notify", methods=["POST"])
def notify():

    received_at = datetime.utcnow()
    data = request.json

    try:
        notified_at = datetime.fromisoformat(
            data["notifiedAt"].replace("Z", "")
        )

        entity = data["data"][0]

        print("\n========== NOTIFICACIÓN ==========")
        print(f"Entidad: {entity['id']}")

        print("\n--- DATA RECIBIDO ---")
        print(json.dumps(entity, indent=2, ensure_ascii=False))

        observed_at = None
        sensor_type = None

        for key, value in entity.items():
            if isinstance(value, dict) and "observedAt" in value:
                observed_at = datetime.fromisoformat(
                    value["observedAt"].replace("Z", "")
                )
                sensor_type = key
                break

        if observed_at:

            total_latency = (received_at - observed_at).total_seconds()

            print("\n--- LATENCIAS ---")
            print(f"ObservedAt : {observed_at}")
            print(f"ReceivedAt : {received_at}")
            print("--------------------------------")
            print(f"Total  : {total_latency:.3f} s")

            # =========================
            # 🔥 GUARDAR EN JSONL
            # =========================
            record = {
                "entity": entity["id"],
                "sensor": sensor_type,
                "observedAt": observed_at.isoformat(),
                "receivedAt": received_at.isoformat(),
                "total_latency": total_latency
            }

            with open(LOG_FILE, "a") as f:
                json.dump(record, f)
                f.write("\n")

        print("================================\n")

    except Exception as e:
        print("Error calculando latencias:", e)

    return "", 204


if __name__ == "__main__":
    app.run(port=5000)