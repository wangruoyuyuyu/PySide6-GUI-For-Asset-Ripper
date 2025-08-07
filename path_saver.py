import os.path

DIRECTORY = os.path.expanduser("~/.wry_asset_ripper_ui")
FILE = "last_path.txt"
EXPORT_FILE = "last_export_path.txt"


def save_last_path(path: str):
    try:
        if not os.path.isdir(DIRECTORY):
            os.mkdir(DIRECTORY)
        with open(os.path.join(DIRECTORY, FILE), "w+") as f:
            f.write(path)
    except Exception:
        return


def get_last_path():
    try:
        if not os.path.exists(os.path.join(DIRECTORY, FILE)):
            return "."
        with open(os.path.join(DIRECTORY, FILE), "r+") as f:
            return f.read().strip()
    except Exception:
        return "."


def save_last_export_path(path: str):
    try:
        if not os.path.isdir(DIRECTORY):
            os.mkdir(DIRECTORY)
        with open(os.path.join(DIRECTORY, EXPORT_FILE), "w+") as f:
            f.write(path)
    except Exception:
        return


def get_last_export_path():
    try:
        if not os.path.exists(os.path.join(DIRECTORY, FILE)):
            return "."
        with open(os.path.join(DIRECTORY, EXPORT_FILE), "r+") as f:
            return f.read().strip()
    except Exception:
        return "."


def get_file_dir(file: str):
    file = file.replace("\\", "/")
    return "/".join(file.split("/")[:-1])


if __name__ == "__main__":
    print(get_file_dir("C:/Users\\test/file.ab"))
