@echo off

echo Deleting Platform...
curl -X DELETE http://localhost:8080/ngsi-ld/v1/entities/urn:ngsi-ld:Vehicle001

echo Deleting CameraRGB...
curl -X DELETE http://localhost:8080/ngsi-ld/v1/entities/urn:ngsi-ld:CameraRGB:001

echo Deleting FrameObservableProperty...
curl -X DELETE http://localhost:8080/ngsi-ld/v1/entities/urn:ngsi-ld:FrameObservableProperty:001

echo Deleting FrameResult...
curl -X DELETE http://localhost:8080/ngsi-ld/v1/entities/urn:ngsi-ld:FrameResult:001

echo Deleting FrameObservation...
curl -X DELETE http://localhost:8080/ngsi-ld/v1/entities/urn:ngsi-ld:FrameObservation:001

echo Done.
pause