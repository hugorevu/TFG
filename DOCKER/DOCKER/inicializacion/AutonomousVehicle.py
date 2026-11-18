
import requests
from datetime import datetime, timezone
from config import CONTEXT, HEADERS


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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
        "@context": CONTEXT
    }


def create_vehicles(broker_url, n_cars):
    url = f"{broker_url}/entities"

    print("Creating AutonomousVehicle entities...")

    for i in range(1, n_cars + 1):
        entity = create_entity(i)

        try:
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
                raise RuntimeError("Error creating entity")

        except requests.RequestException as e:
            print(f"Connection error: {e}")
            raise

    print("AutonomousVehicle creation finished")
