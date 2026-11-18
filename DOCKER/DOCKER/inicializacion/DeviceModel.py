import requests
from config import CONTEXT, HEADERS

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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
    }


def create_device_models(broker_url):

    url = f"{broker_url}/entities"

    entities = [
        create_entity1(),
        create_entity2(),
        create_entity3(),
        create_entity4(),
        create_entity5()
    ]

    print("Creating DeviceModel entities...")

    for entity in entities:

        r = requests.post(
            url,
            headers=HEADERS,
            json=entity,
            timeout=15
        )

        if r.status_code == 201:
            print(f"Created {entity['id']}")

        elif r.status_code == 409:
            print(f"Already exists {entity['id']}")

        else:
            print(f"Error {entity['id']}: {r.status_code} {r.text}")
            raise RuntimeError("Error creating DeviceModel")

    print("DeviceModel creation finished")

