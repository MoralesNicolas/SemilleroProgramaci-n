import cv2
import numpy as np
from pdf2image import convert_from_path
import tempfile
import os
from .image_processor import ImageProcessor
from .barcode_reader import BarcodeReader

class OMRProcessor:
    def __init__(self, config):
        self.config = config
        self.image_processor = ImageProcessor(config)
        self.barcode_reader = BarcodeReader(config)
    
    def process_pdf(self, pdf_path, num_questions=None):
        images = convert_from_path(pdf_path, dpi=200)
        results = []
        
        for page_num, image in enumerate(images):
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            student_id = self._extract_student_id(image_cv)
            
            if num_questions:
                questions_per_page = self.config.QUESTIONS_PER_PAGE
                start_q = page_num * questions_per_page + 1
                end_q = min(start_q + questions_per_page - 1, num_questions)
                responses = self._extract_responses(image_cv, start_q, end_q)
            else:
                responses = self._extract_responses(image_cv)
            
            if student_id:
                results.append({
                    'cedula': student_id,
                    'responses': responses,
                    'page': page_num + 1
                })
            else:
                print(f"Advertencia: No se pudo leer el codigo de barras en la pagina {page_num + 1}")
        
        return results
    
    def _extract_student_id(self, image):
        height, width = image.shape[:2]
        dpi_scale = width / 612.0
        
        barcode_bottom_y = self.config.BARCODE_Y
        barcode_height_pts = self.config.BARCODE_HEIGHT
        barcode_top_y = self.config.PAGE_HEIGHT - barcode_bottom_y - barcode_height_pts
        if barcode_top_y < 0:
            barcode_top_y = 0
        
        x = int(self.config.BARCODE_X * dpi_scale)
        y = int(barcode_top_y * dpi_scale)
        w = int(self.config.BARCODE_WIDTH * dpi_scale)
        h = int(barcode_height_pts * dpi_scale)
        
        if y + h > height:
            h = height - y
        if x + w > width:
            w = width - x
            
        barcode_region = image[y:y+h, x:x+w]
        return self.barcode_reader.read_barcode(barcode_region)
    
    def _extract_responses(self, image, start_q=1, end_q=None):
        if end_q is None:
            end_q = self.config.QUESTIONS_PER_PAGE
        
        gray = self.image_processor.convert_to_grayscale(image)
        thresh = self.image_processor.threshold(gray, self.config.OMR_BLACK_THRESHOLD)
        
        reference_marks = self.image_processor.find_reference_marks(image)
        
        if len(reference_marks) >= 4:
            image = self.image_processor.correct_perspective(image, reference_marks)
            gray = self.image_processor.convert_to_grayscale(image)
            thresh = self.image_processor.threshold(gray, self.config.OMR_BLACK_THRESHOLD)
        
        responses = []
        options = ['A', 'B', 'C', 'D']
        
        x_start = self.config.MARGIN_LEFT + 30
        y_start = self.config.MARGIN_TOP + 50
        
        option_x_offset = [0, self.config.BUBBLE_SPACING, 
                          self.config.BUBBLE_SPACING * 2, 
                          self.config.BUBBLE_SPACING * 3]
        
        for q_num in range(start_q, end_q + 1):
            y = y_start + (self.config.QUESTION_HEIGHT * (end_q - q_num))
            
            question_responses = []
            
            for idx, x_off in enumerate(option_x_offset):
                x = x_start + x_off
                r = self.config.BUBBLE_RADIUS
                
                bubble_region = self.image_processor.extract_bubble_region(
                    thresh, x, y, r + 3
                )
                
                fill_pct = self.image_processor.calculate_fill_percentage(bubble_region)
                
                if fill_pct > self.config.OMR_THRESHOLD:
                    question_responses.append(options[idx])
            
            if len(question_responses) == 1:
                responses.append(question_responses[0])
            elif len(question_responses) > 1:
                responses.append('INVALID')
            else:
                responses.append('')
        
        return responses