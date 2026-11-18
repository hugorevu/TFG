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

def create_entity(i):
    return {
        "id": f"urn:ngsi-ld:AutonomousVehicle:{i:03d}",
        "type": "AutonomousVehicle",
        "saeLevel": {
            "type": "Property",
            "value": 3
        },
        "dateCreated": {
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
    entity = create_entity(i)

    r = requests.post(URL, headers=HEADERS, data=json.dumps(entity))

    if r.status_code == 201:
        print(f"Created {entity['id']}")
    elif r.status_code == 409:
        print(f"Already exists {entity['id']}")
    else:
        print("Error:", r.status_code, r.text)


print("Done")