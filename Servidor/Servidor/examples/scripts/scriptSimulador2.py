import json
import requests
import time
from datetime import datetime

BROKER_URL = "http://localhost:8080/ngsi-ld/v1/entities"

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

# =========================
# HELPERS
# =========================

def now():
    return datetime.utcnow().isoformat() + "Z"

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

def update_imu(data):
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
    }
}

    patch_entity("urn:ngsi-ld:DeviceMeasurementIMU:002", payload)


# =========================
# GNSS
# =========================

def update_gnss(data):
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
        }
    }

    patch_entity("urn:ngsi-ld:DeviceMeasurementGNSS:002", payload)


# =========================
# CAMERA
# =========================

def update_camera(data):
    payload = {
        "textValue": {
            "type": "Property",
            "value": data["relative_path"]
        }
    }

    patch_entity("urn:ngsi-ld:DeviceMeasurementCamera:002", payload)


# =========================
# LiDAR
# =========================

def update_lidar(data):
    timestamp = now()

    payload = {
        "textValue": {
            "type": "Property",
            "value": data["relative_path"],
            "observedAt": timestamp
        },
        "numValue": {
            "type": "Property",
            "value": data["num_points"],
            "observedAt": timestamp
        }
    }

    patch_entity("urn:ngsi-ld:DeviceMeasurementLiDAR:002", payload)


# =========================
# RADAR
# =========================

def update_radar(data):
    timestamp = now()

    payload = {
        "numValue": {
            "type": "Property",
            "value": data["num_detections"],
            "observedAt": timestamp
        },
        "textValue": {
            "type": "Property",
            "value": data["relative_path"],
            "observedAt": timestamp
        }
    }

    patch_entity("urn:ngsi-ld:DeviceMeasurementRadar:002", payload)


# =========================
# FRAME PROCESSOR
# =========================

def process_frame(frame):
    sensors = frame.get("sensors", {})

    if "imu" in sensors:
        update_imu(sensors["imu"])

    if "gnss" in sensors:
        update_gnss(sensors["gnss"])

    if "rgb" in sensors:
        update_camera(sensors["rgb"])

    if "lidar" in sensors:
        update_lidar(sensors["lidar"])

    if "radar" in sensors:
        update_radar(sensors["radar"])


# =========================
# SIMULADOR
# =========================

def run_simulation(file_path, delay=0.5):
    with open(file_path) as f:
        data = json.load(f)

    for frame in data:
        print(f"Processing frame {frame['frame']}")
        process_frame(frame)
        time.sleep(delay)


# =========================
# START
# =========================

if __name__ == "__main__":
    run_simulation("prueba.json", delay=2)