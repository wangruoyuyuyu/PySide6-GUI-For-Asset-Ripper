import sys
import time
import cv2
import numpy as np
import pyaudio
import wave
import logging
import requests
import os
import tempfile, _thread
from collections import deque

try:
    import ffmpeg

    has_ffmpeg = True
except (ImportError, FileNotFoundError):
    has_ffmpeg = False
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QMessageBox,
    QComboBox,
    QTextEdit,
    QProgressDialog,
)
from PySide6.QtCore import Qt, QThread, Signal, QMutex
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor


logging.basicConfig(
    filename="video_player.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class RangeSupportChecker:
    """检测服务器是否支持Partial Request (Range请求)"""

    @staticmethod
    def check(url):
        """
        检查服务器是否支持Range请求

        参数:
            url: 视频URL

        返回:
            tuple: (是否支持, 错误信息或None)
        """
        try:
            # 发送一个小范围的HEAD请求测试
            headers = {"Range": "bytes=0-1"}
            response = requests.head(url, headers=headers, timeout=10)

            # 支持Range请求的服务器会返回206状态码
            # 或在正常响应中包含Accept-Ranges头
            if response.status_code == 206:
                return (True, "服务器支持部分请求 (Range)")

            # 检查是否明确支持字节范围请求
            if "Accept-Ranges" in response.headers:
                return (
                    response.headers["Accept-Ranges"].lower() == "bytes",
                    f"服务器Accept-Ranges: {response.headers['Accept-Ranges']}",
                )

            # 有些服务器不响应HEAD请求的Range头，尝试GET请求
            response = requests.get(url, headers=headers, timeout=10, stream=True)
            if response.status_code == 206:
                return (True, "服务器支持部分请求 (Range)")

            return (False, "服务器不支持部分请求 (Range)")

        except Exception as e:
            return (False, f"检测Range支持时出错: {str(e)}")


class AudioVisualizer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 100)
        self.setStyleSheet("background-color: #222; color: white;")
        self.audio_data = []
        self.max_samples = 100
        self.data_status = "等待音频数据..."

    def update_audio(self, data, data_size=0):
        self.data_status = f"数据大小: {data_size}字节"
        if not data or data_size == 0:
            self.audio_data = []
            self.update()
            return

        try:
            samples = np.frombuffer(data, dtype=np.int16)
            if len(samples) == 0:
                self.audio_data = []
                self.data_status += " (空数据)"
                self.update()
                return

            energy = np.sum(np.square(samples)) / len(samples)
            self.data_status += f", 能量: {energy:.2f}"

            samples = np.abs(samples) / 32768
            step = max(1, len(samples) // self.max_samples)
            self.audio_data = samples[::step][: self.max_samples]
            self.update()
        except Exception as e:
            self.data_status = f"数据处理错误: {str(e)}"
            logging.error(f"音频可视化错误: {str(e)}")
            self.audio_data = []
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(34, 34, 34))

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(10, 20, self.data_status)

        if not self.audio_data:
            return

        w = self.width()
        h = self.height()
        step_w = w / len(self.audio_data)
        painter.setPen(QColor(0, 255, 128))

        for i in range(len(self.audio_data) - 1):
            x1 = i * step_w
            y1 = h / 2 - (self.audio_data[i] * h / 2)
            x2 = (i + 1) * step_w
            y2 = h / 2 - (self.audio_data[i + 1] * h / 2)
            painter.drawLine(x1, y1, x2, y2)

        painter.setPen(QColor(100, 100, 100))
        painter.drawLine(0, h / 2, w, h / 2)


class VideoCaptureThread(QThread):
    frame_ready = Signal(QImage, float)
    error_occurred = Signal(str)
    duration_updated = Signal(int)
    audio_spec_ready = Signal(dict)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.cap = None
        self.running = False
        self.paused = True
        self.fps = 30
        self.total_frames = 0
        self.current_frame = 0
        self.total_duration = 0
        self.mutex = QMutex()
        self.external_seek_request = False
        self.seek_position = 0
        self.key_frames = []  # 存储关键帧位置
        self._is_to_stop_old_frameTimer = False

    def load_key_frames(self):
        """预加载关键帧位置，提高定位准确性"""
        if not has_ffmpeg or not self.video_path:
            return

        try:
            # 使用ffmpeg获取关键帧信息
            probe = ffmpeg.probe(
                self.video_path,
                select_streams="v",
                show_frames="key_frame=1",
                show_entries="frame=pkt_pts_time",
            )

            # 提取关键帧时间戳
            self.key_frames = []
            for frame in probe["frames"]:
                try:
                    pts_time = float(frame["pkt_pts_time"])
                    self.key_frames.append(pts_time)
                except (KeyError, ValueError):
                    continue

            if self.key_frames:
                self.error_occurred.emit(f"已加载{len(self.key_frames)}个关键帧位置")
            else:
                self.error_occurred.emit("未检测到关键帧，可能影响定位准确性")

        except Exception as e:
            self.error_occurred.emit(f"提取关键帧失败: {str(e)}")
            logging.warning(f"提取关键帧失败: {str(e)}")
            self.key_frames = []

    def find_nearest_key_frame(self, target_time):
        """找到目标时间戳之前最近的关键帧"""
        if not self.key_frames:
            return target_time

        # 二分查找最近的关键帧
        left, right = 0, len(self.key_frames) - 1
        best = 0

        while left <= right:
            mid = (left + right) // 2
            if self.key_frames[mid] <= target_time:
                best = mid
                left = mid + 1
            else:
                right = mid - 1

        return self.key_frames[best]

    def run(self):
        self.mutex.lock()
        self.running = True
        self.mutex.unlock()
        self._is_to_stop_old_frameTimer = True

        try:
            # 明确使用FFmpeg后端打开视频
            self.cap = cv2.VideoCapture(self.video_path, cv2.CAP_FFMPEG)
            if not self.cap.isOpened():
                self.error_occurred.emit(f"无法打开视频: {self.video_path}")
                return

            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.total_duration = (
                self.total_frames / self.fps if self.total_frames else 0
            )
            self.duration_updated.emit(int(self.total_duration * 1000))
            self.error_occurred.emit(
                f"视频参数: FPS={self.fps:.2f}, 总时长={self.total_duration:.1f}秒"
            )

            # 加载关键帧信息
            self.load_key_frames()

            self._extract_audio_spec()

            play_interval = 1.0 / self.fps
            last_play_time = time.time()
            frm = 0
            self._is_first_frame = True

            while True:
                self.mutex.lock()
                if not self.running:
                    self.mutex.unlock()
                    break
                if self.paused:
                    self.mutex.unlock()
                    time.sleep(0.01)
                    continue

                if self.external_seek_request:
                    # 计算目标时间戳（秒）
                    target_time = self.seek_position / 1000.0

                    # 找到最近的关键帧
                    key_frame_time = self.find_nearest_key_frame(target_time)

                    # 先定位到关键帧
                    frame_pos_key = int(key_frame_time * self.fps)
                    frame_pos_key = max(0, min(frame_pos_key, self.total_frames - 1))
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos_key)

                    # 从关键帧解码到目标帧，确保解码器状态正确
                    target_frame = int(target_time * self.fps)
                    target_frame = max(0, min(target_frame, self.total_frames - 1))

                    # 逐帧解码直到目标帧
                    frames_to_skip = target_frame - frame_pos_key
                    if frames_to_skip > 0:
                        for _ in range(frames_to_skip):
                            ret, _ = self.cap.read()
                            if not ret:
                                break

                    self.current_frame = target_frame
                    self.external_seek_request = False
                    self.error_occurred.emit(
                        f"视频已定位到: {target_time:.2f}秒 (通过关键帧 {key_frame_time:.2f}秒)"
                    )

                self.mutex.unlock()

                # current_time = time.time()
                # elapsed = current_time - last_play_time
                # if elapsed < play_interval:
                #     time.sleep(play_interval - elapsed)
                # last_play_time = current_time
                frm += 1
                if self._is_first_frame:
                    self._is_to_stop_old_frameTimer = False
                    _thread.start_new_thread(self._set_the_frame, tuple())
                    self._is_first_frame = False
                else:
                    while frm >= self._frm:
                        time.sleep(0.00001)

                ret, frame = self.cap.read()
                if not ret:
                    # 尝试重试几次
                    retry_count = 0
                    while not ret and retry_count < 3:
                        self.error_occurred.emit(f"读取帧失败，重试 {retry_count+1}/3")
                        ret, frame = self.cap.read()
                        retry_count += 1

                    if not ret:
                        self.error_occurred.emit("视频播放结束")
                        self.mutex.lock()
                        self.paused = True
                        self.current_frame = 0
                        self.mutex.unlock()
                        break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = frame_rgb.shape
                q_image = QImage(frame_rgb.data, w, h, w * c, QImage.Format_RGB888)
                self.current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                current_timestamp = self.current_frame / self.fps
                self.frame_ready.emit(q_image, current_timestamp)

        except Exception as e:
            self.error_occurred.emit(f"视频错误: {str(e)}")
        finally:
            self.mutex.lock()
            if self.cap:
                self.cap.release()
            self.running = False
            self.mutex.unlock()

    def _set_the_frame(self):
        self._frm = 0
        while True:
            if self._is_to_stop_old_frameTimer:
                self._is_to_stop_old_frameTimer = False
                break
            if self.paused:
                time.sleep(0.00001)
                continue
            self._frm += 1
            time.sleep(1.0 / self.fps)
            # print(self._frm)

    def _extract_audio_spec(self):
        if not has_ffmpeg:
            self.error_occurred.emit("未检测到ffmpeg，仅播放视频画面（无声音）")
            self.audio_spec_ready.emit(None)
            return

        try:
            probe = ffmpeg.probe(self.video_path)
            audio_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "audio"
                ),
                None,
            )

            if audio_stream:
                spec = {
                    "sample_rate": int(audio_stream["sample_rate"]),
                    "channels": int(audio_stream["channels"]),
                    "codec": audio_stream["codec_name"],
                    "duration": (
                        float(probe["format"]["duration"])
                        if "duration" in probe["format"]
                        else 0
                    ),
                    "bit_rate": audio_stream.get("bit_rate", "未知"),
                }
                self.error_occurred.emit(
                    f"音频参数: 采样率={spec['sample_rate']}, 声道={spec['channels']}, "
                    f"编码={spec['codec']}, 比特率={spec['bit_rate']}"
                )
                self.audio_spec_ready.emit(spec)
            else:
                self.error_occurred.emit("视频中未包含音频流")
                self.audio_spec_ready.emit(None)
        except Exception as e:
            self.error_occurred.emit(f"音频参数提取失败: {str(e)}")
            self.audio_spec_ready.emit(None)

    def pause(self):
        self.mutex.lock()
        self.paused = not self.paused
        self.mutex.unlock()

    def stop(self):
        self.mutex.lock()
        self.paused = True
        self.running = False
        self.current_pos_backup = self.current_frame
        self.mutex.unlock()

    def restart(self):
        self.mutex.lock()
        if not self.running:
            self.current_frame = (
                self.current_pos_backup if hasattr(self, "current_pos_backup") else 0
            )
            self.start()
        else:
            self.paused = False
        self.mutex.unlock()

    def set_position(self, pos_ms):
        self.mutex.lock()
        if not self.cap or not self.running:
            self.mutex.unlock()
            return

        self.seek_position = pos_ms
        self.external_seek_request = True
        self.mutex.unlock()


class AudioPlayThread(QThread):
    audio_error = Signal(str)
    device_list_updated = Signal(list)
    audio_data_ready = Signal(bytes, int)
    ffmpeg_stderr = Signal(str)

    def __init__(self):
        super().__init__()
        self.audio_spec = None
        self.video_path = None
        self.running = False
        self.paused = True
        self.current_timestamp = 0.0
        self.pa = None
        self.stream = None
        self.process = None
        self.selected_device = None
        self.volume = 1.0
        self.debug_file = None
        self.mutex = QMutex()
        self.data_counter = 0

        # 音频数据缓冲区
        self.audio_buffer = deque()
        self.buffer_max_size = 3
        self.buffer_min_size = 1

    def init_audio(self, audio_spec, video_path):
        if not audio_spec or not has_ffmpeg:
            return

        self.audio_spec = audio_spec
        self.video_path = video_path
        self.pa = pyaudio.PyAudio()

        try:
            if "--debug" in sys.argv:
                self.debug_file = wave.open("audio_debug.wav", "wb")
                self.debug_file.setnchannels(audio_spec["channels"])
                self.debug_file.setsampwidth(2)
                self.debug_file.setframerate(audio_spec["sample_rate"])
                logging.info("调试音频文件初始化成功")
            else:
                self.debug_file = None
        except Exception as e:
            self.audio_error.emit(f"调试文件创建失败: {str(e)}")
            logging.error(f"调试文件创建失败: {str(e)}")
            self.debug_file = None

        devices = []
        for i in range(self.pa.get_device_count()):
            try:
                dev_info = self.pa.get_device_info_by_index(i)
                if dev_info.get("maxOutputChannels", 0) > 0:
                    is_virtual = (
                        "mapper" in dev_info["name"].lower()
                        or "virtual" in dev_info["name"].lower()
                    )
                    dev_name = f"{dev_info['name']} {'(虚拟设备)' if is_virtual else '(硬件设备)'}"
                    devices.append((i, dev_name, dev_info, is_virtual))
            except Exception as e:
                logging.warning(f"获取设备信息失败: {str(e)}")

        self.device_list_updated.emit(devices)
        self.audio_error.emit(f"检测到{len(devices)}个音频输出设备")

    def set_audio_device(self, device_index):
        self.mutex.lock()
        self.selected_device = device_index
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        buffer_size = 1024
        self.audio_error.emit(f"音频缓冲区大小设置为: {buffer_size}")

        retry_count = 3
        for i in range(retry_count):
            if self._create_audio_stream(buffer_size):
                break
            else:
                self.audio_error.emit(f"音频流创建重试 {i+1}/{retry_count}")
                time.sleep(0.5)
        self.mutex.unlock()

    def _create_audio_stream(self, buffer_size):
        if not self.audio_spec or not self.pa or self.selected_device is None:
            return False

        try:
            dev_info = self.pa.get_device_info_by_index(self.selected_device)

            stream_kwargs = {
                "rate": self.audio_spec["sample_rate"],
                "channels": self.audio_spec["channels"],
                "format": pyaudio.paInt16,
                "output": True,
                "frames_per_buffer": buffer_size,
                "output_device_index": self.selected_device,
                "start": False,
            }

            try:
                supported = self.pa.is_format_supported(
                    rate=self.audio_spec["sample_rate"],
                    channels=self.audio_spec["channels"],
                    format=pyaudio.paInt16,
                    output=True,
                    output_device=self.selected_device,
                )
                if not supported:
                    self.audio_error.emit(
                        f"设备不支持当前音频格式（采样率: {self.audio_spec['sample_rate']}）"
                    )
                    return False
            except Exception as e:
                self.audio_error.emit(f"格式支持检查警告: {str(e)}（继续尝试）")

            self.stream = self.pa.open(**stream_kwargs)
            if not self.stream.is_active():
                self.stream.start_stream()
                time.sleep(0.1)

            if not self.stream.is_active():
                raise Exception("流启动后仍未激活")

            self.audio_error.emit(
                f"音频流创建成功: 设备={dev_info['name']}, 缓冲大小={buffer_size}"
            )
            return True
        except Exception as e:
            self.audio_error.emit(f"音频流创建失败: {str(e)}")
            logging.error(f"音频流创建失败: {str(e)}")
            self.stream = None
            return False

    def set_volume(self, volume):
        self.mutex.lock()
        self.volume = max(0.0, min(1.0, volume / 100.0))
        self.audio_error.emit(f"音量设置为: {self.volume*100:.1f}%")
        self.mutex.unlock()

    def manual_sync(self, video_timestamp):
        self.mutex.lock()
        if not self.running or not self.stream:
            self.mutex.unlock()
            return

        self.audio_error.emit(
            f"手动同步音频: 视频={video_timestamp:.2f}s, 音频={self.current_timestamp:.2f}s"
        )

        # 清空缓冲区并重新定位
        self.audio_buffer.clear()
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

        self.current_timestamp = video_timestamp
        self.mutex.unlock()

    def run(self):
        self.mutex.lock()
        if not self.audio_spec or not self.stream or not has_ffmpeg:
            self.audio_error.emit("音频播放条件不满足，退出线程")
            self.mutex.unlock()
            return

        self.running = True
        self.data_counter = 0
        self.audio_error.emit("音频线程启动（初始状态：暂停）")
        self.mutex.unlock()

        try:
            # 音频读取线程
            self.read_thread_running = True
            import threading

            self.read_thread = threading.Thread(
                target=self._read_audio_data, daemon=True
            )
            self.read_thread.start()

            # 音频播放主循环
            while True:
                self.mutex.lock()
                if not self.running:
                    self.mutex.unlock()
                    break
                if self.paused:
                    self.audio_buffer.clear()
                    self.mutex.unlock()
                    time.sleep(0.01)
                    continue

                # 等待缓冲区有足够数据
                while (
                    len(self.audio_buffer) < self.buffer_min_size
                    and self.running
                    and not self.paused
                ):
                    self.mutex.unlock()
                    time.sleep(0.001)
                    self.mutex.lock()

                if not self.audio_buffer:
                    self.mutex.unlock()
                    continue

                # 从缓冲区获取数据
                in_bytes = self.audio_buffer.popleft()
                data_size = len(in_bytes)
                self.mutex.unlock()

                # 应用音量
                if self.volume != 1.0:
                    audio_np = np.frombuffer(in_bytes, dtype=np.int16)
                    audio_np = (audio_np * self.volume).astype(np.int16)
                    in_bytes = audio_np.tobytes()

                # 写入音频流
                try:
                    self.mutex.lock()
                    if self.stream and self.stream.is_active():
                        self.stream.write(in_bytes)

                        # 更新时间戳
                        bytes_per_sample = self.audio_spec["channels"] * 2
                        sample_count = data_size // bytes_per_sample
                        self.current_timestamp += (
                            sample_count / self.audio_spec["sample_rate"]
                        )
                    else:
                        self.audio_error.emit("音频流未激活，无法播放")
                    self.mutex.unlock()

                except Exception as e:
                    self.audio_error.emit(f"音频写入失败: {str(e)}")
                    logging.error(f"音频写入失败: {str(e)}")
                    self.mutex.unlock()
                    time.sleep(0.1)

        except Exception as e:
            self.audio_error.emit(f"音频线程错误: {str(e)}")
            logging.error(f"音频线程错误: {str(e)}")
        finally:
            self.mutex.lock()
            self.read_thread_running = False
            if self.process:
                self.process.terminate()
                self.process.wait()
            if self.debug_file:
                self.debug_file.close()
                self.audio_error.emit("调试音频已保存到 audio_debug.wav")
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
            if self.pa:
                self.pa.terminate()
            self.running = False
            self.audio_buffer.clear()
            self.mutex.unlock()
            self.audio_error.emit(f"音频线程结束，共处理{self.data_counter}块数据")

    def _read_audio_data(self):
        """读取音频数据并填充缓冲区"""
        while self.running and self.read_thread_running:
            self.mutex.lock()
            if self.paused or not self.running:
                self.mutex.unlock()
                time.sleep(0.01)
                continue

            # 缓冲区已满则等待
            while (
                len(self.audio_buffer) >= self.buffer_max_size
                and self.running
                and not self.paused
            ):
                self.mutex.unlock()
                time.sleep(0.005)
                self.mutex.lock()

            if not self.process:
                try:
                    self.process = (
                        ffmpeg.input(
                            self.video_path, ss=self.current_timestamp, threads=1
                        )
                        .output(
                            "pipe:",
                            format="s16le",
                            ac=self.audio_spec["channels"],
                            ar=self.audio_spec["sample_rate"],
                            acodec="pcm_s16le",
                        )
                        .overwrite_output()
                        .run_async(pipe_stdout=True, pipe_stderr=True)
                    )
                    self.audio_error.emit(
                        f"ffmpeg解码启动（时间戳: {self.current_timestamp:.2f}s）"
                    )
                    self.start_ffmpeg_stderr_reader()
                except Exception as e:
                    self.audio_error.emit(f"ffmpeg启动失败: {str(e)}")
                    logging.error(f"ffmpeg启动失败: {str(e)}")
                    self.mutex.unlock()
                    time.sleep(0.1)
                    continue
            self.mutex.unlock()

            # 读取音频数据
            try:
                in_bytes = self.process.stdout.read(4096)
                data_size = len(in_bytes)

                if data_size == 0:
                    self.mutex.lock()
                    total_duration = self.audio_spec.get("duration", 0)
                    if self.current_timestamp >= total_duration - 1.0:
                        self.audio_error.emit("音频播放结束")
                        self.paused = True
                        self.mutex.unlock()
                        break
                    self.mutex.unlock()
                    time.sleep(0.01)
                    continue

                self.data_counter += 1
                if self.data_counter % 10 == 0:
                    self.audio_error.emit(
                        f"已处理{self.data_counter}块音频数据，缓冲区大小: {len(self.audio_buffer)}"
                    )

                if self.debug_file:
                    self.debug_file.writeframes(in_bytes)

                self.audio_data_ready.emit(in_bytes, data_size)

                # 将数据添加到缓冲区
                self.mutex.lock()
                self.audio_buffer.append(in_bytes)
                self.mutex.unlock()

            except Exception as e:
                self.audio_error.emit(f"音频读取错误: {str(e)}")
                logging.error(f"音频读取错误: {str(e)}")
                time.sleep(0.1)

    def start_ffmpeg_stderr_reader(self):
        def read_stderr():
            while self.process and self.process.poll() is None and self.running:
                try:
                    err = self.process.stderr.readline()
                    if err:
                        err_str = err.decode("utf-8", errors="ignore").strip()
                        self.ffmpeg_stderr.emit(f"ffmpeg: {err_str}")
                        logging.debug(f"ffmpeg输出: {err_str}")
                except Exception as e:
                    logging.error(f"读取ffmpeg stderr错误: {str(e)}")
                    break

        import threading

        threading.Thread(target=read_stderr, daemon=True).start()

    def pause(self):
        self.mutex.lock()
        self.paused = not self.paused
        state = "暂停" if self.paused else "继续"
        self.audio_error.emit(f"音频{state}")
        self.mutex.unlock()

    def stop(self):
        self.mutex.lock()
        self.running = False
        self.paused = True
        self.mutex.unlock()
        self.audio_error.emit("音频线程停止")

    def seek(self, pos_sec):
        """定位音频到指定时间点"""
        self.mutex.lock()
        self.audio_error.emit(f"音频定位到: {pos_sec:.2f}秒")
        self.audio_buffer.clear()
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
        self.current_timestamp = pos_sec
        self.mutex.unlock()


class OpenCVVideoWidget(QWidget):
    def __init__(self, parent=None, debug=False):
        super().__init__(parent)
        self.video_thread = None
        self.audio_thread = None
        self.is_playing = False
        self.duration = 0
        self.current_pos = 0
        self.video_loaded = False
        self.video_path = None  # 视频路径（可能是URL）
        self.debug = debug
        self.is_dragging = False
        self.target_position = 0
        self.range_supported = True  # 服务器是否支持Range请求
        self.reloading = False  # 是否正在重新加载视频
        self._is_to_play = False
        self._itp2 = False

        self.init_ui()

    def init_ui(self):
        self.video_label = QLabel()
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setMinimumSize(640, 360)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.audio_visualizer = AudioVisualizer()
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMinimumHeight(150)

        # 调试控件
        self.debug_widgets = [self.audio_visualizer, self.log_view]
        for widget in self.debug_widgets:
            widget.hide()

        # 控制按钮和设备选择
        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.toggle_play)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop)

        self.device_label = QLabel("音频设备:")
        self.device_combo = QComboBox()
        self.device_combo.currentIndexChanged.connect(self.on_device_changed)

        self.volume_label = QLabel("音量:")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)

        # 进度条 - 单独放在一行
        self.progress_bar = QSlider(Qt.Horizontal)
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setStyleSheet(
            """
            QSlider::horizontal {
                min-height: 20px;
                background: #f0f0f0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #336699;
                width: 18px;
                margin: -8px 0;
                border-radius: 8px;
            }
        """
        )
        self.progress_bar.sliderPressed.connect(self.on_progress_pressed)
        self.progress_bar.sliderReleased.connect(self.on_progress_released)
        self.progress_bar.sliderMoved.connect(self.on_progress_moved)
        self.progress_bar.setSingleStep(100)
        self.progress_bar.setPageStep(1000)
        self.progress_bar.show()

        # 按钮和控制选项布局（第一行）
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addSpacing(20)  # 添加间距
        controls_layout.addWidget(self.device_label)
        controls_layout.addWidget(self.device_combo)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(self.volume_label)
        controls_layout.addWidget(self.volume_slider)
        controls_layout.addStretch()  # 右侧拉伸，将控件向左推

        # 进度条布局（第二行）
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_bar)  # 进度条单独一行，占满宽度

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.video_label)

        if self.debug:
            for widget in self.debug_widgets:
                widget.show()
                main_layout.addWidget(widget)

        # 添加控制布局和进度条布局
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(progress_layout)

        # 设置布局比例
        main_layout.setStretch(0, 8)  # 视频区域
        if self.debug:
            main_layout.setStretch(1, 2)  # 可视化区域
            main_layout.setStretch(2, 2)  # 日志区域
            main_layout.setStretch(3, 1)  # 控制按钮区域
            main_layout.setStretch(4, 1)  # 进度条区域
        else:
            main_layout.setStretch(1, 1)  # 控制按钮区域
            main_layout.setStretch(2, 1)  # 进度条区域

        self.setLayout(main_layout)

    def log(self, message):
        if self.debug:
            self.log_view.append(f"[{time.strftime('%H:%M:%S')}] {message}")
            self.log_view.verticalScrollBar().setValue(
                self.log_view.verticalScrollBar().maximum()
            )
        logging.info(message)

    def on_progress_pressed(self):
        if not self.video_loaded or self.duration == 0 or self.reloading:
            return
        self.is_dragging = True
        if self.is_playing:
            self.video_thread.pause()
            if self.audio_thread:
                self.audio_thread.pause()
            self.log("拖动进度条中...")

    def on_progress_moved(self, position):
        if (
            not self.is_dragging
            or not self.video_loaded
            or self.duration == 0
            or self.reloading
        ):
            return

        position = max(0, min(position, self.duration))
        self.progress_bar.setValue(position)
        self.target_position = position
        pos_sec = position / 1000
        self.log(f"拖动到: {pos_sec:.1f}秒")

    def on_progress_released(self):
        if (
            not self.is_dragging
            or not self.video_loaded
            or self.duration == 0
            or self.reloading
        ):
            return

        current_pos_sec = self.current_pos / 1000
        target_pos_sec = self.target_position / 1000

        # 检查是否是向前拖动并且服务器不支持Range请求
        print(
            "range: "
            + str(self.range_supported)
            + " is before: "
            + str(target_pos_sec < current_pos_sec)
        )
        if target_pos_sec < current_pos_sec and not self.range_supported:
            self.log("检测到向前拖动且服务器不支持部分请求，需要重新加载视频...")
            self._reload_and_seek(self.target_position)
        else:
            # 正常定位
            self.set_play_position(self.target_position)

        self.is_dragging = False
        if self.is_playing and not self.reloading:
            self._resume_playback()

    def _reload_and_seek(self, target_pos_ms):
        """重新加载视频并定位到目标位置"""
        # if self.reloading:
        #     return

        # self.reloading = True
        # self.video_label.setText("正在重新加载视频...")
        print(f"重新加载视频并定位到 {target_pos_ms/1000:.2f}秒")

        # # 显示加载进度
        # progress_dialog = QProgressDialog("正在重新加载视频...", "取消", 0, 100, self)
        # progress_dialog.setWindowTitle("请稍候")
        # progress_dialog.setWindowModality(Qt.WindowModal)
        # progress_dialog.setValue(10)

        # # 停止当前播放
        # self.stop()
        # progress_dialog.setValue(30)

        # # 重新加载视频
        # try:
        #     # 关闭当前视频线程
        #     if self.video_thread and self.video_thread.isRunning():
        #         self.video_thread.stop()
        #         self.video_thread.wait()

        #     progress_dialog.setValue(50)

        #     # 重新初始化视频线程
        #     self.video_loaded = False
        #     self.video_thread = VideoCaptureThread(self.video_path)
        #     self.video_thread.frame_ready.connect(self.update_frame)
        #     self.video_thread.error_occurred.connect(self.handle_error)
        #     self.video_thread.duration_updated.connect(self.update_duration)
        #     self.video_thread.audio_spec_ready.connect(
        #         lambda spec: self._on_audio_ready_after_reload(spec, target_pos_ms)
        #     )
        #     self.video_thread.start()

        #     progress_dialog.setValue(70)

        #     # 等待视频加载完成
        #     start_time = time.time()
        #     while not self.video_loaded and time.time() - start_time < 10:  # 最多等待10秒
        #         QApplication.processEvents()
        #         time.sleep(0.1)
        #         progress = 70 + int((time.time() - start_time) / 10 * 20)
        #         progress_dialog.setValue(min(progress, 90))

        #     if not self.video_loaded:
        #         raise Exception("视频加载超时")

        #     progress_dialog.setValue(100)

        # except Exception as e:
        #     self.log(f"重新加载视频失败: {str(e)}")
        #     QMessageBox.critical(self, "加载失败", f"无法重新加载视频: {str(e)}")
        # finally:
        #     progress_dialog.close()
        #     self.reloading = False
        #     self.video_label.setText("")
        # self.play_btn.click()
        self.video_loaded = False
        self._to_play_dur = target_pos_ms
        self._is_to_play = True
        self.load_video(self.video_path)

    def _on_audio_ready_after_reload(self, audio_spec, target_pos_ms):
        """重新加载后音频准备就绪的回调"""
        self.init_audio(audio_spec)

        # 定位到目标位置
        if self.video_loaded:
            self.set_play_position(target_pos_ms)
            self.is_playing = True
            self.play_btn.setText("Pause")

            # 开始播放
            if self.video_thread:
                self.video_thread.pause()  # 切换播放状态
            if self.audio_thread:
                self.audio_thread.pause()  # 切换播放状态

    def _resume_playback(self):
        if self.video_thread and not self.is_dragging and not self.reloading:
            # 获取当前视频时间戳
            pos_sec = self.target_position / 1000

            # 手动同步音频到视频时间戳
            if self.audio_thread:
                self.audio_thread.manual_sync(pos_sec)

            # 恢复播放
            self.video_thread.pause()
            if self.audio_thread:
                self.audio_thread.pause()

    def load_video(self, video_path: str):
        """加载视频，先检查Range支持"""
        if self.video_loaded or self.reloading:
            return

        self.video_path = video_path
        self.log(f"开始加载视频: {video_path}")

        # 检查是否是网络视频
        if video_path.startswith(("http://", "https://")):
            # 检测服务器是否支持Range请求
            self.log("检测服务器是否支持部分请求...")
            self.range_supported, msg = RangeSupportChecker.check(video_path)
            self.log(f"Range请求支持: {self.range_supported} - {msg}")

            # 如果不支持Range请求，提示用户可能会有性能影响
            # if not self.range_supported:
            #     QMessageBox.information(
            #         self,
            #         "服务器限制",
            #         "检测到服务器不支持部分请求，向前拖动进度条时可能需要重新加载视频，这会影响播放体验。"
            #     )

        # 开始加载视频
        self._start_video_loading()

    def _start_video_loading(self):
        """开始加载视频"""
        try:
            self.progress_bar.setValue(0)
            self.duration = 0
            self.current_pos = 0
            self.target_position = 0

            self.video_thread = VideoCaptureThread(self.video_path)
            self.video_thread.frame_ready.connect(self.update_frame)
            self.video_thread.error_occurred.connect(self.handle_error)
            self.video_thread.duration_updated.connect(self.update_duration)
            self.video_thread.audio_spec_ready.connect(self.init_audio)
            self.video_thread.start()
            self.video_loaded = True
            self.log("视频加载完成，点击Play开始播放")
            if self._is_to_play:
                self._itp2 = True
        except Exception as e:
            QMessageBox.critical(self, "加载错误", f"无法加载视频: {str(e)}")
            self.log(f"加载错误: {str(e)}")

    def init_audio(self, audio_spec):
        if not audio_spec or not has_ffmpeg:
            self.log("无可用音频或ffmpeg，隐藏音频控制")
            self.device_label.hide()
            self.device_combo.hide()
            self.volume_label.hide()
            self.volume_slider.hide()
            return

        try:
            # 如果已有音频线程，先停止
            if self.audio_thread and self.audio_thread.isRunning():
                self.audio_thread.stop()
                self.audio_thread.wait()

            self.log("初始化音频线程")
            self.audio_thread = AudioPlayThread()
            self.audio_thread.audio_error.connect(self.handle_audio_error)
            self.audio_thread.device_list_updated.connect(self.update_device_list)
            if self.debug:
                self.audio_thread.audio_data_ready.connect(
                    self.audio_visualizer.update_audio
                )
            self.audio_thread.ffmpeg_stderr.connect(self.handle_ffmpeg_error)
            self.audio_thread.init_audio(audio_spec, self.video_path)
            self.audio_thread.start()
            self.audio_thread.set_volume(self.volume_slider.value())
        except Exception as e:
            self.handle_audio_error(f"音频初始化失败: {str(e)}")

    def update_device_list(self, devices):
        self.device_combo.clear()
        for i, name, _, _ in devices:
            self.device_combo.addItem(name, i)
        if devices:
            for idx, (i, name, _, is_virtual) in enumerate(devices):
                if not is_virtual:
                    self.device_combo.setCurrentIndex(idx)
                    self.on_device_changed(idx)
                    return
            self.device_combo.setCurrentIndex(0)
            self.on_device_changed(0)

    def on_device_changed(self, index):
        if not self.audio_thread or index < 0:
            return
        device_index = self.device_combo.itemData(index)
        self.log(f"切换音频设备: {self.device_combo.currentText()}")
        self.audio_thread.set_audio_device(device_index)

    def on_volume_changed(self, value):
        if self.audio_thread:
            self.audio_thread.set_volume(value)

    def update_frame(self, q_image, timestamp):
        if self._itp2:
            self._is_to_play = False
            self._itp2 = False
            self.set_play_position(self._to_play_dur)
            self.play_btn.click()
            self.play_btn.click()
        if not self.is_dragging and not self.reloading:
            scaled_img = q_image.scaled(
                self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.video_label.setPixmap(QPixmap.fromImage(scaled_img))

            # 更新进度条
            self.current_pos = int(timestamp * 1000)
            if abs(self.progress_bar.value() - self.current_pos) > 100:
                self.progress_bar.setValue(self.current_pos)

    def update_duration(self, duration):
        self.duration = duration
        self.progress_bar.setRange(0, duration)
        self.log(f"视频总时长: {duration/1000:.1f}秒")

    def toggle_play(self):
        if not self.video_loaded or self.reloading:
            QMessageBox.warning(self, "未准备好", "请先加载视频")
            return

        self.is_playing = not self.is_playing

        if self.is_playing:
            # 从暂停状态恢复播放时进行同步
            if self.video_thread.paused:
                # 获取当前视频时间戳
                current_video_time = self.current_pos / 1000

                # 手动同步音频
                if self.audio_thread:
                    self.audio_thread.manual_sync(current_video_time)

                self.video_thread.pause()
            else:
                self.video_thread.restart()

            if self.audio_thread and self.audio_thread.paused:
                self.audio_thread.pause()
            self.play_btn.setText("Pause")
            self.log("开始播放")
        else:
            if not self.video_thread.paused:
                self.video_thread.pause()

            if self.audio_thread and not self.audio_thread.paused:
                self.audio_thread.pause()
            self.play_btn.setText("Play")
            self.log("已暂停")

    def stop(self):
        self.log("停止播放")
        if self.audio_thread and self.audio_thread.isRunning():
            self.audio_thread.stop()
            self.audio_thread.wait()
            self.audio_thread = None

        if self.video_thread and self.video_thread.isRunning():
            self.video_thread.stop()

        self.is_playing = False
        self.current_pos = 0
        self.target_position = 0
        self.play_btn.setText("Play")
        self.progress_bar.setValue(0)
        self.is_dragging = False

    def set_play_position(self, pos_ms):
        if not self.video_loaded or self.duration == 0 or self.reloading:
            return

        pos_ms = max(0, min(pos_ms, self.duration))
        pos_sec = pos_ms / 1000
        self.log(f"定位到: {pos_sec:.1f}秒")

        self.video_thread.set_position(pos_ms)
        if self.audio_thread:
            # 定位时同步音频
            self.audio_thread.seek(pos_sec)

        self.current_pos = pos_ms
        self.progress_bar.setValue(pos_ms)

    def handle_error(self, msg):
        self.log(f"视频提示: {msg}")

    def handle_audio_error(self, msg):
        self.log(f"音频提示: {msg}")

    def handle_ffmpeg_error(self, msg):
        self.log(f"FFmpeg: {msg}")

    def closeEvent(self, event):
        self.stop()
        event.accept()


class MainWindow(QMainWindow):
    def __init__(self, video_path=None, debug=False):
        super().__init__()
        self.setWindowTitle("视频播放器（重新加载而非下载）")
        self.setGeometry(100, 100, 1400, 900)

        self.central_widget = OpenCVVideoWidget(debug=debug)
        self.setCentralWidget(self.central_widget)

        if video_path:
            self.central_widget.load_video(video_path)
        else:
            # 默认使用测试视频
            self.central_widget.load_video(
                "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_1MB.mp4"
            )

    def closeEvent(self, event):
        self.central_widget.close()
        event.accept()


VLCVideoWidget = OpenCVVideoWidget


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        debug_mode = "--debug" in sys.argv
        video_path = (
            sys.argv[1] if (len(sys.argv) > 1 and sys.argv[1] != "--debug") else None
        )

        window = MainWindow(video_path=video_path, debug=debug_mode)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "致命错误", f"程序崩溃: {str(e)}")
        print(f"错误详情: {e}")
        sys.exit(1)
