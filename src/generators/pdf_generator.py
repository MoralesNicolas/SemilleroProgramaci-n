from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import tempfile
from .barcode_generator import BarcodeGenerator


class PDFGenerator:
    PAGE_WIDTH = 612
    PAGE_HEIGHT = 792
    MARGIN_LEFT = 30
    MARGIN_RIGHT = 30
    MARGIN_TOP = 50
    MARGIN_BOTTOM = 50
    
    MARKER_SIZE = 12
    BUBBLE_RADIUS = 9
    BUBBLE_SPACING = 30
    QUESTION_HEIGHT = 26
    
    def __init__(self, config, header_image_path=None, title=None, footer_text=None):
        self.config = config
        self.header_image_path = header_image_path
        self.title = title or config.DOCUMENT_TITLE
        self.footer_text = footer_text or config.DOCUMENT_FOOTER
        self.current_student = None
    
    def calculate_layout(self, num_questions):
        available_width = self.PAGE_WIDTH - (self.MARGIN_LEFT + self.MARGIN_RIGHT)
        available_height = self.PAGE_HEIGHT - self.MARGIN_TOP - self.MARGIN_BOTTOM - 150
        
        block_width = 120
        min_cols = max(1, int(available_width / block_width))
        min_cols = min(min_cols, 3)
        
        row_height = self.QUESTION_HEIGHT + 6
        max_rows_per_col = available_height // row_height
        max_rows_per_col = min(max_rows_per_col, 30)
        
        cols_needed = min(min_cols, (num_questions + max_rows_per_col - 1) // max_rows_per_col)
        cols_needed = max(1, cols_needed)
        
        rows_per_col = (num_questions + cols_needed - 1) // cols_needed
        
        return cols_needed, rows_per_col, row_height
    
    def generate_sheets(self, students, num_questions, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        num_cols, rows_per_col, row_height = self.calculate_layout(num_questions)
        questions_per_page = num_cols * rows_per_col
        
        for student in students:
            self.current_student = student
            pages_needed = (num_questions + questions_per_page - 1) // questions_per_page
            
            for page_num in range(pages_needed):
                self._draw_page(c, student, num_questions, page_num, pages_needed, num_cols, rows_per_col, row_height)
                c.showPage()
        
        c.save()
        return output_path
    
    def _draw_page(self, c, student, num_questions, page_num, total_pages, num_cols, rows_per_col, row_height):
        width, height = letter
        
        self._draw_header(c, width, height)
        self._draw_student_info(c, width, height, student)
        self._draw_footer(c, width, height, page_num, total_pages)
        
        content_top = height - 150
        content_bottom = self.MARGIN_BOTTOM + 50
        
        self._draw_reference_markers(c, width, height, content_top, content_bottom)
        
        available_width = width - self.MARGIN_LEFT - self.MARGIN_RIGHT
        col_width = available_width / num_cols
        block_total_width = num_cols * col_width
        start_x = (width - block_total_width) / 2 + 10
        start_y = content_top - 5
        
        for col in range(num_cols):
            start_q = page_num * rows_per_col * num_cols + col * rows_per_col + 1
            if start_q > num_questions:
                break
            
            end_q = min(start_q + rows_per_col - 1, num_questions)
            x_offset = start_x + col * col_width
            
            self._draw_question_table(
                c,
                start_q,
                end_q,
                x_offset + 5,
                start_y,
                col_width - 10,
                row_height
            )
    
    def _draw_header(self, c, width, height):
        if self.header_image_path and os.path.exists(self.header_image_path):
            try:
                c.drawImage(self.header_image_path, 30, height - 60, width=70, height=35, preserveAspectRatio=True)
            except:
                pass
        
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2, height - 45, self.title)
    
    def _draw_student_info(self, c, width, height, student):
        y = height - 80
        
        c.setFont("Helvetica", 11)
        c.drawString(50, y, "Nombre:")
        c.line(90, y - 1, 210, y - 1)
        
        c.drawString(230, y, "Cédula:")
        c.drawString(280, y, student.id_number)
        
        c.drawString(390, y, "Fecha:")
        c.line(430, y - 1, 500, y - 1)
        
        barcode_gen = BarcodeGenerator(self.config)
        barcode_img = barcode_gen.generate(student.id_number)
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        barcode_img.save(temp_file.name, format='PNG')
        temp_file.close()
        
        c.drawImage(temp_file.name, 510, height - 90, width=100, height=30)
        os.unlink(temp_file.name)
    
    def _draw_footer(self, c, width, height, page_num, total_pages):
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, 25, self.footer_text)
        c.drawRightString(width - 30, 25, f"Página {page_num + 1} de {total_pages}")
    
    def _draw_reference_markers(self, c, page_width, page_height, content_top, content_bottom):
        size = self.MARKER_SIZE
        c.setFillColor(colors.black)
        
        margin = 15
        c.rect(margin, content_top - size, size, size, fill=1, stroke=0)
        c.rect(page_width - margin - size, content_top - size, size, size, fill=1, stroke=0)
        c.rect(margin, content_bottom - size, size, size, fill=1, stroke=0)
        c.rect(page_width - margin - size, content_bottom - size, size, size, fill=1, stroke=0)
    
    def _draw_question_table(self, c, start_q, end_q, x_offset, start_y, col_width, row_height):
        from reportlab.platypus import Table, TableStyle

        data = []
        for q in range(start_q, end_q + 1):
            data.append([str(q), "", "", "", ""])

        col_widths = [30, 30, 30, 30, 30]

        table = Table(data, colWidths=col_widths, rowHeights=row_height)

        table.setStyle(TableStyle([
            ("LINEABOVE", (0,0), (-1,-1), 0.4, colors.grey),

            ("ROWBACKGROUNDS", (0,0), (-1,-1), [
                colors.HexColor("#e2e8f0ae"),
                None
            ]),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (0,-1), 11),
        ]))

        table.wrapOn(c, col_width, 1000)
        table.drawOn(c, x_offset, start_y - (len(data) * row_height))

        for row_index in range(len(data)):
            y = start_y - (row_index * row_height) - (row_height / 2)

            for col_index in range(1, 5):
                x = x_offset + sum(col_widths[:col_index]) + col_widths[col_index] / 2

                c.setLineWidth(1.2)
                c.circle(x, y, self.BUBBLE_RADIUS)

                c.setFont("Helvetica-Bold", 10)
                c.drawCentredString(x, y - 3, ["A", "B", "C", "D"][col_index - 1])