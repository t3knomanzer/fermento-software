SET FMW=%CD%\firmware\firmware.bin
esptool --baud 460800 write_flash 0x1000 %FMW%
