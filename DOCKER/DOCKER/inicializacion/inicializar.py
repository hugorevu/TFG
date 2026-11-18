
import argparse

from config import get_broker_url
from AutonomousVehicle import create_vehicles
from DeviceModel import create_device_models
from Device import create_devices
from DeviceMeasurement import create_device_measurements
from Subscriptions import create_subscriptions
from Subscriptions import delete_subscriptions


def main():

    # Argumentos de ejecución
    parser = argparse.ArgumentParser(
        description="Inicialización de entidades y suscripciones NGSI-LD"
    )

    parser.add_argument(
        "--broker",
        choices=["orion", "scorpio", "stellio"],
        required=True,
        help="Context Broker que se utilizará"
    )

    parser.add_argument(
        "--cars",
        type=int,
        default=50,
        help="Número de vehículos (por defecto 50)"
    )

    parser.add_argument(
        "--subscribers",
        type=int,
        choices=[1,2,3,4,5],
        default=1,
        help="Número de suscriptores: 1 o 5 (por defecto 1)"
    )

    parser.add_argument(
        "--reset-subscriptions",
        action="store_true",
        help="Eliminar las suscripciones anteriores antes de crear las nuevas"
    )

    args = parser.parse_args()

    if args.cars < 1:
        parser.error("El número de vehículos debe ser mayor que cero")

    # Obtener URL del broker
    broker_url = get_broker_url(args.broker)

    print(f"\nInitializing {args.broker}")
    print(f"Broker URL: {broker_url}")
    print(f"Vehicles: {args.cars}\n")
    print(f"Subscribers: {args.subscribers}\n")

    # 1. Crear vehículos
    create_vehicles(broker_url, args.cars)

    # 2. Crear modelos de dispositivos
    create_device_models(broker_url)

    # 3. Crear dispositivos
    create_devices(broker_url, args.cars)

    # 4. Crear mediciones
    create_device_measurements(broker_url, args.cars)

    # 5. Eliminar suscripciones anteriores (opcional)
    if args.reset_subscriptions:
        delete_subscriptions(broker_url)

    # 6. Crear suscripciones
    create_subscriptions(broker_url, args.cars, args.subscribers)

    # py inicializar.py --broker orion --cars 50 --subscribers 1

    print("\nInitialization finished")


if __name__ == "__main__":
    main()
