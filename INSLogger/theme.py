from typing import overload, TypeVar

Theme = TypeVar("Theme")

class Theme:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, origin_theme: Theme) -> None: ...
    @overload
    def __init__(self, theme_dict: dict) -> None: ...

    def __init__(self, a0 = None) -> None:
        if isinstance(a0, Theme):
            self.theme = a0.theme
        elif isinstance(a0, dict):
            self.theme = a0
        else:
            raise TypeError("a0 only can be Theme or dict!")
    
    @overload
    def set_theme(self, theme_dict: dict) -> None: ...
    @overload
    def set_theme(self, theme_key: str, theme_data: str) -> None: ...

    def set_theme(self, a0, a1 = None) -> None:
        if isinstance(a0, dict):
            for key in list(a0.keys()):
                self.theme[key] = a0[key]
        elif isinstance(a0, str):
            if a1 is None:
                raise TypeError("theme_data cannot be None!")
            if isinstance(a1, str):
                self.theme[a0] = a1
            else:
                raise TypeError("theme_data only can be str!")
        else:
            raise TypeError("a0 only can be dict or str!")
    
    def get_theme(self, theme_key: str) -> str:
        if isinstance(theme_key, str):
            if self.theme.get(theme_key, None) is None:
                raise KeyError(f"cannot find theme key '{theme_key}'!")
            return self.theme[theme_key]
        else:
            raise TypeError("theme_key only can be str!")

    def __call__(self, theme_key: str) -> str:
        return self.get_theme(theme_key)
