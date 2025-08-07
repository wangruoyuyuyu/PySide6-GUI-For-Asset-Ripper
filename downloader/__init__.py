try:
    import ui_downloadingWindow
except (ImportError, ModuleNotFoundError):
    try:
        from . import ui_downloadingWindow
    except (ImportError, ModuleNotFoundError):
        import ui_downloadingWindow
from PySide6 import QtWidgets, QtCore
import os, time, requests, _thread
from contextlib import closing


class Downloader(ui_downloadingWindow.Ui_Dialog, QtWidgets.QDialog):
    chunkSize = 1024 * 10  # 24  # 1MB 块大小
    loop = 5  # 最大重试次数

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.progressBar.setRange(0, 100)

        self.value = 0
        self.stopped = False
        self.isDownloaded = False
        self.check_interval = QtCore.QTimer()
        self.check_interval.timeout.connect(self.checkprog)
        self.check_interval.start()

    def checkprog(self):
        if self.isDownloaded:
            self.progressBar.setValue(100)
            self.buttonBox.buttons()[0].setText("OK")
            self.label.setText("Finished Saving")
        else:
            self.label.setText("Saving...")
            self.progressBar.setValue(self.value)
            self.buttonBox.buttons()[0].setText("Cancel")

    def check_support_range(self, url):
        """检测服务器是否支持Partial Request（断点续传）"""
        try:
            # 发送HEAD请求测试Range支持
            test_headers = self.headers.copy()
            test_headers["Range"] = "bytes=0-1"  # 请求前2字节
            response = requests.head(
                url, headers=test_headers, timeout=10, allow_redirects=True
            )
            # 支持断点续传的服务器会返回206 Partial Content
            return response.status_code == 206
        except Exception as e:
            print(f"检测断点续传支持失败: {e}")
            return False

    def file_download(self, fileUrl, filePath):
        self.buttonBox.buttons()[0].setText("Cancel")
        self.value = 0
        self.stopped = False
        _thread.start_new_thread(self._file_download, (fileUrl, filePath))

    def _file_download(self, fileUrl, filePath):
        """下载文件（支持断点续传，兼容不支持的服务器）"""
        # 检测服务器是否支持断点续传
        support_range = self.check_support_range(fileUrl)
        print(f"服务器{'支持' if support_range else '不支持'}断点续传")

        # 获取文件总大小
        try:
            head_response = requests.head(
                fileUrl, headers=self.headers, allow_redirects=True, timeout=10
            )
            fileSize = int(head_response.headers.get("content-length", 0))
            if not fileSize:
                head_response = requests.get(
                    fileUrl,
                    headers=self.headers,
                    allow_redirects=True,
                    timeout=10,
                    stream=True,
                )
                fileSize = int(head_response.headers.get("content-length", 0))
            self.chunkSize = int(fileSize / 100) if int(fileSize / 100) else 1
            print(fileSize)
        except Exception as e:
            print(f"获取文件大小失败: {e}")
            return False

        tmpSize = 0  # 已下载大小
        n = 0  # 重试计数
        self.isDownloaded = False

        while n < self.loop:
            # 检查本地已下载大小
            if os.path.exists(filePath):
                tmpSize = os.path.getsize(filePath)
                # 文件已完整下载
                if tmpSize == fileSize and fileSize > 0:
                    self.isDownloaded = True
                    break

            # 构建请求头（仅在支持断点续传时使用Range）
            _headers = self.headers.copy()
            if support_range and tmpSize > 0 and tmpSize < fileSize:
                _headers["Range"] = f"bytes={tmpSize}-{fileSize}"
                print(f"继续下载: 从 {tmpSize} 字节到 {fileSize} 字节")
            else:
                # 不支持断点续传或首次下载，从头开始
                tmpSize = 0

            # 不支持断点续传且有部分文件时，删除旧文件重新下载
            if not support_range and tmpSize > 0 and tmpSize < fileSize:
                print(f"服务器不支持断点续传，删除不完整文件并重下")
                os.remove(filePath)
                tmpSize = 0

            contentSize = 0  # 本次下载的块数量
            remainSize = (fileSize - tmpSize) / self.chunkSize if fileSize else 0
            filename = os.path.basename(filePath)
            st = time.perf_counter()  # 计时开始
            print("down started", remainSize, tmpSize)

            if remainSize > 0 or tmpSize == 0:
                try:
                    # 发送下载请求
                    with closing(
                        requests.get(fileUrl, headers=_headers, stream=True, timeout=30)
                    ) as _response, open(
                        filePath, "ab" if tmpSize > 0 else "wb"
                    ) as file:

                        # 检查响应状态
                        if _response.status_code not in [200, 206]:
                            print(f"下载失败，状态码: {_response.status_code}")
                            n += 1
                            continue

                        # 流式写入文件
                        for content in _response.iter_content(
                            chunk_size=self.chunkSize
                        ):
                            print("downing...")
                            if self.stopped:
                                break
                            if content:
                                file.write(content)
                                timeTook = time.perf_counter() - st
                                contentSize += len(content) / self.chunkSize

                                # 显示进度和速度
                                self.speed_handle(
                                    contentSize + (tmpSize / self.chunkSize),
                                    fileSize / self.chunkSize,
                                )
                                downloadSpeed = (
                                    contentSize / timeTook if timeTook > 0 else 0
                                )
                                remainingTime = (
                                    int(
                                        (timeTook / contentSize)
                                        * (remainSize - contentSize)
                                    )
                                    if contentSize > 0
                                    else 0
                                )

                                print(
                                    f"[平均速度: \033[1;31m{downloadSpeed:.2f}MiB/s\033[0m, "
                                    f"剩余时间: \033[1;32m{remainingTime}s\033[0m, "
                                    f"文件大小: \033[1;34m{fileSize/self.chunkSize:.2f}MiB\033[0m]",
                                    flush=True,
                                    end=" ",
                                )

                except Exception as e:
                    print(f"下载出错: {e}，将重试 ({n+1}/{self.loop})")
                    import traceback

                    print(traceback.format_exc())
                    n += 1
                    continue

            # 验证文件完整性
            if (
                os.path.exists(filePath)
                and os.path.getsize(filePath) == fileSize
                and fileSize > 0
            ):
                self.isDownloaded = True
                break
            else:
                n += 1
                print(f"文件不完整，重试 ({n}/{self.loop})")

        return self.isDownloaded

    def speed_handle(self, process, file_length):
        """显示下载进度条和速度信息"""
        if process != file_length:
            num = process / file_length
            progress = ": \033[1;33m{:.2f}\033[0m%|{}{}| ".format(
                float(num * 100), "■" * round(num * 20), "□" * round((1 - num) * 20)
            )
            self.value = num * 100
        else:
            progress = " \033[1;33m{}\033[0m% |{}|".format(100, "■" * 50)
            self.value = 100
        print(progress, flush=True, end="")

    def closeEvent(self, arg__1):
        self.stopped = True
        return super().closeEvent(arg__1)


if __name__ == "__main__":
    qa = QtWidgets.QApplication(list())
    d = Downloader()
    d.show()
    d.file_download("http://localhost:5000/files/Audio_2.ogg", "test.wdown")
    qa.exec()
