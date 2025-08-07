import sys, os
import re
from PySide6 import QtWidgets, QtCore
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
import mainWindow  # 导入您的主窗口模块


class Launcher(QtCore.QObject):
    def __init__(self):
        super().__init__()

        # 存储提取到的端口号
        self.port = None
        # 标志位：是否处于导出状态
        self.exporting = False
        # 主窗口实例
        self.mw = None

        # 创建QProcess用于启动外部程序
        self.process = QtCore.QProcess()
        self.process.setProgram("./AssetRipperCore/AssetRipper.GUI.Free.exe")
        self.process.setArguments(["--launch-browser=False"])

        # 连接信号与槽（保持持续监听，不中途断开）
        self.process.readyReadStandardOutput.connect(self.on_stdout_ready)
        self.process.errorOccurred.connect(self.on_process_error)
        self.process.finished.connect(self.on_process_finished)
        # 新增：进程启动后获取PID的信号
        self.process.started.connect(self.on_process_started)

        # 启动外部进程
        self.start_external_process()

    def start_external_process(self):
        """启动外部进程"""
        print("启动 AssetRipper.GUI.Free.exe ...")
        self.process.start()
        if not self.process.waitForStarted():
            print("无法启动外部进程")
            # 如果启动失败，直接显示主窗口
            self.show_main_window()

    def on_process_started(self):
        """进程启动后获取PID并发送给主窗口"""
        # 获取进程PID
        pid = self.process.processId()
        print(f"外部进程已启动，PID: {pid}")

        # 向主窗口反馈PID（如果主窗口已创建）
        if self.mw and hasattr(self.mw, "setProcessPid"):
            self.mw.setProcessPid(pid)
        else:
            # 如果主窗口尚未创建，存储PID待后续发送
            self.stored_pid = pid

    def on_stdout_ready(self):
        """处理进程输出（持续监听，不中断）"""
        # 读取所有可用输出
        output = (
            self.process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        )

        # 按行处理输出
        for line in output.splitlines():
            # 查找端口号（保持原有逻辑）
            if not self.port:
                port_match = re.search(
                    r"Now listening on: http://127.0.0.1:(\d+)", line
                )
                if port_match:
                    self.port = port_match.group(1)
                    print(f"提取到端口号: {self.port}")
                    self.show_main_window()

            # 处理导出相关信息
            self.handle_export_output(line)

    def handle_export_output(self, line):
        """处理导出相关的输出信息"""
        # 1. 检测导出开始（支持两种开始标志）
        if (
            "Export : Starting export" in line
            or "Export : Starting primary content export" in line
        ):
            self.exporting = True
            print(f"检测到导出开始，启用进度监听: {line}")
            return

        # 2. 检测导出结束（支持两种结束标志）
        if (
            "Export : Finished post-export" in line
            or "Export : Finished exporting primary content." in line
        ):
            self.exporting = False
            print(f"检测到导出完成，关闭进度监听: {line}")
            if self.mw and hasattr(self.mw, "finishExportingEvent"):
                self.mw.finishExportingEvent()
            return

        # 3. 当导出标志位开启时，处理进度信息（原有逻辑不变）
        if self.exporting:
            # 处理导出进度
            progress_match = re.search(
                r"ExportProgress : \((\d+)/(\d+)\) Exporting '([^']+)'", line
            )
            if progress_match:
                current = progress_match.group(1)
                total = progress_match.group(2)
                filename = progress_match.group(3)
                print(f"导出进度: {current}/{total} - {filename}")
                if self.mw and hasattr(self.mw, "handleExportingOutPut"):
                    self.mw.handleExportingOutPut(current, total, filename)
                return

            # 处理反编译信息
            decompile_match = re.search(r"Decompiling ([\w\-]+)", line)
            if decompile_match:
                name = decompile_match.group(1)
                print(f"正在反编译: {name}")
                if self.mw and hasattr(self.mw, "handleDecompilingMessage"):
                    self.mw.handleDecompilingMessage(name)
                return

            # 处理保存信息
            saving_match = re.search(r"Export : Saving (.*)", line)
            if saving_match:
                content = saving_match.group(1)
                print(f"正在保存: {content}")
                if self.mw and hasattr(self.mw, "handleSavingMessage"):
                    self.mw.handleSavingMessage(content)
                return

    def show_main_window(self):
        """显示主窗口"""
        if self.mw is None:
            print("显示主窗口")
            self.mw = mainWindow.MainWindow()
            # 传递端口号给主窗口
            if self.port and hasattr(self.mw, "set_port"):
                self.mw.set_port(self.port)
            # 检查是否有存储的PID需要发送
            if hasattr(self, "stored_pid") and hasattr(self.mw, "setProcessPid"):
                self.mw.setProcessPid(self.stored_pid)
                delattr(self, "stored_pid")  # 发送后删除存储的PID
            self.mw.show()

    def on_process_error(self, error):
        """处理进程错误"""
        error_str = self.process.errorString()
        print(f"进程错误: {error_str}")
        # 发生错误时显示主窗口
        self.show_main_window()

    def on_process_finished(self, exit_code, exit_status):
        """进程结束时的处理"""
        print(f"外部进程已结束，退出代码: {exit_code}")


def enable_remote_debugging(port=9222):
    """设置环境变量，启用远程调试端口"""
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = str(port)
    print(f"远程调试已启用，端口: {port}")
    print(f"请在Chrome浏览器中访问: http://localhost:{port}")


if __name__ == "__main__":
    enable_remote_debugging()
    # 添加 Chromium 命令行参数禁用 CORS
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
        "--disable-web-security --allow-file-access-from-files"
    )

    # 创建应用实例
    qa = QtWidgets.QApplication(sys.argv)

    # 通过QWebEngineProfile设置全局属性
    profile = QWebEngineProfile.defaultProfile()
    settings = profile.settings()

    # 允许加载不安全内容
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True
    )
    # 允许本地内容访问远程URL
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
    )

    # 启动启动器
    launcher = Launcher()

    # 进入事件循环
    sys.exit(qa.exec())
