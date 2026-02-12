import time
from machine import Pin, I2C
from drivers import ssd1306
from drivers import sht4x
from drivers import scd4x


def update_buffer(buffer, value, max_items=3):
    buffer.append(value)
    if len(buffer) > max_items:
        buffer.pop(0)


def average_buffer(buffer):
    result = sum(buffer) / len(buffer)
    return result


print("Creating I2C bus...")
i2c_bus = I2C(0, sda=Pin(5), scl=Pin(6))

print("Creating sensors...")
s_sht41 = sht4x.SHT4x(i2c_bus)
s_sht41.reset()
s_sht41.mode = sht4x.Mode.NOHEAT_HIGHPRECISION
time.sleep_ms(1)

t_buffer = []
rh_buffer = []
max_samples = 3
t = 0
rh = 0
t_offset = -0.5

while True:
    t, rh = s_sht41.measurements
    update_buffer(t_buffer, t, max_samples)
    t = average_buffer(t_buffer) + t_offset
    update_buffer(rh_buffer, rh, max_samples)
    rh = average_buffer(rh_buffer)
    print(f"T:{t} RH:{rh}")
    time.sleep(1)
