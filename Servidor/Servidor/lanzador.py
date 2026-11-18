
import subprocess
import sys
from pathlib import Path

# =========================
# CONFIGURACIÓN
# =========================

N_VEHICLES = 20
DELAY = 0.5
BROKER = "stellio"

SCRIPT = Path(__file__).resolve().parent / "Simulador.py"

# =========================
# LANZAR SIMULADORES
# =========================

procesos = []

for i in range(1, N_VEHICLES + 1):

    vehicle_id = f"{i:03d}"

    print(f"Lanzando vehículo {vehicle_id}...")

    proceso = subprocess.Popen([
        sys.executable,
        str(SCRIPT),
        vehicle_id,
        str(DELAY),
        BROKER
    ])

    procesos.append(proceso)

print(f"\n{N_VEHICLES} simuladores lanzados.")
print("Esperando a que terminen...")

for proceso in procesos:
    proceso.wait()

print("\nTodos los simuladores han terminado.")
