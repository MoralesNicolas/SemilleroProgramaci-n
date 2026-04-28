import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from .barcode_reader import BarcodeReader


class OMRProcessor:
    def __init__(self, config):
        self.config = config
        self.barcode_reader = BarcodeReader(config)
    
    def process_pdf(self, pdf_path, num_questions=None):
        images = convert_from_path(pdf_path, dpi=200)
        results = []
        
        for page_num, image in enumerate(images):
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            h, w = image_cv.shape[:2]
            
            student_id = self._extract_student_id(image_cv, w, h)
            
            if num_questions:
                responses = self._extract_responses(image_cv, w, h, 1, num_questions)
            else:
                responses = self._extract_responses(image_cv, w, h)
            
            results.append({
                'cedula': student_id if student_id else 'NO_LEIDO',
                'responses': responses,
                'page': page_num + 1
            })
        
        return results
    
    def _extract_student_id(self, image, w, h):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        roi = gray[int(0.075*h):int(0.115*h), int(0.83*w):int(0.997*w)]
        result = self.barcode_reader.read_barcode(roi)
        
        return result
    
    def _extract_responses(self, image, w, h, start_q=1, end_q=None):
        if end_q is None:
            end_q = 50
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        PAGE_WIDTH_PT = 612.0
        PAGE_HEIGHT_PT = 792.0
        MARGIN_PT = 15
        MARKER_SIZE_PT = 12
        CONTENT_TOP_PT = PAGE_HEIGHT_PT - 150
        ROW_HEIGHT_PT = 32
        BUBBLE_SPACING_PT = 30
        FIRST_BUBBLE_X_OFFSET_PT = 45
        TABLE_START_Y_OFFSET_PT = 5
        BUBBLE_RADIUS_PT = 9
        
        scale_x = w / PAGE_WIDTH_PT
        scale_y = h / PAGE_HEIGHT_PT
        
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        markers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            marker_area_pt = MARKER_SIZE_PT * MARKER_SIZE_PT
            min_area = 0.3 * marker_area_pt * scale_x * scale_y
            max_area = 2.0 * marker_area_pt * scale_x * scale_y
            if min_area < area < max_area:
                M = cv2.moments(cnt)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    markers.append((cx, cy))
        
        min_markers_needed = 2
        if len(markers) < min_markers_needed:
            return [''] * (end_q - start_q + 1)
        
        total_questions = end_q - start_q + 1
        
        available_width_pt = PAGE_WIDTH_PT - 60
        block_width_pt = 120
        min_cols = max(1, int(available_width_pt / block_width_pt))
        min_cols = min(min_cols, 3)
        available_height_pt = PAGE_HEIGHT_PT - 50 - 50 - 150
        max_rows_per_col = min(int(available_height_pt / ROW_HEIGHT_PT), 30)
        num_cols = min(min_cols, (total_questions + max_rows_per_col - 1) // max_rows_per_col)
        num_cols = max(1, num_cols)
        rows_per_col = (total_questions + num_cols - 1) // num_cols
        
        col_width_pt = available_width_pt / num_cols
        block_total_width_pt = num_cols * col_width_pt
        start_x_pt = (PAGE_WIDTH_PT - block_total_width_pt) / 2 + 10
        start_y_pt = CONTENT_TOP_PT - TABLE_START_Y_OFFSET_PT
        
        responses = [''] * total_questions
        options = ['A', 'B', 'C', 'D']
        bubble_radius_px = max(3, int(BUBBLE_RADIUS_PT * scale_x * 0.35))
        
        for q_num in range(start_q, end_q + 1):
            idx = q_num - start_q
            if idx < 0 or idx >= len(responses):
                continue
            
            col_idx = (q_num - 1) // rows_per_col
            row_idx = (q_num - 1) % rows_per_col
            
            x_offset_pt = start_x_pt + col_idx * col_width_pt
            
            fills = {}
            
            for i, opt in enumerate(options):
                x_pt = x_offset_pt + FIRST_BUBBLE_X_OFFSET_PT + i * BUBBLE_SPACING_PT
                y_pt = start_y_pt - row_idx * ROW_HEIGHT_PT - ROW_HEIGHT_PT / 2
                
                x_px = int(x_pt * scale_x)
                y_px = int((PAGE_HEIGHT_PT - y_pt) * scale_y)
                
                x1 = max(0, x_px - bubble_radius_px)
                x2 = min(w, x_px + bubble_radius_px)
                y1 = max(0, y_px - bubble_radius_px)
                y2 = min(h, y_px + bubble_radius_px)
                
                if x2 <= x1 or y2 <= y1:
                    continue
                
                roi = gray[y1:y2, x1:x2]
                
                if roi.size > 0:
                    dark_pixels = np.sum(roi < 140)
                    fill_ratio = dark_pixels / roi.size
                    fills[opt] = fill_ratio
            
            marked = [opt for opt, fill in fills.items() if fill > 0.15]
            
            if len(marked) == 1:
                responses[idx] = marked[0]
            else:
                responses[idx] = ''
        
        return responses