@echo off

echo Creating Platform...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @platform.json

echo Creating CameraRGB...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @camera.json

echo Creating FrameObservableProperty...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameObservableProperty.json

echo Creating FrameResult...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameResult.json

echo Creating FrameObservation...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameObservation.json

echo Creating GNSS...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @gnss.json

echo Creating GNSSObservableProperty...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @gnssObservableProperty.json

echo Creating GNSSResult...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @gnssResult.json

echo Creating GNSSObservation...
curl -X POST http://localhost:9090/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @gnssObservation.json

echo Done.
pause