import flet as ft
from controllers.generation_controller import GenerationController
from controllers.processing_controller import ProcessingController

ACCENT = "#10b981"
ORANGE = "#f97316"
CARD_BG = "#1e293b"
TEXT_WHITE = "#ffffff"
TEXT_GRAY = "#94a3b8"
INPUT_BG = "#0f172a"
BORDER_COLOR = "#334155"

SPACING = 6
SPACING_MD = 10
SPACING_LG = 14

CARD_WIDTH = 600

class MainView:
    def __init__(self, page, csv_picker, image_picker, pdf_picker, output_picker, csv_output_picker):
        self.page = page
        self.csv_picker = csv_picker
        self.image_picker = image_picker
        self.pdf_picker = pdf_picker
        self.output_picker = output_picker
        self.csv_output_picker = csv_output_picker
        self.csv_path = None
        self.image_path = None
        self.output_dir = None
        self.pdf_path = None
        self.csv_output_dir = None

        self._build_ui()
        
        self.gen_controller = GenerationController(self)
        self.proc_controller = ProcessingController(self)

    def _build_ui(self):
        self.csv_text = ft.Text("", size=12, color=TEXT_GRAY)
        self.image_text = ft.Text("", size=12, color=TEXT_GRAY)
        self.output_text = ft.Text("", size=12, color=TEXT_GRAY)
        self.pdf_text = ft.Text("", size=12, color=TEXT_GRAY)
        self.csv_out_text = ft.Text("", size=12, color=TEXT_GRAY)
        self.gen_status = ft.Text("", size=11, color=TEXT_GRAY)
        self.proc_status = ft.Text("", size=11, color=TEXT_GRAY)

        self.num_questions = ft.TextField(label="Preguntas", value="50", width=220, height=36, text_size=12, bgcolor=INPUT_BG, border_color=BORDER_COLOR)
        self.title = ft.TextField(label="Título", value="HOJA RESPUESTAS", width=220, height=36, text_size=12, bgcolor=INPUT_BG, border_color=BORDER_COLOR)
        self.footer = ft.TextField(label="Footer", value="ICFES", width=450, height=36, text_size=12, bgcolor=INPUT_BG, border_color=BORDER_COLOR)
        self.num_questions_proc = ft.TextField(label="Preguntas", value="50", width=450, height=36, text_size=12, bgcolor=INPUT_BG, border_color=BORDER_COLOR)
        
        self.url_input = ft.TextField(
            label="URL",
            width=300,
            height=36,
            text_size=12,
            bgcolor=INPUT_BG,
            border_color=BORDER_COLOR,
            visible=False
        )

        self.file_btn = ft.Container(
            content=ft.Text("Archivo", size=12, weight="bold"),
            padding=ft.Padding(10, 6, 10, 6),
            bgcolor=ACCENT,
            border_radius=6,
            on_click=lambda e: self._show_file_mode("archivo")
        )

        self.url_btn = ft.Container(
            content=ft.Text("URL", size=12, weight="bold"),
            padding=ft.Padding(10, 6, 10, 6),
            bgcolor="transparent",
            border_radius=6,
            on_click=lambda e: self._show_file_mode("url")
        )

    def _show_file_mode(self, mode):
        if mode == "archivo":
            self.file_btn.bgcolor = ACCENT
            self.url_btn.bgcolor = "transparent"
            self.url_input.visible = False
        else:
            self.file_btn.bgcolor = "transparent"
            self.url_btn.bgcolor = ACCENT
            self.url_input.visible = True
        self.page.update()

    def _btn(self, txt, ic, on_click):
        return ft.Container(
            content=ft.Row([ft.Icon(ic, size=16), ft.Text(txt, size=12)], spacing=8),
            bgcolor=ACCENT,
            border_radius=6,
            padding=10,
            on_click=on_click,
            ink=True
        )

    def _btn_main(self, txt, ic, color, on_click):
        return ft.Container(
            content=ft.Row([ft.Icon(ic, size=16), ft.Text(txt, size=13, weight="bold")], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=color,
            border_radius=6,
            padding=12,
            on_click=on_click,
            ink=True
        )

    def _label(self, txt):
        return ft.Text(txt, size=12, color=TEXT_GRAY)

    def _input(self, label, value, width=280):
        return ft.TextField(label=label, value=value, width=width, height=36, text_size=12, bgcolor=INPUT_BG, border_color=BORDER_COLOR)

    def build(self):
        gen_card = ft.Container(
            content=ft.Column([
                ft.Text("GENERAR HOJAS", size=16, weight="bold", color=TEXT_WHITE),
                ft.Container(height=SPACING_MD),

                self._label("Archivo CSV"),
                self._btn("Seleccionar CSV", ft.Icons.UPLOAD_FILE, self._on_csv),
                self.csv_text,
                ft.Container(height=SPACING),

                self._label("Imagen (opcional)"),
                ft.Row([self.file_btn, self.url_btn], spacing=6),
                self.url_input,
                self._btn("Seleccionar imagen", ft.Icons.IMAGE, self._on_image),
                self.image_text,
                ft.Container(height=SPACING),

                ft.Row([
                    self.num_questions,
                    self.title,
                ], spacing=10),
                ft.Container(height=SPACING),

                self.footer,
                ft.Container(height=SPACING_MD),

                self._label("Carpeta de salida"),
                self._btn("Seleccionar carpeta", ft.Icons.FOLDER_OPEN, self._on_output),
                self.output_text,
                ft.Container(height=SPACING_MD),

                self._btn_main("GENERAR PDF", ft.Icons.PICTURE_AS_PDF, ACCENT, self._on_gen),
                self.gen_status,
            ], spacing=2),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=10,
            width=CARD_WIDTH
        )

        proc_card = ft.Container(
            content=ft.Column([
                ft.Text("PROCESAR HOJAS OMR", size=16, weight="bold", color=TEXT_WHITE),
                ft.Container(height=SPACING_MD),

                self._label("Archivo PDF escaneado"),
                self._btn("Seleccionar PDF", ft.Icons.UPLOAD_FILE, self._on_pdf),
                self.pdf_text,
                ft.Container(height=SPACING),

                self.num_questions_proc,
                ft.Container(height=SPACING_MD),

                self._label("Carpeta de salida CSV"),
                self._btn("Seleccionar carpeta", ft.Icons.FOLDER_OPEN, self._on_csv_output),
                self.csv_out_text,
                ft.Container(height=SPACING_MD),

                self._btn_main("PROCESAR OMR", ft.Icons.DOCUMENT_SCANNER, ORANGE, self._on_proc),
                self.proc_status,
            ], spacing=2),
            padding=20,
            bgcolor=CARD_BG,
            border_radius=10,
            width=CARD_WIDTH
        )

        main_col = ft.Column([
            gen_card,
            ft.Container(height=SPACING_MD),
            proc_card,
        ], spacing=SPACING_MD, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        wrapper = ft.Container(
            content=ft.Column([main_col], scroll="auto"),
            padding=SPACING_LG,
            expand=True
        )

        return wrapper

    async def _on_csv(self, e):
        f = await self.csv_picker.pick_files(allow_multiple=False, allowed_extensions=["csv"])
        if f:
            self.csv_path = f[0].path
            self.csv_text.value = f[0].name
            self.csv_text.color = ACCENT
            self.page.update()

    async def _on_image(self, e):
        if self.url_input.visible and self.url_input.value:
            self.image_path = self.url_input.value
            self.image_text.value = self.image_path
            self.image_text.color = ACCENT
        else:
            f = await self.image_picker.pick_files(allow_multiple=False, allowed_extensions=["png","jpg","jpeg"])
            if f:
                self.image_path = f[0].path
                self.image_text.value = f[0].name
                self.image_text.color = ACCENT
        self.page.update()

    async def _on_output(self, e):
        p = await self.output_picker.get_directory_path()
        if p:
            self.output_dir = p
            self.output_text.value = p
            self.output_text.color = ACCENT
            self.page.update()

    async def _on_pdf(self, e):
        f = await self.pdf_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])
        if f:
            self.pdf_path = f[0].path
            self.pdf_text.value = f[0].name
            self.pdf_text.color = ORANGE
            self.page.update()

    async def _on_csv_output(self, e):
        p = await self.csv_output_picker.get_directory_path()
        if p:
            self.csv_output_dir = p
            self.csv_out_text.value = p
            self.csv_out_text.color = ORANGE
            self.page.update()

    def _on_gen(self, e=None):
        self.gen_controller.generate()

    def set_loading(self, loading):
        pass
    
    def set_status(self, msg, err=False):
        self.gen_status.value = msg
        self.gen_status.color = "#ef4444" if err else TEXT_GRAY
        self.proc_status.value = msg
        self.proc_status.color = "#ef4444" if err else TEXT_GRAY
        self.page.update()

    def _on_proc(self, e=None):
        self.proc_controller.process()