import subprocess
import sys
from pathlib import Path

# Directorio donde está este script
BASE_DIR = Path(__file__).resolve().parent

# Carpetas de cada Context Broker
BROKERS = {
    "orion": "orion-test",
    "scorpio": "scorpio",
    "stellio": "stellio-context-broker"
}


def gestionar_broker(broker, accion):

    if broker not in BROKERS:
        print(f"Broker no válido: {broker}")
        print(f"Disponibles: {', '.join(BROKERS)}")
        return

    carpeta = BASE_DIR / BROKERS[broker]

    if not carpeta.exists():
        print(f"No existe la carpeta: {carpeta}")
        return

    if accion == "start":
        comando = ["docker", "compose", "up", "-d"]

    elif accion == "stop":
        comando = ["docker", "compose", "down"]

    elif accion == "delete":
        comando = ["docker", "compose", "down", "-v"]

    elif accion == "restart":
        comando = ["docker", "compose", "restart"]

    else:
        print(f"Acción no válida: {accion}")
        print("Acciones: start, stop, delete, restart")
        return

    print(f"\nBroker: {broker}")
    print(f"Acción: {accion}\n")

    subprocess.run(
        comando,
        cwd=carpeta,
        check=True
    )


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Uso: python gestionar_brokers.py <broker> <accion>")
        sys.exit(1)

    broker = sys.argv[1].lower()
    accion = sys.argv[2].lower()

    gestionar_broker(broker, accion)