
import requests
from config import CONTEXT, HEADERS, SUBSCRIBER_URLS
from urllib.parse import quote


SENSORS = [
    "Camera",
    "GNSS",
    "IMU",
    "LiDAR",
    "Radar"
]


def create_subscription(broker_url, entity_id, subscriber_url):
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
                "uri": subscriber_url,
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
        print(f"Created subscription: {entity_id} -> {subscriber_url}")
    else:
        print(f"Error {entity_id}: {res.status_code} {res.text}")
        raise RuntimeError("Error creating subscription")


def create_subscriptions(broker_url, n_cars, n_subscribers=1):
    print("Creating subscriptions...")

    if n_subscribers not in [1,2,3,4,5]:
        raise ValueError("Only 1 or 5 subscribers allowed")

    for sensor in SENSORS:
        for i in range(1, n_cars + 1):
            entity_id = (
                f"urn:ngsi-ld:DeviceMeasurement"
                f"{sensor}:{i:03d}"
            )

            for subscriber_url in SUBSCRIBER_URLS[:n_subscribers]:
                create_subscription(
                    broker_url,
                    entity_id,
                    subscriber_url
                )

    print("Subscriptions creation finished")

# def create_subscriptions(broker_url, n_cars, n_subscribers=1):
#     print("Creating subscriptions...")

#     for sensor in SENSORS:
#         for i in range(1, 4):  # Vehículos 001, 002 y 003

#             entity_id = (
#                 f"urn:ngsi-ld:DeviceMeasurement"
#                 f"{sensor}:{i:03d}"
#             )

#             create_subscription(
#                 broker_url,
#                 entity_id,
#                 SUBSCRIBER_URLS[0]
#             )

#     print("Subscriptions creation finished")

# def create_subscriptions(broker_url, n_cars, n_subscribers=1):
#     print("Creating one subscription...")

#     entity_id = "urn:ngsi-ld:DeviceMeasurementGNSS:001"

#     create_subscription(
#         broker_url,
#         entity_id,
#         SUBSCRIBER_URLS[0]
#     )

#    print("Subscription creation finished")

def delete_subscriptions(broker_url):

    url = f"{broker_url}/subscriptions"

    print("Deleting subscriptions...")

    total_deleted = 0

    while True:

        # Recuperar una página de suscripciones
        res = requests.get(
            url,
            headers={"Accept": "application/ld+json"},
            params={"limit": 100},
            timeout=15
        )

        if res.status_code != 200:
            raise RuntimeError(
                f"Error getting subscriptions: "
                f"{res.status_code} {res.text}"
            )

        subs = res.json()

        # Si no quedan suscripciones, terminar
        if not subs:
            break

        # Eliminar todas las de esta página
        for sub in subs:

            sub_id = sub["id"]

            delete_url = f"{url}/{quote(sub_id, safe='')}"

            r = requests.delete(
                delete_url,
                timeout=15
            )

            if r.status_code == 204:
                total_deleted += 1
                print(f"Deleted {sub_id}")
            else:
                raise RuntimeError(
                    f"Error deleting {sub_id}: "
                    f"{r.status_code} {r.text}"
                )

    print(f"Subscriptions deletion finished: {total_deleted} deleted")
