import json
import sys
import requests
import time
import ntplib
from datetime import datetime

BROKERS = {
    #"orion": "http://172.31.232.59:1026",
    "orion": "http://localhost:1026",
    "scorpio": "http://172.31.232.59:9090",
    "stellio": "http://172.31.232.59:8080"
}

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

#CONTROL_SERVER = "172.31.232.42:5001"  # servidor maestro
CONTROL_SERVER = "localhost:5001"  # servidor maestro

DELAYS = [0.5, 0.2, 0.1]

vehicle_id = sys.argv[1]
delay = float(sys.argv[2])
broker = sys.argv[3].lower()

if delay not in DELAYS:
    raise ValueError(f"Delay no válido. Opciones: {DELAYS}")

if broker not in BROKERS:
    raise ValueError(f"Broker no válido. Opciones: {list(BROKERS.keys())}")

BROKER_URL = f"{BROKERS[broker]}/ngsi-ld/v1/entities"

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


#mi_offset = calcular_offset_local('172.31.232.59', 123)

#print(f"Desfase NTP: {mi_offset*1000:.3f} ms")

def now():
    return datetime.utcfromtimestamp(
        time.time()
        #+ mi_offset
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
    entity_id = f"urn:ngsi-ld:DeviceMeasurementIMU:{i}"
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

    entity_id = f"urn:ngsi-ld:DeviceMeasurementGNSS:{i}"
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

    entity_id = f"urn:ngsi-ld:DeviceMeasurementCamera:{i}"
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

    entity_id = f"urn:ngsi-ld:DeviceMeasurementLiDAR:{i}"
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

    entity_id = f"urn:ngsi-ld:DeviceMeasurementRadar:{i}"
    patch_entity(entity_id, payload)


# =========================
# FRAME PROCESSOR
# =========================

def process_frame(frame, vehicle_id):
    sensors = frame.get("sensors", {})


    if "imu" in sensors:
        update_imu(sensors["imu"],vehicle_id)

    if "gnss" in sensors:
        update_gnss(sensors["gnss"],vehicle_id)

    if "CameraRGB" in sensors:
        update_camera(sensors["CameraRGB"],vehicle_id)

    if "LiDAR" in sensors:
        update_lidar(sensors["LiDAR"],vehicle_id)

    if "Radar" in sensors:
        update_radar(sensors["Radar"],vehicle_id)


# =========================
# SIMULADOR
# =========================

def run_simulation(file_path, delay):
    with open(file_path) as f:
        data = json.load(f)

    start_time = time.monotonic()
    duration = 60

    for frame in data:

        # Comprobar si han pasado 60 segundos
        if time.monotonic() - start_time >= duration:
            break

        print(f"Processing frame {frame['frame']}")
        print(f"  Updating vehicle {vehicle_id}")

        process_frame(frame, vehicle_id)

        # Esperar sin superar el tiempo restante
        remaining = duration - (time.monotonic() - start_time)

        if remaining > 0:
            time.sleep(min(delay, remaining))

    print(f"Simulation finished: {vehicle_id}")


# =========================
# START
# =========================

if __name__ == "__main__":
    esperar_inicio()
    run_simulation("../../examples/Json/dataset1000frames.json", delay=delay)
