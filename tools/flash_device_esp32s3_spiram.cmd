SET FMW=%CD%\firmware\ESP32_FERMENTO_S3-SPIRAM_OCT\firmware.bin
esptool --baud 460800 write-flash 0 %FMW%
