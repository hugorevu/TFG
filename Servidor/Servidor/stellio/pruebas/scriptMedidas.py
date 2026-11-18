import requests
import time
import statistics

URL = "http://localhost:8080/ngsi-ld/v1/temporal/entities/urn:ngsi-ld:DeviceMeasurementCamera:001"

N = 1000  # número de repeticiones
latencies = []

for i in range(N):
    start = time.time()

    r = requests.get(URL, headers={
        "Accept": "application/ld+json"
    })

    end = time.time()

    if r.status_code == 200:
        latencies.append((end - start) * 1000)  # ms
    else:
        print("Error:", r.status_code)

print("Media:", statistics.mean(latencies), "ms")
print("Mediana:", statistics.median(latencies), "ms")
print("Min:", min(latencies), "ms")
print("Max:", max(latencies), "ms")