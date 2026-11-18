import requests

BROKER = "http://localhost:8080/ngsi-ld/v1/subscriptions"

HEADERS = {
    "Content-Type": "application/ld+json"
}

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

def create_subscription(entity_id, attribute):
    sub = {
        "@context": CONTEXT,
        "type": "Subscription",
        "entities": [{
            "id": entity_id,
            "type": "DeviceMeasurement"
        }],
        "watchedAttributes": [attribute],
        "notification": {
            "attributes": [attribute],
            "endpoint": {
                "uri": "http://host.docker.internal:5001/notify",
                "accept": "application/json"
            }
        }
    }

    res = requests.post(BROKER, headers=HEADERS, json=sub)

    print(f"{entity_id} -> {attribute}: {res.status_code}")
    if res.status_code not in [201]:
        print(res.text)


# =========================
# CREAR TODAS
# =========================

create_subscription("urn:ngsi-ld:DeviceMeasurementCamera:002", "textValue")
create_subscription("urn:ngsi-ld:DeviceMeasurementGNSS:002", "location")
create_subscription("urn:ngsi-ld:DeviceMeasurementIMU:002", "textValue")
create_subscription("urn:ngsi-ld:DeviceMeasurementLiDAR:002", "textValue")
create_subscription("urn:ngsi-ld:DeviceMeasurementLiDAR:002", "numValue")
create_subscription("urn:ngsi-ld:DeviceMeasurementRadar:002", "numValue")
create_subscription("urn:ngsi-ld:DeviceMeasurementRadar:002", "textValue")