import network
import camera
import _thread
import time
from machine import SoftI2C, Pin
import struct
import socket


def connect_wifi():
    # 连接wifi
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        print("connecting to network ...")
        wifi.connect("AP982109", "hao1314520")
        while not wifi.isconnected():
            pass
    # 打印网络配置
    print("网络配置", wifi.ifconfig())


def creat_udp_socket():

    # 1.创建SOCKET
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 2.绑定一个固定的端口
    udp_socket.bind(("0.0.0.0", 8000))
    print("绑定端口成功")

    return udp_socket


# def recv_udp_cmd(*args, **kwargs):
#     # 1.创建cli对象
#     i2c = SoftI2C(sda=Pin(14), scl=Pin(15), freq=100000)
#     # 2. 扫描，看看有哪些cli设备
#     devices = i2c.scan()
#     # 3. 接收udp数据
#     try:
#         while True:
#             recv_data, sender_info = udp_socket.recvfrom(1024)
#             print(recv_data.decode("utf-8"))
#             # 3.给这些设备发送测试数据
#             for device in devices:
#                 i2c.writeto(device, recv_data)
#     except Exception as e:
#         print("接收命令的线程结束...", e)


def camera_init():
    # 摄像头初始化
    print("摄像头正在初始化")
    try:
        camera.init(0, format=camera.JPEG)
    except Exception as e:
        camera.deinit()
        camera.init(0, format=camera.JPEG)
    print("正在初始化摄像头...初始化成功")

    # # 拍摄一张图片
    # buf = camera.capture()  # 大小是640x480

    # # 保存图片到文件
    # with open("第一张图片.png", "wb") as f:
    #     f.write(buf)  # buf中的数据就是图片的数据，所以直接写入到文件就行了
    #     print(
    #         "拍照已完成，点击Thonny左侧【MicroPython设备】右侧的三，\n然后看到‘刷新’，点击刷新会看到 图片，\n然后右击图片名称，选择下载到电脑的路径即可..."
    #     )
    # camera.deinit()
    # 其他设置：
    # 上翻下翻
    camera.flip(1)
    # 左/右
    camera.mirror(1)

    # 分辨率
    camera.framesize(camera.FRAME_HVGA)
    # 选项如下：
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA FRAME_FHD
    # FRAME_P_HD FRAME_P_3MP FRAME_QXGA FRAME_QHD FRAME_WQXGA
    # FRAME_P_FHD FRAME_QSXGA
    # 有关详细信息，请查看此链接：https://bit.ly/2YOzizz

    # 特效
    camera.speffect(camera.EFFECT_NONE)
    # 选项如下：
    # 效果\无（默认）效果\负效果\ BW效果\红色效果\绿色效果\蓝色效果\复古效果
    # EFFECT_NONE (default) EFFECT_NEG \EFFECT_BW\ EFFECT_RED\ EFFECT_GREEN\ EFFECT_BLUE\ EFFECT_RETRO

    # 白平衡
    # camera.whitebalance(camera.WB_HOME)
    # 选项如下：
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

    # 饱和
    camera.saturation(0)
    # -2,2（默认为0）. -2灰度
    # -2,2 (default 0). -2 grayscale

    # 亮度
    camera.brightness(0)
    # -2,2（默认为0）. 2亮度
    # -2,2 (default 0). 2 brightness

    # 对比度
    camera.contrast(0)
    # -2,2（默认为0）.2高对比度
    # -2,2 (default 0). 2 highcontrast

    # 质量
    camera.quality(10)
    # 10-63数字越小质量越高


def camera_video():

    # socket UDP 的创建
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    try:
        while True:
            buf = camera.capture()  # 获取图像数据
            s.sendto(buf, ("192.168.31.15", 9090))  # 向服务器发送图像数据
            time.sleep(0.1)  # 适当延时
    except:
        pass
    finally:
        camera.deinit()


def i2c_io(hex: bytes):
    # 1.创建iic对象
    i2c = SoftI2C(sda=Pin(14), scl=Pin(15), freq=100000)
    # 2.扫描，看看哪些iic设备
    devices = i2c.scan()
    print(devices)
    # 3.给这些设备发送测试数据
    for device in devices:
        i2c.writeto(device, hex)


def recv_udp_cmd(*args, **kwargs):
    # 1. 创建iic对象
    i2c = SoftI2C(sda=Pin(14), scl=Pin(15), freq=100000)
    # 2. 扫描，看看有哪些iic的设备
    devices = i2c.scan()
    print(devices)
    # 3. 接收udp数据
    try:
        while True:
            recv_data, sender_info = udp_socket.recvfrom(1024)
            print(recv_data)
            # 3. 给这些设备发送测试数据
            for device in devices:
                i2c.writeto(device, recv_data)
    except Exception as ret:
        print("接收命令的线程结束...", ret)


if __name__ == "__main__":
    # 连接路由器
    # connect_wifi()

    # 测试扩展io
    print("写入\\xA5")
    i2c_io(b"\xA5")

    # # 初始化摄像头
    # camera_init()

    # # 创建UDP套接字
    # udp_socket = creat_udp_socket()

    # # # 创建子线程用来接收数据
    # thread_1 = _thread.start_new_thread(recv_udp_cmd, (None,))

    # try:
    #     while True:
    #         # 向服务器发送数据
    #         udp_socket.sendto("hello".encode(), ("192.168.31.15", 9090))
    #         print("发送测试数据hello给上位机")
    #         time.sleep_ms(1000)
    # except Exception as ret:
    #     print("异常：", ret)

    # try:
    #     while True:
    #         # 向服务端发送数据
    #         """
    #         udp_socket.sendto("hello".encode(), ("192.168.31.15", 9090))
    #         print("发送数据给上位机")
    #         time.sleep_ms(1000)
    #         """
    #         # 获取图像数据
    #         buf = camera.capture()
    #         # 向服务端发送数据
    #         udp_socket.sendto(buf, ("192.168.31.15", 9090))
    #         # 适当延时
    #         time.sleep_ms(50)
    # except Exception as e:
    #     print("异常", e)

    # finally:
    #     camera.deinit()
