import os
import threading
from src.config import Config
from src.processors.omr_processor import OMRProcessor
from src.utils.csv_handler import CSVHandler

class ProcessingController:
    def __init__(self, view):
        self.view = view
        self.config = Config()
    
    def process(self):
        if not self.view.pdf_path:
            self.view.set_status("Error: Seleccione archivo PDF", True)
            return
        if not self.view.csv_output_dir:
            self.view.set_status("Error: Seleccione carpeta salida", True)
            return
        
        try:
            num_q = int(self.view.num_questions_proc.value)
        except:
            self.view.set_status("Error: Número inválido", True)
            return
        
        self.view.set_loading(True)
        self.view.set_status("Procesando...")
        
        def do_proc():
            try:
                proc = OMRProcessor(self.config)
                results = proc.process_pdf(self.view.pdf_path, num_questions=num_q)
                
                out_csv = os.path.join(self.view.csv_output_dir, "resultados.csv")
                CSVHandler.write_responses(out_csv, results, num_q)
                
                self.view.page.run_task(self._on_done, out_csv, len(results))
            except Exception as e:
                self.view.page.run_task(self._on_error, str(e))
        
        threading.Thread(target=do_proc, daemon=True).start()
    
    async def _on_done(self, filename, count):
        self.view.set_loading(False)
        self.view.set_status(f"Listo: {os.path.basename(filename)} ({count} hojas)")
    
    async def _on_error(self, msg):
        self.view.set_loading(False)
        self.view.set_status(f"Error: {msg}", True)