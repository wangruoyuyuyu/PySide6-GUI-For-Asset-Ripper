from PySide6.QtCore import Qt, QUrl, Signal, QObject, QSize
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (QWidget, QLabel, QScrollArea, 
                             QVBoxLayout, QApplication)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

class NetworkImageLoader(QObject):
    image_loaded = Signal(QPixmap)
    load_failed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.on_reply_finished)

    def load_image(self, url_str):
        url = QUrl(url_str)
        if not url.isValid():
            self.load_failed.emit(f"无效URL: {url_str}")
            return
        request = QNetworkRequest(url)
        request.setRawHeader(b"User-Agent", b"Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        self.manager.get(request)

    def on_reply_finished(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            self.load_failed.emit(f"加载失败: {reply.errorString()}")
            reply.deleteLater()
            return
        data = reply.readAll()
        reply.deleteLater()
        pixmap = QPixmap()
        if pixmap.loadFromData(data):
            self.image_loaded.emit(pixmap)
        else:
            image = QImage()
            if image.loadFromData(data):
                self.image_loaded.emit(QPixmap.fromImage(image))
            else:
                self.load_failed.emit("无法解析图片数据")


class ReliableImageScaler(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_pixmap = None
        self.scaled_pixmap = None
        
        # 主布局 - 关键：使用布局确保控件随父容器缩放
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.scroll_area)
        
        # 图片显示标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("等待加载图片...")
        self.scroll_area.setWidget(self.image_label)
        
        # 网络加载器
        self.loader = NetworkImageLoader(self)
        self.loader.image_loaded.connect(self.on_image_loaded)
        self.loader.load_failed.connect(lambda msg: self.image_label.setText(msg))

    def on_image_loaded(self, pixmap: QPixmap):
        """图片加载完成后初始化并首次缩放"""
        self.original_pixmap = pixmap
        self.scale_to_fit()  # 立即缩放以适应当前尺寸

    def scale_to_fit(self):
        """核心缩放逻辑：根据当前可用空间缩放图片"""
        if not self.original_pixmap:
            return
            
        # 获取实际可用显示区域尺寸（滚动区的视口大小）
        available_size = self.scroll_area.viewport().size()
        
        # 计算缩放后的尺寸（保持比例，不超过可用区域）
        scaled_size = self.original_pixmap.size().scaled(
            available_size,
            Qt.KeepAspectRatio
        )
        
        # 只有尺寸变化时才重新缩放，避免不必要的重绘
        if scaled_size != self.original_pixmap.size() or not self.scaled_pixmap:
            self.scaled_pixmap = self.original_pixmap.scaled(
                scaled_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(self.scaled_pixmap)

    def resizeEvent(self, event):
        """窗口/容器尺寸变化时自动触发缩放"""
        # 先让父类处理布局更新
        super().resizeEvent(event)
        # 延迟一点时间确保布局完成更新（关键解决时机问题）
        self.scale_to_fit()


# 测试代码（放入QTabWidget中）
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
    
    # 创建主窗口和标签页
    main_window = QTabWidget()
    main_window.setWindowTitle("可靠的图片自动缩放")
    main_window.resize(800, 600)  # 初始窗口大小
    
    # 创建图片标签页
    image_tab = QWidget()
    tab_layout = QVBoxLayout(image_tab)
    image_viewer = ReliableImageScaler()
    tab_layout.addWidget(image_viewer)
    
    main_window.addTab(image_tab, "图片预览")
    
    # 加载测试图片
    image_viewer.loader.load_image("https://picsum.photos/2000/1500")  # 较大图片用于测试
    
    main_window.show()
    sys.exit(app.exec())
