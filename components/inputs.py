import flet as ft

class StyledTextField(ft.TextField):
    def __init__(self, label: str, value: str = "", width: int = 300, keyboard_type=ft.KeyboardType.TEXT, multiline: bool = False):
        super().__init__(
            label=label,
            value=value,
            width=width,
            keyboard_type=keyboard_type,
            multiline=multiline,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_200,
            label_style=ft.TextStyle(color=ft.Colors.GREY_400)
        )

class NumberField(ft.TextField):
    def __init__(self, label: str, value: str = "50", width: int = 200):
        super().__init__(
            label=label,
            value=value,
            width=width,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.BLUE_400,
            focused_border_color=ft.Colors.BLUE_200,
            label_style=ft.TextStyle(color=ft.Colors.GREY_400)
        )
