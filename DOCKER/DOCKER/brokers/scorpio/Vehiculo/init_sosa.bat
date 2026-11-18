@echo off

echo Creating Platform...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @platform.json

echo Creating CameraRGB...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @camera.json

echo Creating FrameObservableProperty...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameObservableProperty.json

echo Creating FrameResult...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameResult.json

echo Creating FrameObservation...
curl -X POST http://localhost:8080/ngsi-ld/v1/entities ^
-H "Content-Type: application/ld+json" ^
-d @frameObservation.json

echo Done.
pause