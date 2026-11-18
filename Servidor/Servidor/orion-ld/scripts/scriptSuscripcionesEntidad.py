
import requests
from config import CONTEXT, HEADERS, SUBSCRIBER_URL


SENSORS = [
    "Camera",
    "GNSS",
    "IMU",
    "LiDAR",
    "Radar"
]


def create_subscription(broker_url, entity_id):
    url = f"{broker_url}/subscriptions"

    sub = {
        "@context": CONTEXT,
        "type": "Subscription",
        "entities": [{
            "id": entity_id,
            "type": "DeviceMeasurement"
        }],
        "notification": {
            "endpoint": {
                "uri": SUBSCRIBER_URL,
                "accept": "application/json"
            }
        }
    }

    res = requests.post(
        url,
        headers=HEADERS,
        json=sub,
        timeout=15
    )

    if res.status_code == 201:
        print(f"Created subscription: {entity_id}")
    else:
        print(f"Error {entity_id}: {res.status_code} {res.text}")
        raise RuntimeError("Error creating subscription")


def create_subscriptions(broker_url, n_cars):
    print("Creating subscriptions...")

    for sensor in SENSORS:
        for i in range(1, n_cars + 1):
            entity_id = (
                f"urn:ngsi-ld:DeviceMeasurement"
                f"{sensor}:{i:03d}"
            )

            create_subscription(broker_url, entity_id)

    print("Subscriptions creation finished")
