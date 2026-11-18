import requests
from datetime import datetime, timezone
from config import CONTEXT, HEADERS

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
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
        "@context": CONTEXT
    }


def create_devices(broker_url, n_cars):

    url = f"{broker_url}/entities"

    print("Creating Device entities...")

    for i in range(1, n_cars + 1):

        entities = [
            create_entity1(i),  # Camera
            create_entity2(i),  # GNSS
            create_entity3(i),  # IMU
            create_entity4(i),  # LiDAR
            create_entity5(i)   # Radar
        ]

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
                print(
                    f"Error {entity['id']}: "
                    f"{r.status_code} {r.text}"
                )
                raise RuntimeError("Error creating Device")

        print(f"Device {i:03d} completed")

    print("Device creation finished")
