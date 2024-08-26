from machine import Pin
import time

# 左前 第1个轮子引脚
P13 = Pin(13, Pin.OUT)
p12 = Pin(12, Pin.OUT)


def wheel_one_front():
    # 第1个轮子前进
    P13.off()
    p12.on()


def wheel_one_back():
    # 第1个轮子后退
    P13.on()
    p12.off()


# 右前 第2个轮子引脚
p14 = Pin(14, Pin.OUT)
p27 = Pin(27, Pin.OUT)


def wheel_two_front():
    # 第2个轮子前进
    p14.off()
    p27.on()


def wheel_two_back():
    # 第2个轮子后退
    p14.on()
    p27.off()


# 左后 第3个轮子引脚
p33 = Pin(33, Pin.OUT)
p32 = Pin(32, Pin.OUT)


def wheel_three_front():
    # 第3个轮子前进
    p33.on()
    p32.off()


def wheel_three_back():
    # 第3个轮子后退
    p33.off()
    p32.on()


# 右后 第4个轮子引脚
p26 = Pin(26, Pin.OUT)
p25 = Pin(25, Pin.OUT)


def wheel_four_front():
    # 第4个轮子前进
    p26.on()
    p25.off()


def wheel_four_back():
    # 第4个轮子后退
    p26.off()
    p25.on()


def main():
    test()


def move_front():
    # 前进
    wheel_one_front()
    wheel_two_front()
    wheel_three_front()
    wheel_four_front()


def move_back():
    # 后退
    wheel_one_back()
    wheel_two_back()
    wheel_three_back()
    wheel_four_back()


def move_right():
    # 右移动
    wheel_one_front()
    wheel_two_back()
    wheel_three_back()
    wheel_four_front()


def move_left():
    # 左移动
    wheel_four_back()
    wheel_two_front()
    wheel_three_front()
    wheel_four_back()


def move_cw():
    # 顺时针旋转
    wheel_one_front()
    wheel_two_back()
    wheel_three_front()
    wheel_four_back()


def move_aw():
    wheel_one_back()
    wheel_two_front()
    wheel_three_back()
    wheel_four_front()


def stop():
    # 停止
    P13.off()
    p12.off()
    p14.off()
    p27.off()
    p26.off()
    p25.off()
    p33.off()
    p32.off()


def test():
    stop()
    # stop()
