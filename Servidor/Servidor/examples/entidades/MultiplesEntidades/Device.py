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
    return{
        "id": f"urn:ngsi-ld:DeviceCamera:{i:03d}",
        "type": "Device",
        "controlledProperty": {
            "type": "Property",
            "value": ["image"]
        },
        "batteryLevel": {  
            "type": "Property",  
            "value": 0.75  
        },
        "dateCreated": {
            "type": "Property",
            "value": now()
        },
        "deviceCategory": {
            "type": "Property",
            "value": ["sensor"]
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "refDeviceModel": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:DeviceModel:CameraModelX"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

def create_entity2(i):
    return{
        "id": f"urn:ngsi-ld:DeviceGNSS:{i:03d}",
        "type": "Device",
        "controlledProperty": {
            "type": "Property",
            "value": ["location"]
        },
        "batteryLevel": {  
            "type": "Property",  
            "value": 0.75  
        },
        "dateCreated": {
            "type": "Property",
            "value": now()
        },
        "deviceCategory": {
            "type": "Property",
            "value": ["sensor"]
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "refDeviceModel": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:DeviceModel:GNSSModelX"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

def create_entity3(i):
    return{
        "id": f"urn:ngsi-ld:DeviceIMU:{i:03d}",
        "type": "Device",
        "controlledProperty": {
            "type": "Property",
            "value": ["acceleration"]
        },
        "batteryLevel": {  
            "type": "Property",  
            "value": 0.75  
        },
        "dateCreated": {
            "type": "Property",
            "value": now()
        },
        "deviceCategory": {
            "type": "Property",
            "value": ["sensor"]
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "refDeviceModel": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:DeviceModel:IMUModelX"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

def create_entity4(i):
    return{
        "id": f"urn:ngsi-ld:DeviceLiDAR:{i:03d}",
        "type": "Device",
        "controlledProperty": {
            "type": "Property",
            "value": ["distance"]
        },
        "batteryLevel": {  
            "type": "Property",  
            "value": 0.75  
        },
        "dateCreated": {
            "type": "Property",
            "value": now()
        },
        "deviceCategory": {
            "type": "Property",
            "value": ["sensor"]
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "refDeviceModel": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:DeviceModel:LiDARModelX"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

def create_entity5(i):
    return{
        "id": f"urn:ngsi-ld:DeviceRadar:{i:03d}",
        "type": "Device",
        "controlledProperty": {
            "type": "Property",
            "value": ["distance"]
        },
        "batteryLevel": {  
            "type": "Property",  
            "value": 0.75  
        },
        "dateCreated": {
            "type": "Property",
            "value": now()
        },
        "deviceCategory": {
            "type": "Property",
            "value": ["sensor"]
        },
        "refVehicle": {
            "type": "Relationship",
            "object": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}"
        },
        "refDeviceModel": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:DeviceModel:RadarModelX"
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


print("Done")   