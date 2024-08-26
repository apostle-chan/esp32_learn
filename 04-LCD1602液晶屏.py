from machine import Pin, SoftI2C


i2c = SoftI2C(scl=Pin(15), sda=Pin(2), freq=100000)
i2c.scan()

