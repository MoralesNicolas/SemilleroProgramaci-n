import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flet as ft
from src.config import Config
from src.models.student import Student
from src.generators.pdf_generator import PDFGenerator
from src.processors.omr_processor import OMRProcessor
from src.utils.csv_handler import CSVHandler


class ICFESApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.init_components()
        self.build_ui()
    
    def setup_page(self):
        self.page.title = "un orm pal semillero"
        self.page.window.width = 470
        self.page.window.height = 600
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#0f172a"
    
    def init_components(self):
        self.config = Config()
        
        self.csv_picker = ft.FilePicker()
        self.pdf_picker = ft.FilePicker()
        self.output_dir_picker = ft.FilePicker()
        self.csv_output_dir_picker = ft.FilePicker()
        
        self.page.services.extend([
            self.csv_picker,
            self.pdf_picker,
            self.output_dir_picker,
            self.csv_output_dir_picker
        ])
        
        self.num_questions_gen = ft.TextField(
            label="Número de preguntas",
            value=str(Config.DEFAULT_QUESTIONS),
            width=200
        )
        self.csv_path_display = ft.Text("", size=12)
        self.output_dir_display = ft.Text("", size=12)
        
        self.num_questions_proc = ft.TextField(
            label="Número de preguntas",
            value=str(Config.DEFAULT_QUESTIONS),
            width=200
        )
        self.pdf_path_display = ft.Text("", size=12)
        self.csv_output_dir_display = ft.Text("", size=12)
        
        self.gen_status = ft.Text("", size=12)
        self.proc_status = ft.Text("", size=12)
        
        self.gen_progress = ft.ProgressBar(width=300, visible=False)
        self.proc_progress = ft.ProgressBar(width=300, visible=False)
    
    def build_ui(self):
        gen_card = ft.Container(
            content=ft.Column([
                ft.Text("GENERAR HOJAS DE RESPUESTAS", size=20, weight="bold"),
                ft.Container(height=10),
                ft.Button("Seleccionar CSV", icon=ft.Icons.UPLOAD_FILE, on_click=self._on_csv),
                self.csv_path_display,
                ft.Button("Carpeta de salida", icon=ft.Icons.FOLDER_OPEN, on_click=self._on_output_dir),
                self.output_dir_display,
                ft.Container(height=10),
                ft.Row([self.num_questions_gen, ft.Button("GENERAR PDF", on_click=self.generate_pdf)]),
                self.gen_progress,
                self.gen_status
            ], spacing=10),
            padding=20,
            width=450,
            bgcolor="#1e293b",
            border_radius=10
        )

        proc_card = ft.Container(
            content=ft.Column([
                ft.Text("PROCESAR HOJAS (OMR)", size=20, weight="bold"),
                ft.Container(height=10),
                ft.Button("Seleccionar PDF", icon=ft.Icons.UPLOAD_FILE, on_click=self._on_pdf),
                self.pdf_path_display,
                ft.Button("Carpeta de salida", icon=ft.Icons.FOLDER_OPEN, on_click=self._on_csv_output_dir),
                self.csv_output_dir_display,
                ft.Container(height=10),
                ft.Row([self.num_questions_proc, ft.Button("PROCESAR OMR", on_click=self.process_omr)]),
                self.proc_progress,
                self.proc_status
            ], spacing=10),
            padding=20,
            width=450,
            bgcolor="#1e293b",
            border_radius=10
        )

        main_col = ft.Column(
            [gen_card, ft.Container(height=15), proc_card], 
            spacing=20, 
            alignment="center",
            scroll = ft.ScrollMode.AUTO,
            expand = True
        )
        
        self.page.add(main_col)

    async def _on_csv(self, e):
        f = await self.csv_picker.pick_files(allow_multiple=False, allowed_extensions=["csv"])
        if f:
            self.csv_path = f[0].path
            self.csv_path_display.value = f[0].name
            self.page.update()
    
    async def _on_pdf(self, e):
        f = await self.pdf_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])
        if f:
            self.pdf_path = f[0].path
            self.pdf_path_display.value = f[0].name
            self.page.update()
    
    async def _on_output_dir(self, e):
        p = await self.output_dir_picker.get_directory_path()
        if p:
            self.output_dir = p
            self.output_dir_display.value = p
            self.page.update()
    
    async def _on_csv_output_dir(self, e):
        p = await self.csv_output_dir_picker.get_directory_path()
        if p:
            self.csv_output_dir = p
            self.csv_output_dir_display.value = p
            self.page.update()

    def generate_pdf(self, e):
        if not hasattr(self, 'csv_path') or not self.csv_path:
            self.gen_status.value = "Error: Seleccione un archivo CSV"
            self.page.update()
            return
        
        if not hasattr(self, 'output_dir') or not self.output_dir:
            self.gen_status.value = "Error: Seleccione carpeta de salida"
            self.page.update()
            return
        
        try:
            num_q = int(self.num_questions_gen.value)
            if num_q <= 0:
                self.gen_status.value = "Error: El número debe ser mayor a 0"
                self.page.update()
                return
        except:
            self.gen_status.value = "Error: Número inválido"
            self.page.update()
            return

        self.gen_progress.visible = True
        self.gen_status.value = "Generando PDF..."
        self.page.update()
        
        csv_path = self.csv_path
        output_dir = self.output_dir
        num_questions = num_q
        
        def do_generate():
            try:
                import time
                time.sleep(0.3)
                students_ids = CSVHandler.read_student_ids(csv_path)
                students = [Student(sid) for sid in students_ids]
                
                title = Config.DOCUMENT_TITLE
                footer = Config.DOCUMENT_FOOTER
                
                output_filename = os.path.join(output_dir, "hojas_generadas.pdf")
                
                generator = PDFGenerator(Config(), None, title, footer)
                generator.generate_sheets(students, num_questions, output_filename)
                
                self.gen_status.value = f"PDF generado: {os.path.basename(output_filename)} ({len(students)} estudiantes)"
                self.gen_progress.visible = False
                self.page.update()
            except Exception as ex:
                self.gen_error(str(ex))
        
        thread = threading.Thread(target=do_generate, daemon=True)
        thread.start()

    def gen_error(self, error_msg):
        self.gen_progress.visible = False
        self.gen_status.value = f"Error: {error_msg}"
        self.page.update()

    def process_omr(self, e):
        if not hasattr(self, 'pdf_path') or not self.pdf_path:
            self.proc_status.value = "Error: Seleccione un PDF"
            self.page.update()
            return
        
        if not hasattr(self, 'csv_output_dir') or not self.csv_output_dir:
            self.proc_status.value = "Error: Seleccione carpeta de salida CSV"
            self.page.update()
            return
        
        try:
            num_q = int(self.num_questions_proc.value)
            if num_q <= 0:
                self.proc_status.value = "Error: El número debe ser mayor a 0"
                self.page.update()
                return
        except:
            self.proc_status.value = "Error: Número inválido"
            self.page.update()
            return

        self.proc_progress.visible = True
        self.proc_status.value = "Procesando..."
        self.page.update()
        
        pdf_path = self.pdf_path
        csv_output_dir = self.csv_output_dir
        num_questions = num_q
        
        def do_process():
            try:
                import time
                time.sleep(0.3)
                processor = OMRProcessor(Config())
                results = processor.process_pdf(pdf_path, num_questions=num_questions)
                
                output_csv = os.path.join(csv_output_dir, "resultados_omr.csv")
                CSVHandler.write_responses(output_csv, results, num_questions)
                
                self.proc_status.value = f"Completado: {os.path.basename(output_csv)} ({len(results)} hojas)"
                self.proc_progress.visible = False
                self.page.update()
            except Exception as ex:
                self.proc_error(str(ex))
        
        thread = threading.Thread(target=do_process, daemon=True)
        thread.start()

    def proc_error(self, error_msg):
        self.proc_progress.visible = False
        self.proc_status.value = f"Error: {error_msg}"
        self.page.update()


def main(page: ft.Page):
    app = ICFESApp(page)


if __name__ == "__main__":
    ft.run(main)