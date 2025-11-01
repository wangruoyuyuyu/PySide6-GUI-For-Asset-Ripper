import requests
import _thread
import sys,importlib.util
if sys.version_info.minor==9:
    try:
        from . import parser
    except (ImportError,ModuleNotFoundError):
        parser=None
else:
    import parser

def import_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if not parser:
    parser=import_from_file("parser","./parser.py")

import re
import chardet  # 导入chardet库用于编码检测
from urllib.parse import quote, unquote
from json import dumps

PORT = 18374


class StatusMachine(object):
    onApiCallFinished = lambda res: (res)
    onReplaceFileFinished = lambda res: (res)

    def __init__(self):
        pass


def decode_response(response):
    """通用解码函数，使用chardet检测编码并解码"""
    # 检测响应内容的编码
    detected_encoding = chardet.detect(response.content)["encoding"]

    # 处理可能的编码检测错误
    if detected_encoding is None:
        detected_encoding = "utf-8"  # 默认使用utf-8

    try:
        # 尝试用检测到的编码解码
        return response.content.decode(detected_encoding)
    except UnicodeDecodeError:
        # 解码失败时 fallback 到utf-8并忽略错误
        return response.content.decode("utf-8", errors="ignore")


def open_file(port=PORT):
    _thread.start_new_thread(_open_file, (port,))


def _open_file(port=PORT):
    res = requests.post(
        f"http://localhost:{port}/LoadFile",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"value": "Open File"},
    )
    # 修改响应处理方式
    decoded_content = decode_response(res)
    # 将解码后的内容附加到响应对象，方便后续使用
    res.decoded_text = decoded_content
    StatusMachine.onApiCallFinished(res)


def open_folder(port=PORT):
    _thread.start_new_thread(_open_folder, (port,))


def _open_folder(port=PORT):
    res = requests.post(
        f"http://localhost:{port}/LoadFolder",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"value": "Open Folder"},
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onApiCallFinished(res)


# 注意：原代码中有重复定义的_open_file函数，这里保留一个
def _open_file(port=PORT):
    res = requests.post(
        f"http://localhost:{port}/LoadFile",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"value": "Open File"},
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onApiCallFinished(res)


def reset(port=PORT):
    _thread.start_new_thread(_reset, (port,))


def _reset(port=PORT):
    res = requests.post(
        f"http://localhost:{port}/Reset",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"value": "Reset"},
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onApiCallFinished(res)


def check_is_file(port=PORT) -> bool:
    res = requests.get(f"http://localhost:{port}/")
    # 使用解码后的内容进行判断
    decoded_content = decode_response(res)
    return "View Loaded Files" in decoded_content


def check_version(port=PORT) -> dict:
    res = requests.get(f"http://localhost:{port}/")
    decoded_content = decode_response(res)
    return parser.extract_version_info(decoded_content)


def get_settings(port=PORT) -> dict:
    res = requests.get(f"http://localhost:{port}/Settings/Edit")
    decoded_content = decode_response(res)
    return parser.extract_form_data(decoded_content), parser.parse_form_names(
        decoded_content
    )


def get_loaded_files(port=PORT, path={"P": []}, from_url=False, url="") -> dict:
    if not from_url:
        res = requests.get(
            f"http://localhost:{port}/Bundles/View?path={quote(dumps(path))}",
            headers={"host": "127.0.0.1"},
        )
    else:
        if url.startswith("/"):
            res = requests.get(f"http://localhost:{port}{url}")
        elif url.startswith("http"):
            res = requests.get(url)
        else:
            res = requests.get(f"http://localhost:{port}/{url}")

    decoded_content = decode_response(res)
    return parser.parse(decoded_content)


def get_loaded_collections(port=PORT, path={"P": []}, from_url=False, url="") -> dict:
    if not from_url:
        res = requests.get(
            f"http://localhost:{port}/Collections/View?path={quote(dumps(path))}",
            headers={"host": "127.0.0.1"},
        )
    else:
        if url.startswith("/"):
            res = requests.get(f"http://localhost:{port}{url}")
        elif url.startswith("http"):
            res = requests.get(url)
        else:
            res = requests.get(f"http://localhost:{port}/{url}")

    decoded_content = decode_response(res)
    return parser.extract_tables(decoded_content)


def get_loaded_assets(port=PORT, path={"P": []}, from_url=False, url="") -> dict:
    if not from_url:
        res = requests.get(
            f"http://localhost:{port}/Assets/View?path={quote(dumps(path))}",
            headers={"host": "127.0.0.1"},
        )
    else:
        if url.startswith("/"):
            res = requests.get(f"http://localhost:{port}{url}")
        elif url.startswith("http"):
            res = requests.get(url)
        else:
            res = requests.get(f"http://localhost:{port}/{url}")

    decoded_content = decode_response(res)
    return parser.parse_tab_tables(decoded_content)


def get_loaded_text(
    port=PORT, path={"P": []}, type_="Yaml", from_url=False, url=""
) -> dict:
    if not from_url:
        res = requests.get(
            f"http://localhost:{port}/Assets/{type_}?path={quote(dumps(path))}",
            headers={"host": "127.0.0.1"},
        )
    else:
        if url.startswith("/"):
            res = requests.get(f"http://localhost:{port}{url}")
        elif url.startswith("http"):
            res = requests.get(url)
        else:
            res = requests.get(f"http://localhost:{port}/{url}")

    return decode_response(res)


def get_loaded_font_name(url, port=PORT):
    if url.startswith("/"):
        res = requests.get(f"http://localhost:{port}{url}")
    elif url.startswith("http"):
        res = requests.get(url)
    else:
        res = requests.get(f"http://localhost:{port}/{url}")

    if "Content-Disposition" in res.headers.keys():
        return parser.extract_filename(res.headers["Content-Disposition"])
    return None


def get_video_name(url, port=PORT):
    full_url = f"http://localhost:{port}{url}"
    header_res = requests.get(full_url, stream=True)
    cd = header_res.headers.get("content-disposition")
    return extract_filename(cd)


def extract_filename(content_disposition: str) -> str:
    """
    从Content-Disposition头部提取文件名，优先处理filename*=UTF-8''格式

    参数:
        content_disposition: Content-Disposition头部字符串
    返回:
        解码后的文件名，优先使用filename*的值
    """
    if not content_disposition:
        return ""

    # 1. 优先匹配 filename*=UTF-8'' 格式（RFC 5987标准，支持中文等特殊字符）
    # 模式说明：匹配 filename*=UTF-8'' 后面的编码内容，直到分号或结束
    utf8_pattern = r"filename\*=UTF-8''(.*?)(?:;|$)"
    utf8_match = re.search(utf8_pattern, content_disposition, re.IGNORECASE)

    if utf8_match and utf8_match.group(1):
        try:
            # 解码URL编码（如%E4%B8%AD%E6%96%87 -> 中文）
            return unquote(utf8_match.group(1))
        except Exception as e:
            print(f"解码UTF-8文件名失败: {e}")

    # 2. 若未匹配到filename*，再匹配普通filename格式
    # 支持带引号、不带引号、单引号、双引号的情况
    normal_pattern = r"filename=(?:[\"']?)(.*?)(?:[\"']?)(?:;|$)"
    normal_match = re.search(normal_pattern, content_disposition, re.IGNORECASE)

    if normal_match and normal_match.group(1):
        return normal_match.group(1).strip("\"'")  # 去除可能的引号

    # 3. 未匹配到任何文件名
    return ""


def get_audio_name(url: str, port: int, file_name="Audio", default="ogg"):
    full_url = f"http://localhost:{port}{url}"
    head_req = requests.get(full_url, stream=True)
    extension = head_req.headers.get("content-type", default=default)
    if extension != default:
        extension = extension.split("/")[1]
    extension = "." + extension
    return file_name + extension


def get_loaded_resources(port=PORT, path={"P": []}, from_url=False, url="") -> dict:
    if not from_url:
        res = requests.get(
            f"http://localhost:{port}/Resources/View?path={quote(dumps(path))}",
            headers={"host": "127.0.0.1"},
        )
    else:
        if url.startswith("/"):
            res = requests.get(f"http://localhost:{port}{url}")
        elif url.startswith("http"):
            res = requests.get(url)
        else:
            res = requests.get(f"http://localhost:{port}/{url}")

    decoded_content = decode_response(res)
    return parser.parse_resources_html(decoded_content)


def post_settings(settings: dict, port=PORT):
    res = requests.post(
        f"http://localhost:{port}/Settings/Update",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=settings,
    )
    return res.status_code


def get_configs(port=PORT):
    res = requests.get(f"http://localhost:{port}/ConfigurationFiles")
    decoded_content = decode_response(res)
    return parser.extract_config_data(decoded_content)


def replace_config_file(name: str, port=PORT):
    _thread.start_new_thread(_replace_config_file, (name, port))


def _replace_config_file(name: str, port=PORT):
    res = requests.post(
        f"http://localhost:{port}/ConfigurationFiles/Singleton/Add", data={"Key": name}
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onReplaceFileFinished(res)


def remove_config_file(name: str, port=PORT):
    _thread.start_new_thread(_remove_config_file, (name, port))


def _remove_config_file(name: str, port=PORT):
    res = requests.post(
        f"http://localhost:{port}/ConfigurationFiles/Singleton/Remove",
        data={"Key": name},
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onReplaceFileFinished(res)


def load_file_or_folder_from_path(path: str, port=PORT):
    _thread.start_new_thread(_load_file_or_folder_from_path, (path, port))


def _load_file_or_folder_from_path(path: str, port=PORT):
    res = requests.post(
        f"http://localhost:{port}/LoadFolder",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={"path": path},
    )
    decoded_content = decode_response(res)
    res.decoded_text = decoded_content
    StatusMachine.onApiCallFinished(res)


def export_unity_project(path: str, create_sub_folder: bool, port=PORT):
    _thread.start_new_thread(_export_unity_project, (path, create_sub_folder, port))


def _export_unity_project(path: str, create_sub_folder: bool, port=PORT):
    requests.post(
        f"http://127.0.0.1:{port}/Export/UnityProject",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={"Path": path, "CreateSubfolder": create_sub_folder},
    )


def export_primary_content(path: str, create_sub_folder: bool, port=PORT):
    _thread.start_new_thread(_export_primary_content, (path, create_sub_folder, port))


def _export_primary_content(path: str, create_sub_folder: bool, port=PORT):
    requests.post(
        f"http://127.0.0.1:{port}/Export/PrimaryContent",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={"Path": path, "CreateSubfolder": create_sub_folder},
    )
