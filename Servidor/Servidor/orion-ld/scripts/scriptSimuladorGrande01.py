import json
import requests
import time
import ntplib
from datetime import datetime

BROKER_URL = "http://172.31.232.59:1026/ngsi-ld/v1/entities"

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

CONTROL_SERVER = "172.31.232.42:5001"  # servidor maestro

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

# =========================
# HELPERS
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
        print(f"Error sincronizando con NTP local: {e}")
        return 0.0


mi_offset = calcular_offset_local('172.31.232.59', 123)

print(f"Desfase NTP: {mi_offset*1000:.3f} ms")

def now():
    return datetime.utcfromtimestamp(
        time.time() + mi_offset
    ).isoformat(timespec="milliseconds") + "Z"

def patch_entity(entity_id, payload):
    url = f"{BROKER_URL}/{entity_id}/attrs"

    body = {
        "@context": CONTEXT,
        **payload
    }

    response = requests.patch(url, headers=HEADERS, json=body)

    if response.status_code not in [204]:
        print(f"Error updating {entity_id}: {response.status_code} -> {response.text}")


# =========================
# IMU
# =========================

def update_imu(data, i):
    timestamp = now()

    payload = {
    "textValue": {
        "type": "Property",
        "value": {
            "accelerometer": data["accelerometer"],
            "gyroscope": data["gyroscope"],
            "compass": data["compass"]
        },
        "observedAt": timestamp
    },
    "dateObserved": {
            "type": "Property",
            "value": timestamp
    }
}
    entity_id = f"urn:ngsi-ld:DeviceMeasurementIMU:{i:03d}"
    patch_entity(entity_id, payload)


# =========================
# GNSS
# =========================

def update_gnss(data, i):
    timestamp = now()

    payload = {
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": [
                    data["longitude"],
                    data["latitude"]
                ]
            },
            "observedAt": timestamp
        },
        "dateObserved": {
            "type": "Property",
            "value": timestamp
        }
    }

    entity_id = f"urn:ngsi-ld:DeviceMeasurementGNSS:{i:03d}"
    patch_entity(entity_id, payload)


# =========================
# CAMERA
# =========================

def update_camera(data, i):
    timestamp = now()

    payload = {
        "textValue": {
            "type": "Property",
            "value": data["frameURI"],
            "observedAt": timestamp
        },
        "dateObserved": {
            "type": "Property",
            "value": timestamp
        }
    }

    entity_id = f"urn:ngsi-ld:DeviceMeasurementCamera:{i:03d}"
    patch_entity(entity_id, payload)


# =========================
# LiDAR
# =========================

def update_lidar(data, i):
    timestamp = now()

    payload = {
        "textValue": {
            "type": "Property",
            "value": data["cloudUri"],
            "observedAt": timestamp
        },
        "numValue": {
            "type": "Property",
            "value": data["num_points"],
            "observedAt": timestamp
        },
        "dateObserved": {
            "type": "Property",
            "value": timestamp
        }
    }

    entity_id = f"urn:ngsi-ld:DeviceMeasurementLiDAR:{i:03d}"
    patch_entity(entity_id, payload)


# =========================
# RADAR
# =========================

def update_radar(data, i):
    timestamp = now()

    payload = {
        "numValue": {
            "type": "Property",
            "value": data["num_detections"],
            "observedAt": timestamp
        },
        "textValue": {
            "type": "Property",
            "value": data["cloudUri"],
            "observedAt": timestamp
        },
        "dateObserved": {
            "type": "Property",
            "value": timestamp
        }
    }

    entity_id = f"urn:ngsi-ld:DeviceMeasurementRadar:{i:03d}"
    patch_entity(entity_id, payload)


# =========================
# FRAME PROCESSOR
# =========================

def process_frame(frame, i):
    sensors = frame.get("sensors", {})


    if "imu" in sensors:
        update_imu(sensors["imu"],i)

    if "gnss" in sensors:
        update_gnss(sensors["gnss"],i)

    if "CameraRGB" in sensors:
        update_camera(sensors["CameraRGB"],i)

    if "LiDAR" in sensors:
        update_lidar(sensors["LiDAR"],i)

    if "Radar" in sensors:
        update_radar(sensors["Radar"],i)


# =========================
# SIMULADOR
# =========================

NUM_DEVICES = 1

def run_simulation(file_path, delay=0.5):
    with open(file_path) as f:
        data = json.load(f)

    for frame in data:
        print(f"Processing frame {frame['frame']}")

        for i in range(1, NUM_DEVICES+1):
            print(f"  Updating device {i:03d}")
            process_frame(frame, i)

        time.sleep(delay)


# =========================
# START
# =========================

if __name__ == "__main__":
    esperar_inicio()
    run_simulation("../../examples/Json/dataset1000frames.json", delay=0.1)
