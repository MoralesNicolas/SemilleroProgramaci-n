import flet as ft

class PrimaryButton(ft.FilledButton):
    def __init__(self, text: str, icon: str, on_click, ref=None, width=300, height=50, bgcolor=ft.Colors.BLUE_700):
        super().__init__(
            content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD),
            icon=icon,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=bgcolor,
                padding=20,
            ),
            width=width,
            height=height,
            on_click=on_click,
            ref=ref
        )

class SecondaryButton(ft.FilledButton):
    def __init__(self, text: str, icon: str, on_click, width=250):
        super().__init__(
            content=ft.Text(text, size=14, weight=ft.FontWeight.BOLD),
            icon=icon,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.GREEN_700,
                padding=15,
            ),
            width=width,
            height=45,
            on_click=on_click
        )

class ImageSourceButton(ft.OutlinedButton):
    def __init__(self, text: str, icon: str, on_click):
        super().__init__(
            content=ft.Text(text, size=12),
            icon=icon,
            style=ft.ButtonStyle(
                color=ft.Colors.BLUE_200,
                padding=10
            ),
            on_click=on_click
        )
