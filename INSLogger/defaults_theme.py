from .theme import Theme

ORIGIN_THEME = Theme({
    "GRAY": "\033[97m",
    "INFO": "",
    "WARN": "\033[93m",
    "ERROR": "\033[91m",
    "DEBUG": "\033[2m",
    "CLEAN": "\033[0m"
})

DEFAULT_THEME = Theme({
    "GRAY": "\033[97m",
    "INFO": "\033[36m",
    "WARN": "\033[33m",
    "ERROR": "\033[31m",
    "DEBUG": "\033[34m",
    "CLEAN": "\033[0m"
})
