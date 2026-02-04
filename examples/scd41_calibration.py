import time
from machine import Pin, I2C, reset
from drivers import ssd1306
from drivers import sht4x
from drivers import scd4x

print("Setting up buttons")
btn_set = Pin(42, Pin.IN, Pin.PULL_UP)
btn_save = Pin(41, Pin.IN, Pin.PULL_UP)

print("Creating I2C bus...")
i2c_bus = I2C(0, sda=Pin(45), scl=Pin(47))

print("Creating display...")
display = ssd1306.SSD1306_I2C(128, 64, i2c_bus)


def update_buffer(buffer, value, max_items=3):
    buffer.append(value)
    if len(buffer) > max_items:
        buffer.pop(0)


def average_buffer(buffer):
    result = sum(buffer) / len(buffer)
    return result


co2 = 0
t = 0
rh = 0
co2_buffer = []
t_buffer = []
rh_buffer = []
max_samples = 3
s_scd4x = scd4x.SCD4X(i2c_bus)


print("Performing sensor self-test...")
try:
    s_scd4x.self_test()
except RuntimeError:
    display.text("SCD41 self test failed!", 0, 36, 1)
    reset()
print("Self-test passed")

# print("Resetting to factory settings...")
# s_scd4x.factory_reset()
# time.sleep(1)

# print("Setting parameteters...")
# s_scd4x.stop_periodic_measurement()
# s_scd4x.altitude = 1061  # In meters
# s_scd4x.temperature_offset = 5.1  # in celcious
print(f"Altitude: {s_scd4x.altitude}")
print(f"Temp offset: {s_scd4x.temperature_offset}")

# print("Persisting settings")
# s_scd4x.persist_settings()
# time.sleep(1)

print("Start measuring")
s_scd4x.start_periodic_measurement()

while True:
    if btn_set.value() == 0:
        s_scd4x.force_calibration(426)

    if btn_save.value() == 0:
        s_scd4x.persist_settings()

    if s_scd4x.data_ready:
        print("Data ready")
        update_buffer(co2_buffer, s_scd4x.CO2)
        print(f"CO2 Samples: {co2_buffer}")
        co2 = average_buffer(co2_buffer)
        print(f"Average CO2: {co2}")

        update_buffer(t_buffer, s_scd4x.temperature)
        print(f"T Samples: {t_buffer}")
        t = average_buffer(t_buffer)
        print(f"Average T: {t}")

        update_buffer(rh_buffer, s_scd4x.relative_humidity)
        print(f"RH Samples: {rh_buffer}")
        rh = average_buffer(rh_buffer)
        print(f"Average RH: {rh}")

    display.fill(0)
    display.text(f"T:{t:.1f}C RH:{rh:.1f}%", 0, 12, 1)
    display.text(f"CO2:{co2:.1f}ppm", 0, 24, 1)
    display.show()
    time.sleep(1)
