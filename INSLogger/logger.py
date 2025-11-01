from .theme import Theme
from .defaults_theme import DEFAULT_THEME
from typing import TypeVar
import time

Logger = TypeVar("Logger")


class Logger(object):
    def __init__(self, name: str = "main") -> None:
        self.name = name
        self.namespace_gray = False
        self.disable_time = True
        self.theme = DEFAULT_THEME

    def config(
        self,
        namespace_gray: bool = None,
        disable_time: bool = None,
        theme: Theme = None,
    ) -> None:
        if namespace_gray is not None:
            self.namespace_gray = namespace_gray
        if disable_time is not None:
            self.disable_time = disable_time
        if theme is not None:
            self.theme = theme

    def __call__(self, name: str = "sub") -> Logger:
        new_logger = Logger(f"{self.name} -> {name}")
        new_logger.config(self.namespace_gray, self.disable_time, self.theme)
        return new_logger

    def _log(self, level: str, messages: tuple) -> None:
        level = level.upper()
        messages = list(messages)

        msgs = []
        for i in range(len(messages)):
            messages[i] = str(messages[i])
        i = " ".join(messages)
        for j in i.split("\n"):
            msgs.append(j)

        for message in msgs:
            msg = ""

            if self.namespace_gray:
                msg += self.theme("GRAY")
            else:
                msg += self.theme(level)
            msg += f"[{self.name}] "

            if not self.disable_time:
                msg += f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "

            if self.namespace_gray:
                msg += self.theme(level)
            msg += f"[{level}] {message} {self.theme('CLEAN')}"

            print(msg)

    def info(self, *message) -> None:
        self._log("INFO", message)

    def log(self, *message) -> None:
        self._log("INFO", message)

    def warn(self, *message) -> None:
        self._log("WARN", message)

    def warning(self, *message) -> None:
        self._log("WARN", message)

    def error(self, *message) -> None:
        self._log("ERROR", message)

    def debug(self, *message) -> None:
        self._log("DEBUG", message)

    @staticmethod
    def enable() -> None: ...

    @staticmethod
    def disable() -> None: ...
