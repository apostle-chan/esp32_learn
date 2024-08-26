from machine import Pin

p0 = Pin(0, Pin.OUT)  # 创建对象p0，对应GPIO口输出
p0.on()  # 设置引脚为"on"(1)高电平
p0.off()  # 设置引脚为"off"(0)低电平
p0.value(1)  # 设置引脚为"on"(1)高电平

p2 = Pin(2, Pin.IN)  # 创建对象p2，对应GPIO2口输入
print(p2.value())  # 获取引脚输入值，0低电平或者1高电平

p4 = Pin(4, Pin.IN, Pin.PULL_UP)  # 打开内部上拉电阻
p5 = Pin(5, Pin.OUT, value=1)  # 初始化时候设置引脚的值为1（高电平）
