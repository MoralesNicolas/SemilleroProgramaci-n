import flet as ft

class FilePickerManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.pickers = {}
        self._init_pickers()
    
    def _init_pickers(self):
        # CSV file picker
        self.csv_picker = ft.FilePicker()
        self.pickers['csv'] = self.csv_picker
        
        # Image file picker
        self.image_picker = ft.FilePicker()
        self.pickers['image'] = self.image_picker
        
        # PDF file picker
        self.pdf_picker = ft.FilePicker()
        self.pickers['pdf'] = self.pdf_picker
        
        # Output directory picker (for PDF)
        self.output_dir_picker = ft.FilePicker()
        self.pickers['output_dir'] = self.output_dir_picker
        
        # CSV output directory picker
        self.csv_output_dir_picker = ft.FilePicker()
        self.pickers['csv_output_dir'] = self.csv_output_dir_picker
        
        # Add all to overlay
        self.page.overlay.extend(self.pickers.values())
    
    def set_csv_callback(self, callback):
        self.csv_picker.on_result = callback
    
    def set_image_callback(self, callback):
        self.image_picker.on_result = callback
    
    def set_pdf_callback(self, callback):
        self.pdf_picker.on_result = callback
    
    def set_output_dir_callback(self, callback):
        self.output_dir_picker.on_result = callback
    
    def set_csv_output_dir_callback(self, callback):
        self.csv_output_dir_picker.on_result = callback
    
    def pick_csv(self):
        self.csv_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv"]
        )
    
    def pick_image(self):
        self.image_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg"]
        )
    
    def pick_pdf(self):
        self.pdf_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf"]
        )
    
    def pick_output_dir(self):
        self.output_dir_picker.get_directory_path()
    
    def pick_csv_output_dir(self):
        self.csv_output_dir_picker.get_directory_path()
