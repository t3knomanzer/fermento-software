SET FMW=%CD%\firmware\ESP32_FERMENTO_S3_CAM_SPIRAM_OCT\firmware.bin
esptool erase-flash
esptool write-flash 0 %FMW%
