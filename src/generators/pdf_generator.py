from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
import io
import tempfile
import os
from .barcode_generator import BarcodeGenerator

class PDFGenerator:
    def __init__(self, config, header_image_path=None, title="HOJA DE RESPUESTAS", footer_text="ICFES"):
        self.config = config
        self.header_image_path = header_image_path
        self.title = title
        self.footer_text = footer_text
    
    def generate_sheets(self, students, num_questions, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        for student in students:
            pages_needed = (num_questions + self.config.QUESTIONS_PER_PAGE - 1) // self.config.QUESTIONS_PER_PAGE
            
            for page_num in range(pages_needed):
                self._draw_page(c, student, num_questions, page_num, pages_needed)
                c.showPage()
        
        c.save()
        return output_path
    
    def _draw_page(self, c, student, num_questions, page_num, total_pages):
        width, height = letter
        
        self._draw_header(c, width, height, student)
        self._draw_footer(c, width, height, page_num, total_pages)
        self._draw_reference_marks(c, width, height)
        
        start_q = page_num * self.config.QUESTIONS_PER_PAGE + 1
        end_q = min(start_q + self.config.QUESTIONS_PER_PAGE - 1, num_questions)
        
        self._draw_questions(c, start_q, end_q)
    
    def _draw_header(self, c, width, height, student):
        y_pos = height - 40
        
        if self.header_image_path:
            try:
                c.drawImage(self.header_image_path, 50, y_pos - 20, width=100, height=30, preserveAspectRatio=True)
            except:
                pass
        
        c.setFont(self.config.FONT_NAME, self.config.FONT_SIZE_TITLE)
        c.drawCentredString(width / 2, y_pos, self.title)
        
        barcode_gen = BarcodeGenerator(self.config)
        barcode_img = barcode_gen.generate(student.id_number)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        barcode_img.save(temp_file.name, format='PNG')
        temp_file.close()
        
        barcode_x = self.config.BARCODE_X
        barcode_y = self.config.BARCODE_Y
        
        c.drawImage(temp_file.name, barcode_x, barcode_y, 
                   width=self.config.BARCODE_WIDTH, 
                   height=self.config.BARCODE_HEIGHT)
        
        os.unlink(temp_file.name)
        
        c.setFont(self.config.FONT_NAME, self.config.FONT_SIZE_SMALL)
        c.drawString(barcode_x, barcode_y - 15, f"Cedula: {student.id_number}")
    
    def _draw_footer(self, c, width, height, page_num, total_pages):
        c.setFont(self.config.FONT_NAME, self.config.FONT_SIZE_SMALL)
        c.drawCentredString(width / 2, 30, self.footer_text)
        c.drawRightString(width - 50, 30, f"Pagina {page_num + 1} de {total_pages}")
    
    def _draw_reference_marks(self, c, width, height):
        size = self.config.REFERENCE_MARK_SIZE
        c.setFillColor(colors.black)
        
        c.rect(20, height - 20, size, size, fill=1, stroke=0)
        c.rect(width - 20 - size, height - 20, size, size, fill=1, stroke=0)
        c.rect(20, 20, size, size, fill=1, stroke=0)
        c.rect(width - 20 - size, 20, size, size, fill=1, stroke=0)
    
    def _draw_questions(self, c, start_q, end_q):
        x_start = self.config.MARGIN_LEFT + 30
        y_start = self.config.MARGIN_TOP + 50
        
        options = ['A', 'B', 'C', 'D']
        option_x_offset = [0, self.config.BUBBLE_SPACING, 
                          self.config.BUBBLE_SPACING * 2, 
                          self.config.BUBBLE_SPACING * 3]
        
        for i, q_num in enumerate(range(start_q, end_q + 1)):
            y = y_start + (self.config.QUESTION_HEIGHT * (end_q - q_num))
            
            c.setFont(self.config.FONT_NAME, self.config.FONT_SIZE_NORMAL)
            c.drawString(self.config.MARGIN_LEFT, y + 2, str(q_num))
            
            for idx, (option, x_off) in enumerate(zip(options, option_x_offset)):
                x = x_start + x_off
                r = self.config.BUBBLE_RADIUS
                
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.5)
                c.circle(x, y, r, fill=0, stroke=1)
                
                c.setFont(self.config.FONT_NAME, self.config.FONT_SIZE_SMALL)
                c.drawCentredString(x, y - 12, option)