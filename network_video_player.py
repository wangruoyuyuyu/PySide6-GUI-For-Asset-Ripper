import sys
import vlc
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QTabWidget,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QResizeEvent
from PySide6 import QtCore, QtWidgets


class VLCVideoWidget(QWidget):
    """独立的VLC视频播放组件，可嵌入入任何Qt窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.instance = vlc.Instance(
            [
                "--no-xlib",  # 避免X11相关问题
                "--no-video-title-show",  # 禁用标题显示
                "--avcodec-skip-frame=0",  # 不跳过任何帧
                "--avcodec-skip-idct=0",  # 不跳过IDCT步骤
            ]
        )
        self.media_player = self.instance.media_player_new()

        # 初始化UI
        self.init_ui()

        # 绑定VLC播放器到窗口
        self.bind_player_to_widget()

    def init_ui(self):
        """初始化播放控件UI"""
        # 视频显示区域
        self.video_frame = QWidget()
        self.video_frame.setStyleSheet("background-color: black;")
        self.video_frame.setMinimumSize(640, 360)

        # 控制按钮
        self.play_btn = QPushButton("Play")  # ("播放")
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn = QPushButton("Stop")  # ("停止")
        self.stop_btn.clicked.connect(self.stop)

        # 状态显示
        self.status_label = QLabel("Ready")  # ("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)

        # 布局管理
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.stop_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_frame)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def bind_player_to_widget(self):
        """将VLC播放器绑定到当前窗口部件"""
        if sys.platform.startswith("win"):
            self.media_player.set_hwnd(self.video_frame.winId())
        elif sys.platform.startswith("linux"):
            self.media_player.set_xwindow(self.video_frame.winId())
        elif sys.platform.startswith("darwin"):
            self.media_player.set_nsobject(int(self.video_frame.winId()))

    def load_video(self, url):
        """加载视频（支持本地文件路径或网络URL）"""
        if url.startswith(("http://", "https://", "rtsp://")):
            self.status_label.setText(
                f"Loaded video"  #:{url.split('/')[-1]}"
            )  # (f"加载网络视频: {url.split('/')[-1]}")
            media = self.instance.media_new(url)
        else:
            self.status_label.setText(
                f"Loaded video"  #:{url.split('/')[-1]}"
            )  # (f"加载本地视频: {url.split('/')[-1]}")
            media = self.instance.media_new(url)

        self.media_player.set_media(media)
        media.parse()  # 解析媒体信息

    def toggle_play(self):
        """切换播放/暂停状态"""
        if self.media_player.is_playing():
            self.media_player.pause()
            self.play_btn.setText("Play")  # ("播放")
            self.status_label.setText("Paused")  # ("已暂停")
        else:
            self.media_player.play()
            self.play_btn.setText("Pause")  # ("暂停")
            self.status_label.setText("Playing...")  # ("播放中...")

    def stop(self):
        """停止播放"""
        self.media_player.stop()
        self.play_btn.setText("Play")  # ("播放")
        self.status_label.setText("Stopped")  # ("已停止")

    def resizeEvent(self, event: QResizeEvent):
        """窗口大小改变时自适应调整视频"""
        if self.media_player:
            self.media_player.video_set_scale(0)  # 0表示自适应窗口大小
        super().resizeEvent(event)

    def closeEvent(self, event):
        """关闭时释放资源"""
        self.media_player.stop()
        event.accept()

    def getPlayProgress(self):
        """获取播放进度"""
        return (self.media_player.get_time(), self.media_player.get_length())

    def setPlayProgress(self, playprogress: int):
        """设置播放进度"""
        current = self.media_player.get_time()
        total = self.media_player.get_length()

        if playprogress < current:
            # 用停止法了事得了
            self.media_player.stop()
            self.media_player.play()
            self.media_player.set_time(playprogress)
        else:
            # 向后拖动直接设置
            self.media_player.set_time(playprogress)

        # 恢复播放
        if self.media_player.is_playing():
            self.media_player.play()


# 示例：在不同窗口中引用视频组件
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频组件复用示例")
        self.setGeometry(100, 100, 1280, 720)

        # 创建标签页演示多窗口复用
        self.tabs = QTabWidget()

        # 第一个标签页：播放测试视频
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout(self.tab1)
        self.video_player1 = VLCVideoWidget()
        self.video_player1.load_video(
            "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4"
        )
        self.tab1_layout.addWidget(self.video_player1)

        # 第二个标签页：预留的另一个播放器
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout(self.tab2)
        self.video_player2 = VLCVideoWidget()
        self.tab2_layout.addWidget(self.video_player2)
        self.tab2_layout.addWidget(QLabel("在此处可加载其他视频"))

        # 添加标签页
        self.tabs.addTab(self.tab1, "测试视频")
        self.tabs.addTab(self.tab2, "备用播放器")

        self.setCentralWidget(self.tabs)


class SecondWindow(QMainWindow):
    """另一个窗口，同样可以引用视频组件"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("第二个窗口中的视频播放器")
        self.setGeometry(200, 200, 960, 540)

        self.video_player = VLCVideoWidget()
        self.setCentralWidget(self.video_player)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 显示主窗口
    main_window = MainWindow()
    main_window.show()

    # 显示第二个窗口（演示多窗口复用）
    second_window = SecondWindow()
    second_window.show()

    sys.exit(app.exec())
