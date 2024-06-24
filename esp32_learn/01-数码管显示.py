from machine import Pin
import time

# 定义引脚对应数码管的位置
a = Pin(13, Pin.OUT)
b = Pin(12, Pin.OUT)
c = Pin(14, Pin.OUT)
d = Pin(27, Pin.OUT)
e = Pin(26, Pin.OUT)
f = Pin(25, Pin.OUT)
g = Pin(33, Pin.OUT)
h = Pin(32, Pin.OUT)

# 将对应的引脚对象存储到列表
led_list = [a, b, c, d, e, f, g, h]

number_dict = {
    0: "11111100",  # 顺序依次是abcdefgh
    1: "01100000",
    2: "11011010",
    3: "11110010",
    4: "01100110",
    5: "10110110",
    6: "10111110",
    7: "11100000",
    8: "11111110",
    9: "11110110",
}


def show_number(number):
    if number_dict.get(number):
        i = 0
        for num in number_dict.get(number):
            if num == "1":
                led_list[i].value(1)
            else:
                led_list[i].value(0)
            i += 1

for i in range(10):
    show_number(i)
    time.sleep(1)
