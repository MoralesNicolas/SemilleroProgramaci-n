import os
import threading
from src.config import Config
from src.models.student import Student
from src.generators.pdf_generator import PDFGenerator
from src.utils.csv_handler import CSVHandler

class GenerationController:
    def __init__(self, view):
        self.view = view
        self.config = Config()
    
    def generate(self):
        if not self.view.csv_path:
            self.view.set_status("Error: Seleccione archivo CSV", True)
            return
        if not self.view.output_dir:
            self.view.set_status("Error: Seleccione carpeta salida", True)
            return
        
        try:
            num_q = int(self.view.num_questions.value)
        except:
            self.view.set_status("Error: Número inválido", True)
            return
        
        self.view.set_loading(True)
        self.view.set_status("Generando...")
        
        def do_gen():
            try:
                students = [Student(sid) for sid in CSVHandler.read_student_ids(self.view.csv_path)]
                title = self.view.title.value
                footer = self.view.footer.value
                
                out_file = os.path.join(self.view.output_dir, "hojas.pdf")
                gen = PDFGenerator(self.config, None, title, footer)
                gen.generate_sheets(students, num_q, out_file)
                
                self.view.page.run_task(self._on_done, out_file, len(students))
            except Exception as e:
                self.view.page.run_task(self._on_error, str(e))
        
        threading.Thread(target=do_gen, daemon=True).start()
    
    async def _on_done(self, filename, count):
        self.view.set_loading(False)
        self.view.set_status(f"生成: {os.path.basename(filename)} ({count} estudiantes)")
    
    async def _on_error(self, msg):
        self.view.set_loading(False)
        self.view.set_status(f"Error: {msg}", True)