try:
    from . import ui_audioPlayerWidget
except (ImportError, ModuleNotFoundError):
    try:
        from audio_player import ui_audioPlayerWidget
    except (ImportError, ModuleNotFoundError):
        import ui_audioPlayerWidget
from PySide6 import QtWidgets, QtCore
import subprocess, json, requests
from ffpyplayer.player import MediaPlayer
from io import BytesIO
import threading
import os, re, signal, time, tempfile


class AudioPlayerWidget(ui_audioPlayerWidget.Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.media_player = None
        self.is_playing = False
        self.is_dragging = False
        self.is_end = False
        self.length = 0.0  # 音频时长（秒）
        self.audio_link = ""
        self.temp_file_path = ""  # 临时文件路径（核心修改）
        self.supports_range = False
        self.download_thread = None
        self.is_downloading = False

        self.pushButton_play.clicked.connect(self._play)
        self.pushButton_stop.clicked.connect(self.stop)

        self.interval_timer = QtCore.QTimer()
        self.interval_timer.timeout.connect(self._play_interval)
        self.interval_timer.start(100)

        self.init_progress_bar()
        self.label_download = QtWidgets.QLabel("")
        self.layout().addWidget(self.label_download)

    def _play(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def _check_range_support(self, url: str) -> bool:
        """检测URL是否支持部分请求(Range requests)"""
        try:
            headers = {
                "Range": "bytes=0-1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            }
            response = requests.head(
                url, headers=headers, allow_redirects=True, timeout=10
            )
            lower_headers = [k.lower() for k in response.headers.keys()]
            return response.status_code == 206 or "accept-ranges" in lower_headers
        except Exception as e:
            print(f"检测部分请求支持失败: {e}")
            return False

    def _download_audio_to_tempfile(self, url: str) -> str:
        """下载音频到临时文件（核心修改）"""
        try:
            self.is_downloading = True
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept": "audio/ogg, audio/mpeg, audio/*",
            }

            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0

            # 创建临时文件（自动添加音频扩展名）
            suffix = ".ogg" if url.lower().endswith(".ogg") else ".mp3"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                temp_path = tmp.name
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            self.update_download_label(f"下载中: {progress:.1f}%")

            self.update_download_label("下载完成，准备播放")
            return temp_path  # 返回临时文件路径
        except Exception as e:
            self.update_download_label(f"下载失败: {str(e)}")
            print(f"下载音频失败: {e}")
            return None
        finally:
            self.is_downloading = False

    def update_download_label(self, text: str):
        """线程安全地更新下载标签"""
        QtCore.QMetaObject.invokeMethod(
            self.label_download,
            "setText",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, text),
        )

    def _getlength(self, file_path: str) -> float:
        """从临时文件获取时长（稳定可靠）"""
        if not file_path or not os.path.exists(file_path):
            return 0.0

        # 优先用ffprobe（最可靠）
        try:
            cmd = [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                file_path,
            ]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                timeout=10,
            )
            info = json.loads(result.stdout)
            return float(info["format"]["duration"])
        except Exception as e:
            print(f"ffprobe获取时长失败: {e}")

        # 备选：用ffmpeg
        try:
            cmd = [
                "ffmpeg",
                "-i",
                file_path,
                "-v",
                "quiet",
                "-show_entries",
                "format=duration",
                "-print_format",
                "json",
                "pipe:1",
            ]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                timeout=10,
            )
            info = json.loads(result.stdout)
            return float(info["format"]["duration"])
        except Exception as e:
            print(f"ffmpeg获取时长失败: {e}")

        # 最后：文件大小估算
        try:
            file_size = os.path.getsize(file_path)
            avg_bitrate = 128000  # 128kbps
            return (file_size * 8) / avg_bitrate
        except Exception as e:
            print(f"估算时长失败: {e}")
            return 0.0

    def load_audio(self, audio_link: str):
        """加载音频（优先临时文件）"""
        self.stop()  # 停止当前播放
        self.audio_link = audio_link
        self.temp_file_path = ""  # 清空旧临时文件
        self.label_status.setText("加载中...")
        self.label_download.setText("")

        # 网络链接处理
        if audio_link.startswith(("http://", "https://")):
            self.supports_range = self._check_range_support(audio_link)

            if self.supports_range:
                # 支持部分请求：直接播放URL
                self.media_player = MediaPlayer(audio_link)
                self.media_player.set_pause(True)
                self.length = self._getlength(audio_link)  # 此时file_path是URL
                self.label_status.setText("Ready")
            else:
                # 不支持部分请求：下载到临时文件
                self.label_status.setText("不支持部分请求，准备下载...")
                self.download_thread = threading.Thread(
                    target=self._download_and_initialize, args=(audio_link,)
                )
                self.download_thread.daemon = True
                self.download_thread.start()
        else:
            # 本地文件：直接使用
            self.temp_file_path = audio_link  # 本地文件路径作为"临时文件"
            self.media_player = MediaPlayer(audio_link)
            self.media_player.set_pause(True)
            self.length = self._getlength(audio_link)
            self.label_status.setText("Ready")

    def _download_and_initialize(self, audio_link: str):
        """下载到临时文件后初始化播放器"""
        temp_path = self._download_audio_to_tempfile(audio_link)
        if not temp_path:
            QtCore.QMetaObject.invokeMethod(
                self,
                lambda: self.label_status.setText("下载失败，无法播放"),
                QtCore.Qt.QueuedConnection,
            )
            return

        # 保存临时文件路径并初始化播放器
        self.temp_file_path = temp_path
        QtCore.QMetaObject.invokeMethod(
            self, "_post_download_init", QtCore.Qt.QueuedConnection
        )

    @QtCore.Slot()
    def _post_download_init(self):
        """从临时文件初始化播放器"""
        if not self.temp_file_path or not os.path.exists(self.temp_file_path):
            self.label_status.setText("临时文件不存在")
            return

        # 直接从临时文件播放
        self.media_player = MediaPlayer(self.temp_file_path)
        self.media_player.set_pause(True)
        self.length = self._getlength(self.temp_file_path)
        self.label_status.setText(f"Ready (时长: {self.length:.2f}秒)")

    def play(self):
        if self.is_downloading or not self.media_player:
            return

        self.is_end = False
        self.is_playing = True
        self.media_player.set_pause(False)
        self.label_status.setText("Playing...")
        self.pushButton_play.setText(";")

    def pause(self):
        self.is_playing = False
        if self.media_player:
            self.media_player.set_pause(True)
        self.label_status.setText("Paused")
        self.pushButton_play.setText("4")

    def stop(self, *args, is_end=False):
        self.is_playing = False
        if self.media_player:
            self.media_player.set_pause(True)
            if self.media_player.get_pts() > 0:
                self.media_player.seek(-self.media_player.get_pts())
        if not is_end:
            self.label.setText("00:00:00")
            self.horizontalSlider.setValue(0)
        self.label_status.setText("Ready")
        self.pushButton_play.setText("4")

    def _play_interval(self):
        if (
            self.media_player
            and self.is_playing
            and not self.is_dragging
            and not self.is_downloading
        ):
            try:
                current_pos = self.media_player.get_pts()

                # 动态更新时长（如果初始获取失败）
                if self.length <= 0:
                    self.length = self._getlength(
                        self.temp_file_path if self.temp_file_path else self.audio_link
                    )

                # 检测播放结束
                if self.length > 0 and current_pos >= self.length - 0.5:
                    self.is_end = True
                    self.stop(is_end=True)
                    return

                # 更新时间显示
                hours = int(current_pos // 3600)
                mins = int((current_pos % 3600) // 60)
                secs = int(current_pos % 60)
                self.label.setText(f"{hours:02d}:{mins:02d}:{secs:02d}")

                # 更新进度条
                if self.length > 0:
                    self.horizontalSlider.setValue(
                        int((current_pos / self.length) * 100)
                    )
            except Exception as e:
                print(f"播放更新出错: {e}")

    def init_progress_bar(self):
        self.horizontalSlider.setRange(0, 100)
        self.horizontalSlider.sliderPressed.connect(self.on_slider_pressed)
        self.horizontalSlider.sliderReleased.connect(self.on_slider_released)
        self.horizontalSlider.valueChanged.connect(self.on_slider_changed)

    def on_slider_pressed(self):
        self.is_dragging = True

    def on_slider_released(self):
        if not self.media_player or self.length <= 0:
            self.is_dragging = False
            return
        try:
            target_pos = (self.horizontalSlider.value() / 100.0) * self.length
            if target_pos >= self.length * 0.99:
                self.stop()
            else:
                current_pos = self.media_player.get_pts()
                self.media_player.seek(target_pos - current_pos)
        except Exception as e:
            print(f"进度条调整出错: {e}")
        self.is_dragging = False

    def on_slider_changed(self):
        if self.is_dragging and self.length > 0:
            target_pos = (self.horizontalSlider.value() / 100.0) * self.length
            hours = int(target_pos // 3600)
            mins = int((target_pos % 3600) // 60)
            secs = int(target_pos % 60)
            self.label.setText(f"{hours:02d}:{mins:02d}:{secs:02d}")

    def closeEvent(self, event):
        """关闭时删除临时文件（核心修改）"""
        self.stop()
        # 确保临时文件被删除
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
                print(f"已删除临时文件: {self.temp_file_path}")
            except Exception as e:
                print(f"删除临时文件失败: {e}")
        event.accept()


if __name__ == "__main__":
    import sys

    qa = QtWidgets.QApplication(sys.argv)
    apw = AudioPlayerWidget()
    apw.show()
    test_url = "http://localhost/Audio_2.ogg"  # 替换为实际URL
    apw.load_audio(test_url)
    qa.exec()
