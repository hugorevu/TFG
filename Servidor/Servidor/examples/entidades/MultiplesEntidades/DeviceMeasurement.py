import requests
import json
import time
import uuid
from datetime import datetime, timezone

URL = "http://localhost:8080/ngsi-ld/v1/entities"

HEADERS = {
    "Content-Type": "application/ld+json"
}

def now():
    return datetime.utcnow().isoformat() + "Z"

def create_entity1(i):
    return {
        "id": f"urn:ngsi-ld:DeviceMeasurementCamera:{i:03d}",
        "type": "DeviceMeasurement",
        "controlledProperty": {
            "type": "Property",
            "value": "image"
        },
        "textValue": {
            "type": "Property",
            "value": "http://example.org/frame001.jpg"
        },
        "refDevice": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:DeviceCamera:{i:03d}"
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "dateObserved": {
            "type": "Property",
            "value": now()
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity2(i):
    return {
        "id": f"urn:ngsi-ld:DeviceMeasurementGNSS:{i:03d}",
        "type": "DeviceMeasurement",
        "controlledProperty": {
            "type": "Property",
            "value": "location"
        },
        "location": {
            "type": "GeoProperty",
            "value": {
            "type": "Point",
            "coordinates": [-3.7038, 40.4168]
            }
        },
        "refDevice": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:DeviceGNSS:{i:03d}"
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "dateObserved": {
            "type": "Property",
            "value": now()
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity3(i):
    return {
        "id": f"urn:ngsi-ld:DeviceMeasurementIMU:{i:03d}",
        "type": "DeviceMeasurement",
        "controlledProperty": {
            "type": "Property",
            "value": "acceleration"
        },
        "textValue": {
            "type": "Property",
            "value": {
            "accelerometer": {
                "x": -3069.94,
                "y": -43945.47,
                "z": -314.52
            },
            "gyroscope": {
                "x": -4.19e-08,
                "y": 2.43e-07,
                "z": -4.69e-11
            },
            "compass": 0.0068
            }
        },
        "refDevice": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:DeviceIMU:{i:03d}"
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "dateObserved": {
            "type": "Property",
            "value": now()
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity4(i):
    return {
        "id": f"urn:ngsi-ld:DeviceMeasurementLiDAR:{i:03d}",
        "type": "DeviceMeasurement",
        "controlledProperty": {
            "type": "Property",
            "value": "distance"
        },
        "textValue": {
            "type": "Property",
            "value": "lidar_clouds/043836.ply"
        },
        "numValue": {
            "type": "Property",
            "value": 734
        },
        "refDevice": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:DeviceLiDAR:{i:03d}"
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "dateObserved": {
            "type": "Property",
            "value": now()
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity5(i):
    return {
        "id": f"urn:ngsi-ld:DeviceMeasurementRadar:{i:03d}",
        "type": "DeviceMeasurement",
        "controlledProperty": {
            "type": "Property",
            "value": "distance"
        },
        "textValue": {
            "type": "Property",
            "value": "radar_scan/043836.bin"
        },
        "numValue": {
            "type": "Property",
            "value": 75
        },
        "refDevice": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:DeviceRadar:{i:03d}"
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "dateObserved": {
            "type": "Property",
            "value": now()
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

N = 10

print("Inserting entities...")

for i in range(N):

    entities = [
        create_entity1(i),  # Camera
        create_entity2(i),  # GNSS
        create_entity3(i),  # IMU
        create_entity4(i),  # LiDAR
        create_entity5(i)   # Radar
    ]

    for entity in entities:

        r = requests.post(URL, headers=HEADERS, data=json.dumps(entity))

        if r.status_code == 201:
            print(f"Created {entity['id']}")
        elif r.status_code == 409:
            print(f"Already exists {entity['id']}")
        else:
            print("Error:", r.status_code, r.text)

    print(f"DeviceMeasurement {i:03d} completed")

print("Done") 