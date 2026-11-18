
# ==========================================
# CONFIGURACIÓN DE CONTEXT BROKERS
# ==========================================

#SERVER_IP = "172.31.232.59"
SERVER_IP = "localhost"

BROKERS = {
    "orion": 1026,
    "scorpio": 9090,
    "stellio": 8080
}

# ==========================================
# CONTEXTO NGSI-LD
# ==========================================

CONTEXT = [
    "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "https://cdn.jsdelivr.net/gh/hugorevu/dataModel.AutonomousVehicle@cbd61d0/FIWARE_DEVICE_MODEL/examples/datamodels.context-ngsi.jsonld"
]

HEADERS = {
    "Content-Type": "application/ld+json"
}

# ==========================================
# CONFIGURACIÓN DE SUSCRIPCIONES
# ==========================================

#array de suscripciones 

SUBSCRIBER_IP = "host.docker.internal"
#SUBSCRIBER_IP = "172.31.232.59"
SUBSCRIBER_PORTS = [
    #5001,
    5002,
    5003,
    5004,
    5005,
    5006
]

SUBSCRIBER_URLS = [
    f"http://{SUBSCRIBER_IP}:{port}/notify"
    for port in SUBSCRIBER_PORTS
]

# ==========================================
# FUNCIONES
# ==========================================

def get_broker_url(broker):
    broker = broker.lower()

    if broker not in BROKERS:
        raise ValueError(
            f"Context Broker desconocido: {broker}"
        )

    port = BROKERS[broker]

    return f"http://localhost:{port}/ngsi-ld/v1"

    #return f"http://{SERVER_IP}:{port}/ngsi-ld/v1"