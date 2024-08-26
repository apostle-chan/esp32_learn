from machine import Pin
import time

# 定义引脚对应数码管col的位置
row_8 = Pin(13, Pin.OUT)
row_7 = Pin(12, Pin.OUT)
row_6 = Pin(14, Pin.OUT)
row_5 = Pin(27, Pin.OUT)
row_4 = Pin(26, Pin.OUT)
row_3 = Pin(25, Pin.OUT)
row_2 = Pin(33, Pin.OUT)
row_1 = Pin(32, Pin.OUT)

row_list = [row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8]

# 定义引脚对应数码管col的位置
col_8 = Pin(15, Pin.OUT)
col_7 = Pin(2, Pin.OUT)
col_6 = Pin(4, Pin.OUT)
col_5 = Pin(16, Pin.OUT)
col_4 = Pin(17, Pin.OUT)
col_3 = Pin(5, Pin.OUT)
col_2 = Pin(18, Pin.OUT)
col_1 = Pin(19, Pin.OUT)

col_list = [col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8]

row_list[0].value(0)