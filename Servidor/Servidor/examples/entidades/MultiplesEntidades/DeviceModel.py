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

def create_entity1():
    return {
        "id": "urn:ngsi-ld:DeviceModel:CameraModelX",
        "type": "DeviceModel",
        "category": {
            "type": "Property",
            "value": ["sensor"]
        },
        "controlledProperty": {
            "type": "Property",
            "value": ["image"]
        },
        "manufacturerName": {
            "type": "Property",
            "value": "Bosch"
        },
        "brandName": {
            "type": "Property",
            "value": "Bosch"
        },
        "modelName": {
            "type": "Property",
            "value": "X1000"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity2():
    return {
        "id": "urn:ngsi-ld:DeviceModel:GNSSModelX",
        "type": "DeviceModel",
        "category": {
            "type": "Property",
            "value": ["sensor"]
        },
        "controlledProperty": {
            "type": "Property",
            "value": ["location"]
        },
        "manufacturerName": {
            "type": "Property",
            "value": "Bosch"
        },
        "brandName": {
            "type": "Property",
            "value": "Bosch"
        },
        "modelName": {
            "type": "Property",
            "value": "X1000"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity3():
    return {
        "id": "urn:ngsi-ld:DeviceModel:IMUModelX",
        "type": "DeviceModel",
        "category": {
            "type": "Property",
            "value": ["sensor"]
        },
        "controlledProperty": {
            "type": "Property",
            "value": ["acceleration"]
        },
        "manufacturerName": {
            "type": "Property",
            "value": "Bosch"
        },
        "brandName": {
            "type": "Property",
            "value": "Bosch"
        },
        "modelName": {
            "type": "Property",
            "value": "X1000"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity4():
    return {
        "id": "urn:ngsi-ld:DeviceModel:LiDARModelX",
        "type": "DeviceModel",
        "category": {
            "type": "Property",
            "value": ["sensor"]
        },
        "controlledProperty": {
            "type": "Property",
            "value": ["distance"]
        },
        "manufacturerName": {
            "type": "Property",
            "value": "Bosch"
        },
        "brandName": {
            "type": "Property",
            "value": "Bosch"
        },
        "modelName": {
            "type": "Property",
            "value": "X1000"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }
def create_entity5():
    return {
        "id": "urn:ngsi-ld:DeviceModel:RadarModelX",
        "type": "DeviceModel",
        "category": {
            "type": "Property",
            "value": ["sensor"]
        },
        "controlledProperty": {
            "type": "Property",
            "value": ["distance"]
        },
        "manufacturerName": {
            "type": "Property",
            "value": "Bosch"
        },
        "brandName": {
            "type": "Property",
            "value": "Bosch"
        },
        "modelName": {
            "type": "Property",
            "value": "X1000"
        },
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
        ]
    }

entities = [
    create_entity1(),
    create_entity2(),
    create_entity3(),
    create_entity4(),
    create_entity5()
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
