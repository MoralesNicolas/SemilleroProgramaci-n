import flet as ft


def nav_bar(page: ft.Page):
    nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("Cargar"),
                        ft.dropdown.Option("menu2"),
                        ft.dropdown.Option("menu2")
                    ]
                )
            ],
            spacing=10,
        ),
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=10,
        border_radius=8,
        shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK54),
    )
    return nav