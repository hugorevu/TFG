@echo off

echo Deleting Platform...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:Vehicle001

echo Deleting CameraRGB...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:CameraRGB:001

echo Deleting FrameObservableProperty...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:FrameObservableProperty:001

echo Deleting FrameResult...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:FrameResult:001

echo Deleting FrameObservation...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:FrameObservation:001

echo Deleting GNSS...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:GNSS:001

echo Deleting GNSSObservableProperty...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:GNSSObservableProperty:001

echo Deleting GNSSResult...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:GNSSResult:001

echo Deleting GNSSObservation...
curl -X DELETE http://localhost:9090/ngsi-ld/v1/entities/urn:ngsi-ld:GNSSObservation:001

echo Done.
pause