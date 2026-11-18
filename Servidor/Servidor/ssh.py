import subprocess
from pathlib import Path

Pcs = [
    "usuariouc@172.31.232.60",
    "usuariouc@172.31.232.68",
    "usuariouc@172.31.232.66",
    "usuariouc@172.31.232.69",
    "usuariouc@172.31.232.61",
]

DELAYS = [0.5, 0.2, 0.1]
BROKERS = ["orion", "scorpio", "stellio"]

REMOTE_PATH = "/home/usuariouc/Escritorio/Fiware"

# El simulador está en la misma carpeta que este script
LOCAL_FILE = Path(__file__).resolve().parent / "Simulador.py"


# =========================
# ACTUALIZAR SIMULADORES
# =========================

def actualizar_simuladores():
    print("Actualizando simuladores...")

    for pc in Pcs:
        print(f"Copiando simulador a {pc}...")

        subprocess.run([
            "scp",
            str(LOCAL_FILE),
            f"{pc}:{REMOTE_PATH}/Simulador.py"
        ], check=True)

    print("Todos los simuladores actualizados.")


# =========================
# DISTRIBUIR VEHÍCULOS
# =========================

def split_cars(n_cars, n_pcs):
    cars = [f"{i:03d}" for i in range(1, n_cars + 1)]
    return [cars[i::n_pcs] for i in range(n_pcs)]


# =========================
# EJECUTAR EXPERIMENTO
# =========================

def run_experiment(n_cars, delay, broker):
    groups = split_cars(n_cars, len(Pcs))

    for pc, group in zip(Pcs, groups):
        for car in group:

            cmd = (
                f'ssh {pc} '
                f'"cd {REMOTE_PATH} '
                f'&& ./venv/bin/python scriptSimuladorGrande.py {car} {delay} {broker}"'
            )

            subprocess.Popen(cmd, shell=True)


# =========================
# CONFIGURACIÓN EXPERIMENTO
# =========================

n_cars = int(input("Número de vehículos: "))
delay = float(input("Delay (0.5, 0.2, 0.1): "))
broker = input("Context Broker (orion, scorpio, stellio): ").lower().strip()

if n_cars <= 0:
    raise ValueError("El número de vehículos debe ser positivo")

if delay not in DELAYS:
    raise ValueError(f"Delay no válido. Opciones: {DELAYS}")

if broker not in BROKERS:
    raise ValueError(f"Broker no válido. Opciones: {BROKERS}")

# Primero actualizamos los 5 ordenadores
actualizar_simuladores()

# Después lanzamos los vehículos
run_experiment(n_cars, delay, broker)
