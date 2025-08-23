import psutil
import win32gui
import win32process


class StatusMachine(object):
    known_pid = None


def get_window_info(pid):
    """获取指定进程 ID 的所有窗口信息"""
    windows = []

    def callback(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                title = win32gui.GetWindowText(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                windows.append(
                    {
                        "hwnd": hwnd,
                        "title": title,
                        "position": (rect[0], rect[1]),  # 左上角坐标
                        "size": (rect[2] - rect[0], rect[3] - rect[1]),  # 宽高
                    }
                )

    win32gui.EnumWindows(callback, None)
    return windows


def find_process_by_name(process_name):
    """查找指定名称的进程并返回其 PID"""
    for proc in psutil.process_iter(["name", "pid"]):
        if proc.info["name"].lower() == process_name.lower():
            return proc.info["pid"]
    return None


# 主程序
if __name__ == "__main__":
    # 进程名称
    target_process = "AssetRipper.GUI.Free.exe"

    # 查找进程
    pid = find_process_by_name(target_process)
    if not pid:
        print(f"未找到进程: {target_process}")
    else:
        print(f"找到进程，PID: {pid}")

        # 获取窗口信息
        windows = get_window_info(pid)
        if windows:
            print(f"找到 {len(windows)} 个窗口:")
            for window in windows:
                print(f"  - 句柄: {window['hwnd']}")
                print(f"  - 标题: {window['title']}")
                print(f"  - 位置: {window['position']}")
                print(f"  - 大小: {window['size']}")
                print("  -------------------")
        else:
            print("未找到可见窗口或窗口未启用")
