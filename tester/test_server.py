from flask import Flask, request, send_file, Response
import os
import time
from threading import Lock

app = Flask(__name__)

# 限速配置 (10KB/s)
LIMIT_BYTES_PER_SECOND = 100 * 1024  # 10KB
CHUNK_SIZE = 1024  # 每次发送1KB
SLEEP_INTERVAL = CHUNK_SIZE / LIMIT_BYTES_PER_SECOND  # 每次发送后的休眠时间

# 存储要提供下载的文件目录
UPLOAD_FOLDER = "files_to_serve"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 用于控制并发下载的锁
download_lock = Lock()


def get_file_path(filename):
    """获取文件的完整路径"""
    return os.path.join(UPLOAD_FOLDER, filename)


def rate_limited_file_reader(file_path):
    """生成器函数，限速读取文件内容"""
    with open(file_path, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            yield data
            # 控制速度：每发送CHUNK_SIZE字节后休眠相应时间
            time.sleep(SLEEP_INTERVAL)


@app.route("/files/<filename>")
def serve_file(filename):
    """提供文件下载，限速10KB/s"""
    file_path = get_file_path(filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return f"文件 {filename} 不存在", 404

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 设置响应头
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Length": str(file_size),
        "Accept-Ranges": "bytes",  # 支持断点续传
    }

    # 使用限速生成器提供文件内容
    return Response(
        rate_limited_file_reader(file_path),
        headers=headers,
        mimetype="application/octet-stream",
    )


@app.route("/range-test/<filename>")
def range_test(filename):
    """测试断点续传支持的端点"""
    file_path = get_file_path(filename)

    if not os.path.exists(file_path):
        return f"文件 {filename} 不存在", 404

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("Range", None)

    # 如果没有Range头，返回完整文件
    if not range_header:
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes",
        }
        return Response(
            rate_limited_file_reader(file_path),
            headers=headers,
            mimetype="application/octet-stream",
        )

    # 处理Range请求
    try:
        # 解析Range头 (格式: bytes=start-end)
        range_start, range_end = range_header.replace("bytes=", "").split("-")
        range_start = int(range_start)
        range_end = int(range_end) if range_end else file_size - 1

        # 确保范围有效
        if range_start > range_end or range_start >= file_size:
            return "Invalid range", 416

        # 调整结束范围
        range_end = min(range_end, file_size - 1)

        # 生成部分文件内容的生成器
        def limited_range_reader():
            with open(file_path, "rb") as f:
                f.seek(range_start)
                remaining = range_end - range_start + 1
                while remaining > 0:
                    read_size = min(remaining, CHUNK_SIZE)
                    data = f.read(read_size)
                    if not data:
                        break
                    yield data
                    remaining -= read_size
                    time.sleep(SLEEP_INTERVAL)

        # 返回部分内容
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Range": f"bytes {range_start}-{range_end}/{file_size}",
            "Content-Length": str(range_end - range_start + 1),
            "Accept-Ranges": "bytes",
        }

        return Response(
            limited_range_reader(),
            status=206,  # Partial Content
            headers=headers,
            mimetype="application/octet-stream",
        )

    except Exception as e:
        return f"处理范围请求时出错: {str(e)}", 400


@app.route("/no-range/<filename>")
def no_range_serve(filename):
    """提供文件下载但不支持断点续传，用于测试兼容性"""
    file_path = get_file_path(filename)

    if not os.path.exists(file_path):
        return f"文件 {filename} 不存在", 404

    file_size = os.path.getsize(file_path)

    # 不设置Accept-Ranges头，表示不支持断点续传
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Length": str(file_size),
        # 注意：这里没有设置Accept-Ranges头
    }

    return Response(
        rate_limited_file_reader(file_path),
        headers=headers,
        mimetype="application/octet-stream",
    )


if __name__ == "__main__":
    print(f"限速文件服务器启动中...")
    print(
        f"限速: {LIMIT_BYTES_PER_SECOND} bytes/s ({LIMIT_BYTES_PER_SECOND/1024:.2f}KB/s)"
    )
    print(f"请将测试文件放入 {UPLOAD_FOLDER} 目录")
    print(f"访问 http://localhost:5000/files/文件名 以下载文件（支持断点续传）")
    print(f"访问 http://localhost:5000/no-range/文件名 以下载文件（不支持断点续传）")
    app.run(host="0.0.0.0", port=5000, debug=True)
