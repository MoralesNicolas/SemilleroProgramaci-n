import flet as ft
from PIL import Image
import os
ruta_imagen = None


def main(page: ft.Page):
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50

    dest_field = ft.TextField(
        value="/mi-proyecto/",
        expand=True,
        height=40,
        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
        border_radius=8,
        text_size=13,
        disabled=True,
    )
    csv_file_text = ft.TextField(
        value="",
        expand=True,
        height=40,
        border_radius=8,
        disabled= True,

    )
    file_name_text = ft.Text(
        value="Seleccionar archivo o arrastrar aqui",
        size=13,
        color=ft.Colors.BLUE_GREY_600,
    )

    preview_row = ft.Row(
        visible=False,
        controls=[
            ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED,
                    color=ft.Colors.BLUE_GREY_300, size=18),
            ft.Text("", size=13, color=ft.Colors.BLUE_GREY_700),
        ],
        spacing=8,
    )

    cb_pdf = ft.Checkbox(label="PDF", value=True)
    cb_jpg = ft.Checkbox(label="JPG", value=False)
    cb_png = ft.Checkbox(label="PNG", value=False)
    async def seleccionar_archivo(e):
        global ruta_imagen
        picker = ft.FilePicker()
        file = await picker.pick_files(allow_multiple=False)
        if file:
            ruta_imagen = file[0].path
            name = file[0].name
            file_name_text.value = name
            preview_row.controls[1].value = name
            preview_row.visible = True
        else:
            file_name_text.value = "Seleccionar archivo o arrastrar aqui"
            preview_row.visible = False
        page.update()

    async def seleccionar_carpeta(e):
        picker = ft.FilePicker()
        file_path = await picker.get_directory_path()
        if file_path:
            dest_field.value = file_path
        page.update()

    def on_cargar_click(e):
        img = Image.open(ruta_imagen)
        ruta = os.path.join(dest_field.value,file_name_text.value)
        img.save(ruta)
        page.show_dialog(ft.SnackBar(ft.Text("Archivo guardado con exito"), bgcolor="green"))
        page.update()

    def show_welcome():
        content_area.content = welcome_view
        nav_dropdown.value = None
        page.update()
    generar_panel =ft.Column(
        ft.Text(" Generar hojas de respuesta",size=15, color= ft.Colors.BLUE_GREY_500),
        ft.Divider(height=5),
        ft.Container(
            content = ft.Row(
                controls=[
                    ft.Text("Archivo csv"),
                    csv_file_text,
                    ft.IconButton(icon=ft.Icons.FOLDER)

                ]
            )
        )
    ),

    cargar_panel = ft.Column(
        controls=[
            ft.Text("Cargar archivo", size=12, weight=ft.FontWeight.W_600,
                    color=ft.Colors.BLUE_GREY_500),
            ft.Divider(height=1),

            ft.Text("ORIGEN", size=11, color=ft.Colors.BLUE_GREY_400,
                    weight=ft.FontWeight.W_600),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.UPLOAD_FILE_OUTLINED,
                            color=ft.Colors.BLUE_GREY_400, size=20),
                    file_name_text,
                ], spacing=10),
                border=ft.border.all(1.5, ft.Colors.BLUE_GREY_200),
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
                on_click=seleccionar_archivo,
                ink=True,
                bgcolor=ft.Colors.WHITE,
            ),

            ft.Text("DESTINO", size=11, color=ft.Colors.BLUE_GREY_400,
                    weight=ft.FontWeight.W_600),
            ft.Row([
                dest_field,
                ft.Button(
                    "Examinar",
                    on_click=seleccionar_carpeta,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_GREY_700,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    height=40,
                ),
            ], spacing=8),

            ft.Text("TIPO DE ARCHIVO", size=11, color=ft.Colors.BLUE_GREY_400,
                    weight=ft.FontWeight.W_600),
            ft.Row([cb_pdf, cb_jpg, cb_png], spacing=16),

            preview_row,

            ft.Divider(height=1),
            ft.Row([
                ft.TextButton("Cancelar", on_click=lambda _: show_welcome()),
                ft.Button(
                    "Cargar",
                    on_click=on_cargar_click,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_GREY_700,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.END, spacing=8),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    welcome_view = ft.Column(
        controls=[
            ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED,
                    size=48, color=ft.Colors.BLUE_GREY_200),
            ft.Text("Selecciona una opcion del menu para comenzar",
                    size=14, color=ft.Colors.BLUE_GREY_400),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    content_area = ft.Container(
        content=welcome_view,
        expand=True,
        padding=20,
        bgcolor=ft.Colors.BLUE_GREY_50,
    )

    def on_nav_change(e):
        if nav_dropdown.value == "Cargar":
            content_area.content = cargar_panel
        elif nav_dropdown.value =="Generar":
            content_area.content = generar_panel
        else:
            content_area.content = ft.Column(
                controls=[
                    ft.Text("seccion en contruccion.", size=14,
                            color=ft.Colors.BLUE_GREY_400)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        page.update()

    nav_dropdown = ft.Dropdown(
        options=[  
            ft.dropdown.Option("Cargar"),
            ft.dropdown.Option("Generar"),
            ft.dropdown.Option(""),
        ],
        leading_icon=ft.Icons.MENU,
        on_select=on_nav_change,
        height=38,
        text_size=13,
        border_radius=6,
        width=160,
        hint_style=ft.TextStyle(color=ft.Colors.WHITE)
    )

    nav_bar = ft.Container(
        content=ft.Row([nav_dropdown], spacing=10),
        bgcolor=ft.Colors.BLUE_GREY_700,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
    )
    page.add(ft.Column([
        nav_bar,
        content_area,
    ], spacing=0, expand=True))


ft.run(main)

# Idea "Cargar archivos y modificarlos con Apellido y Nombre
# mas facil de calificar"