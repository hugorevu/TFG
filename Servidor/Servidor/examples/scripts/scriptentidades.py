import requests

BASE_URL = "http://localhost:8080/ngsi-ld/v1/entities"

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

sensors = [
    "Camera",
    "GNSS",
    "IMU",
    "LiDAR",
    "Radar"
]

for vehicle_id in range(1, 4):

    # =========================
    # CREATE VEHICLE
    # =========================

    vehicle = {
        "id": f"urn:ngsi-ld:AutonomousVehicle:{vehicle_id:03}",
        "type": "AutonomousVehicle",
        "saeLevel": {
            "type": "Property",
            "value": 4
        },
        "@context": CONTEXT
    }

    requests.post(BASE_URL, json=vehicle, headers=HEADERS)

    print(f"Vehicle {vehicle_id} created")

    # =========================
    # CREATE SENSORS
    # =========================

    for sensor in sensors:

        device = {
            "id": f"urn:ngsi-ld:Device:{sensor}{vehicle_id:03}",
            "type": "Device",
            "controlledProperty": {
                "type": "Property",
                "value": [sensor.lower()]
            },
            "deviceCategory": {
                "type": "Property",
                "value": ["sensor"]
            },
            "batteryLevel": {
                "type": "Property",
                "value": 0.95
            },
            "refVehicle": {
                "type": "Relationship",
                "object": f"urn:ngsi-ld:AutonomousVehicle:{vehicle_id:03}"
            },
            "@context": CONTEXT
        }

        requests.post(BASE_URL, json=device, headers=HEADERS)

        print(f"{sensor} device created")

        # =========================
        # CREATE MEASUREMENT
        # =========================

        measurement = {
            "id": f"urn:ngsi-ld:DeviceMeasurement:{sensor}{vehicle_id:03}",
            "type": "DeviceMeasurement",
            "controlledProperty": {
                "type": "Property",
                "value": sensor.lower()
            },
            "refDevice": {
                "type": "Relationship",
                "object": f"urn:ngsi-ld:Device:{sensor}{vehicle_id:03}"
            },
            "refVehicle": {
                "type": "Relationship",
                "object": f"urn:ngsi-ld:AutonomousVehicle:{vehicle_id:03}"
            },
            "@context": CONTEXT
        }

        requests.post(BASE_URL, json=measurement, headers=HEADERS)

        print(f"{sensor} measurement created")