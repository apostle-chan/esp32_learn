from machine import Pin
import time

a = Pin(15, Pin.OUT)
b = Pin(2, Pin.OUT)
c = Pin(4, Pin.OUT)
d = Pin(16, Pin.OUT)

# 初始化
a.value(0)
b.value(0)
c.value(0)
d.value(0)

# 延时时间
delay_time_ms = 2

while True:
    # 单拍工作方式
    a.value(1)
    b.value(0)
    c.value(0)
    d.value(0)
    time.sleep_ms(delay_time_ms)

    a.value(0)
    b.value(1)
    c.value(0)
    d.value(0)
    time.sleep_ms(delay_time_ms)

    a.value(0)
    b.value(0)
    c.value(1)
    d.value(0)
    time.sleep_ms(delay_time_ms)

    a.value(0)
    b.value(0)
    c.value(0)
    d.value(1)
    time.sleep_ms(delay_time_ms)
