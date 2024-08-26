from machine import Pin
import time

led = Pin(4, Pin.OUT)

# 常亮
led.value(1)

# for i in range(3):
#     led.value(1)
#     time.sleep(0.2)
#     led.value(0)
#     time.sleep(0.2)