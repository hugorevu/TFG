@echo off

echo Creating AutonomousVehicle...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @autonomousVehicle.json

echo Creating Device for Camera...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceCamera.json

echo Creating DeviceModel for Camera...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelCamera.json

echo Creating Measurement for Camera...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementCamera.json

echo Creating Device for GNSS...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceGNSS.json

echo Creating DeviceModel for GNSS...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelGNSS.json

echo Creating Measurement for GNSS...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementGNSS.json

echo Creating Device for IMU...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceIMU.json

echo Creating DeviceModel for IMU...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelIMU.json

echo Creating Measurement for IMU...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementIMU.json

echo Creating Device for LiDAR...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceLiDAR.json

echo Creating DeviceModel for LiDAR...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelLiDAR.json

echo Creating Measurement for LiDAR...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementLiDAR.json

echo Creating Device for Radar...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceRadar.json

echo Creating DeviceModel for Radar...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceModelRadar.json

echo Creating Measurement for Radar...
curl -X POST http://localhost:1026/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @deviceMeasurementRadar.json

echo Done.
pause