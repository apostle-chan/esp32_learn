"""
更多项目访问 https://www.itprojects.cn
作者：王铭东
版权：此程序是王铭东开发，未经许可禁止传播、复制部分、复制全部内容
邮箱：dong4716138@163.com
"""
import io
import socket
import sys

import numpy as np
from PIL import Image
from PySide6.QtCore import QThread
from PySide6.QtGui import QIcon, Qt, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGroupBox, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QMessageBox

UDP_SOCKET = None  # 存储socket套接字
UDP_CLIENT_IP_PORT = None  # 存储另外一方的ip、port


class KeyboardView(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedWidth(400)
        v_layout = QVBoxLayout()
        v_layout.addStretch(2)

        h_layout = QHBoxLayout()

        # 左侧: 上下左右布局
        v_layout_2 = QVBoxLayout()

        key_4_h_1_layout = QHBoxLayout()
        key_4_h_1_layout.addStretch(1)
        self.up_btn = QPushButton("")
        self.up_btn.setStyleSheet("border-image:url(./images/up.png);")
        self.up_btn.setFixedSize(50, 50)
        self.up_btn.pressed.connect(lambda: self.handle_key("pressed", "up", "\xaa", self.up_btn))
        self.up_btn.released.connect(lambda: self.handle_key("released", "up", "\x00", self.up_btn))
        key_4_h_1_layout.addWidget(self.up_btn)
        key_4_h_1_layout.addStretch(1)
        v_layout_2.addLayout(key_4_h_1_layout)

        key_4_h_2_layout = QHBoxLayout()
        self.left_btn = QPushButton("")
        self.left_btn.setStyleSheet("border-image:url(./images/left.png);")
        self.left_btn.setFixedSize(50, 50)
        self.left_btn.pressed.connect(lambda: self.handle_key("pressed", "left", "\x65", self.left_btn))
        self.left_btn.released.connect(lambda: self.handle_key("released", "left", "\x00", self.left_btn))
        key_4_h_2_layout.addWidget(self.left_btn)
        key_4_h_2_layout.addStretch(1)
        self.right_btn = QPushButton("")
        self.right_btn.setStyleSheet("border-image:url(./images/right.png);")
        self.right_btn.setFixedSize(50, 50)
        self.right_btn.pressed.connect(lambda: self.handle_key("pressed", "right", "\x99", self.right_btn))
        self.right_btn.released.connect(lambda: self.handle_key("released", "right", "\x00", self.right_btn))
        key_4_h_2_layout.addWidget(self.right_btn)
        v_layout_2.addLayout(key_4_h_2_layout)

        key_4_h_3_layout = QHBoxLayout()
        key_4_h_3_layout.addStretch(1)
        self.down_btn = QPushButton("")
        self.down_btn.setStyleSheet("border-image:url(./images/down.png);")
        self.down_btn.setFixedSize(50, 50)
        self.down_btn.pressed.connect(lambda: self.handle_key("pressed", "down", "\x55", self.down_btn))
        self.down_btn.released.connect(lambda: self.handle_key("released", "down", "\x00", self.down_btn))
        key_4_h_3_layout.addWidget(self.down_btn)
        key_4_h_3_layout.addStretch(1)
        v_layout_2.addLayout(key_4_h_3_layout)

        # 右侧: 左转弯、右转弯布局
        v_layout_3 = QVBoxLayout()
        v_layout_3.addStretch(1)
        key_2_h_layout = QHBoxLayout()
        key_2_h_layout.addStretch(1)
        self.turn_left_btn = QPushButton("")
        self.turn_left_btn.setStyleSheet("border-image:url(./images/turn-left.png);")
        self.turn_left_btn.setFixedSize(50, 50)
        self.turn_left_btn.pressed.connect(lambda: self.handle_key("pressed", "turn-left", "\x28", self.turn_left_btn))
        self.turn_left_btn.released.connect(lambda: self.handle_key("released", "turn-left", "\x00", self.turn_left_btn))
        key_2_h_layout.addWidget(self.turn_left_btn)
        key_2_h_layout.addStretch(2)
        self.turn_right_btn = QPushButton("")
        self.turn_right_btn.setStyleSheet("border-image:url(./images/turn-right.png);")
        self.turn_right_btn.setFixedSize(50, 50)
        self.turn_right_btn.pressed.connect(lambda: self.handle_key("pressed", "turn-right", "\x82", self.turn_right_btn))
        self.turn_right_btn.released.connect(lambda: self.handle_key("released", "turn-right", "\x00", self.turn_right_btn))
        key_2_h_layout.addWidget(self.turn_right_btn)
        key_2_h_layout.addStretch(1)
        v_layout_3.addLayout(key_2_h_layout)
        v_layout_3.addStretch(1)

        h_layout.addLayout(v_layout_2)
        h_layout.addLayout(v_layout_3)

        v_layout.addLayout(h_layout)

        v_layout.addStretch(1)

        self.setLayout(v_layout)

    def handle_key(self, click_type, key_name, socket_send_data, btn):
        """处理按钮被按下的处理"""
        global UDP_SOCKET
        print(click_type, key_name, socket_send_data, btn)
        try:
            if click_type == "pressed":  # 按键被按下
                btn.setStyleSheet("border-image:url(./images/%s-%s.png);" % (key_name, "typed"))
                if UDP_SOCKET and UDP_CLIENT_IP_PORT:
                    UDP_SOCKET.sendto(socket_send_data.encode(), UDP_CLIENT_IP_PORT)
            else:  # 松开
                btn.setStyleSheet("border-image:url(./images/%s.png);" % key_name)
                if UDP_SOCKET and UDP_CLIENT_IP_PORT:
                    UDP_SOCKET.sendto(socket_send_data.encode(), UDP_CLIENT_IP_PORT)
        except Exception as ret:
            print(ret)


class UdpThread(QThread):
    """创建udp套接字，接收UDP数据，进行处理"""

    def __init__(self, ip, port, video_widget):
        super().__init__()
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind((ip, port))
        self.udp_socket.settimeout(3)  # 超时时间，意思是：如果调用recvfrom的时候，3秒内没有收到任何数据，会产生异常
        global UDP_SOCKET
        UDP_SOCKET = self.udp_socket
        # 设置运行的标志
        self.run_flag = True
        # 存储要显示的widget对象引用
        self.video_widget = video_widget

    def run(self):
        global UDP_CLIENT_IP_PORT
        while self.run_flag:
            try:
                # 接收来自ESP32Cam的数据
                data, UDP_CLIENT_IP_PORT = self.udp_socket.recvfrom(100000)
                print(UDP_CLIENT_IP_PORT, " >>> ", data)
                bytes_stream = io.BytesIO(data)
                image = Image.open(bytes_stream)
                img = np.asarray(image)
                # PySide显示不需要转换，所以直接用img
                temp_image = QImage(img.flatten(), 480, 320, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image)
                self.video_widget.video_label.setPixmap(temp_pixmap)
            except Exception as ret:
                print("UdpThread error:", ret)
                # 如果产生异常，那么就清除画面内容
                self.video_widget.setStyleSheet("background-color: white;")
                self.video_widget.video_label.setText("无数据, 请检查ESP32Cam发送方或网络")

        # 结束后 关闭套接字
        self.udp_socket.close()
        UDP_CLIENT_IP_PORT = None
        # 清除上次显示画面的残留
        self.video_widget.video_label.setText("选择顶部的操作按钮...")
        self.video_widget.setStyleSheet("background-color: white;")
        print("线程运行结束...")


class VideWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white;")

        layout = QHBoxLayout()

        # 用来显示画面的QLabel
        self.video_label = QLabel("选择顶部的操作按钮...")
        self.video_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.video_label.setScaledContents(True)
        layout.addWidget(self.video_label)

        self.setLayout(layout)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # 存储udp线程
        self.udp_thread = None

        self.setWindowTitle("ESP32Cam远程遥控小车 v2023.11.18 作者：王铭东")
        self.setWindowIcon(QIcon('./images/logo.png'))
        self.resize(1177, 555)  # 重新设置窗口的宽度、高度
        self.setMinimumSize(1177, 555)

        # 选择本电脑IP
        camera_label = QLabel("选择本电脑IP：")

        # ip列表
        # 获取本地电脑的ip地址列表
        hostname, alias_list, ip_addr_list = socket.gethostbyname_ex(socket.gethostname())

        self.combox = QComboBox()
        self.combox.addItems(ip_addr_list)
        self.ip_addr_list = ip_addr_list

        # 本地端口
        port_label = QLabel("本地端口：")
        self.port_edit = QLineEdit("9090")

        g_1 = QGroupBox("监听信息")
        g_1.setFixedHeight(60)
        g_1_h_layout = QHBoxLayout()
        g_1_h_layout.addWidget(camera_label)
        g_1_h_layout.addWidget(self.combox)
        g_1_h_layout.addWidget(port_label)
        g_1_h_layout.addWidget(self.port_edit)
        g_1.setLayout(g_1_h_layout)

        # 启动显示
        self.camera_open_close_btn = QPushButton(QIcon("./images/shexiangtou.png"), "启动显示")
        self.camera_open_close_btn.clicked.connect(self.camera_open_close)

        g_2 = QGroupBox("功能操作")
        g_2.setFixedHeight(60)
        g_2_h_layout = QHBoxLayout()
        g_2_h_layout.addWidget(self.camera_open_close_btn)
        # g_2_h_layout.addWidget(self.record_video_btn)
        # g_2_h_layout.addWidget(save_video_path_setting_btn)
        g_2.setLayout(g_2_h_layout)

        # --------- 整体布局 ---------
        h_layout = QHBoxLayout()
        h_layout.addWidget(g_1)
        h_layout.addWidget(g_2)
        h_layout.addStretch(1)

        # 创建底部的显示区域
        h_layout_2 = QHBoxLayout()
        # 左侧是视频画面
        self.video_widget = VideWidget()
        h_layout_2.addWidget(self.video_widget)
        # 右侧是控制按钮
        self.controller_keyboard_view = KeyboardView()
        h_layout_2.addWidget(self.controller_keyboard_view)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addLayout(h_layout_2)
        self.setLayout(v_layout)  # 让这个布局器设定为当前窗口的布局器，也就说，当前窗口根据这个布局器的设定，显示效果

    def camera_open_close(self):
        """启动创建socket线程，用来接收显示数据"""
        if self.camera_open_close_btn.text() == "启动显示":
            ip = self.combox.currentText()
            try:
                port = int(self.port_edit.text())
            except Exception as ret:
                QMessageBox.about(self, '警告', '端口设置错误！！！')
                return

            self.udp_thread = UdpThread(ip, port, self.video_widget)
            self.udp_thread.daemon = True
            self.udp_thread.start()
            self.camera_open_close_btn.setText("关闭显示")
            # 更改显示的文字提示
            self.video_widget.video_label.setText("等待数据中...")
        else:
            if self.udp_thread:
                self.udp_thread.run_flag = False  # 这里标记为False，当udp线程因为超时3秒后，自动判断，然后线程就退出了
            self.camera_open_close_btn.setText("启动显示")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_window = MainWindow()  # 创建界面
    video_window.show()
    app.exec()  # 里面是一个while True 无限循环
