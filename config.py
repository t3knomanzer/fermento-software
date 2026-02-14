import app.services.log.log as log

# Logging configuration
LOG_LEVEL = log.INFO
LOG_MAX_FILES = 3

# Network configuration
MQTT_SERVER = "13.50.219.203"
# MQTT_SERVER = "192.168.8.5"
MQTT_PORT = 1883

WIFI_AP_SSID = "Fermento"
WIFI_AP_PASSWORD = "123456789"

# UI configuration
MEASURE_MAX_CHOICES = 3
TRACK_MAX_CHOICES = 2

# Sensor configuration
I2C_0_ID = 0
I2C_0_SCL_PIN = 1
I2C_0_SDA_PIN = 2

INPUT_NXT_PIN = 39
INPUT_SEL_PIN = 40
INPUT_PRE_PIN = None
INPUT_INC_PIN = None
INPUT_DEC_PIN = None

SENSOR_DISTANCE_TIMING_BUDGET = 200

# ========================
# Camera resolutions:
# ========================
# R240X240 = 5
# XGA = 12
# R320X320 = 7
# QVGA = 6
# R128x128 = 2
# QXGA = 19
# VGA = 10
# R96X96 = 0
# WQXGA = 21
# SVGA = 11
# UXGA = 15
# SXGA = 14
# HQVGA = 4
# QSXGA = 23
# HVGA = 9
# CIF = 8
# HD = 13
# FHD = 16
# QHD = 20
# P_3MP = 18
# QQVGA = 1
# P_FHD = 22
# QCIF = 3
# P_HD = 17

CAMERA_FRAME_SIZE = 6  # QVGA

# ========================
# Camera pixel formats:
# ========================
# RGB555 = 8
# RGB565 = 0
# RGB888 = 5
# YUV420 = 2
# YUV422 = 1
# RGB444 = 7
# GRAYSCALE = 3
# JPEG = 4
# RAW = 6

CAMERA_PIXEL_FORMAT = 4  # JPEG
CAMERA_JPEG_QUALITY = 85
CAMERA_FB_COUNT = 1
