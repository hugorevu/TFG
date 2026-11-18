import requests

BROKER = "http://172.31.232.59:1026/ngsi-ld/v1/subscriptions"

# Obtener todas
res = requests.get(BROKER, headers={"Accept": "application/ld+json"})
subs = res.json()

# Borrar todas
for sub in subs:
    sub_id = sub["id"]
    delete_url = f"{BROKER}/{sub_id}"
    r = requests.delete(delete_url)
    print(f"{sub_id} -> {r.status_code}")
