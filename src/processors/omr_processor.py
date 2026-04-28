import os
import cv2
import numpy as np
from pdf2image import convert_from_path
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
            
            h, w = image_cv.shape[:2]
            print(f"Pagina {page_num+1}: {w}x{h}")
            
            student_id = self._extract_student_id(image_cv)
            
            if num_questions:
                questions_per_page = self.config.QUESTIONS_PER_PAGE
                start_q = page_num * questions_per_page + 1
                end_q = min(start_q + questions_per_page - 1, num_questions)
                responses = self._extract_responses(image_cv, start_q, end_q, debug=True)
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
    
    def _extract_responses(self, image, start_q=1, end_q=None, debug=False):
        import numpy as np
        import cv2
        
        if end_q is None:
            end_q = self.config.QUESTIONS_PER_PAGE
        
        h, w = image.shape[:2]
        gray = np.mean(image, axis=2)
        
        scale_x = w / self.config.PAGE_WIDTH
        scale_y = h / self.config.PAGE_HEIGHT
        
        total_responses = end_q - start_q + 1
        
        margin = 50
        available_width = self.config.PAGE_WIDTH - (margin * 2)
        max_cols = 3
        col_width = available_width / max_cols
        q_per_col = 25
        cols_on_page = min(max_cols, (total_responses + q_per_col - 1) // q_per_col)
        
        responses = [''] * total_responses
        options = ['A', 'B', 'C', 'D']
        
        y_base = (self.config.PAGE_HEIGHT - self.config.MARGIN_TOP - 50) * scale_y
        start_x = (margin + 20) * scale_x
        gap_y = self.config.QUESTION_HEIGHT * scale_y
        
        option_x_offset = [
            0, 
            self.config.BUBBLE_SPACING * scale_x, 
            self.config.BUBBLE_SPACING * 2 * scale_x, 
            self.config.BUBBLE_SPACING * 3 * scale_x
        ]
        
        for col in range(cols_on_page):
            col_start = start_q + col * q_per_col
            col_end = min(col_start + q_per_col, end_q + 1)
            x_offset = (margin + col * col_width + 20) * scale_x
            
            y = y_base
            for q in range(col_start, col_end):
                idx = q - start_q
                if idx >= total_responses:
                    break
                best_opt = None
                best_mean = 256
                
                for i, opt in enumerate(options):
                    x = start_x + x_offset - (margin * scale_x) + option_x_offset[i]
                    roi = gray[max(0, int(y-10)):min(h, int(y+10)), 
                               max(0, int(x-10)):min(w, int(x+10))]
                    
                    if roi.size > 0:
                        mean = np.mean(roi)
                        if mean < best_mean:
                            best_mean = mean
                            best_opt = opt
                
                if best_mean < 250:
                    responses[idx] = best_opt if best_opt else ''
                
                y -= gap_y
        
        return responses