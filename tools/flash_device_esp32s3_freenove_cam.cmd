SET FMW=%CD%\firmware\ESP32S3_FREENOVE_CAM\firmware.bin
esptool erase-flash
esptool write-flash 0 %FMW%
