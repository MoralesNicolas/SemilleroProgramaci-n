import os

class Config:
    PAGE_WIDTH = 612
    PAGE_HEIGHT = 792
    MARGIN_LEFT = 30
    MARGIN_RIGHT = 30
    MARGIN_TOP = 50
    MARGIN_BOTTOM = 50

    QUESTION_HEIGHT = 22
    BUBBLE_RADIUS = 8
    BUBBLE_SPACING = 28
    QUESTIONS_PER_PAGE = 50

    FONT_NAME = "Helvetica"
    FONT_SIZE_NORMAL = 8
    FONT_SIZE_SMALL = 7
    FONT_SIZE_TITLE = 10
    FONT_SIZE_HEADER = 9

    BARCODE_WIDTH = 80
    BARCODE_HEIGHT = 22
    BARCODE_X = 500
    BARCODE_Y = 710

    REFERENCE_MARK_SIZE = 12
    REFERENCE_MARK_COLOR = (0, 0, 0)

    OMR_THRESHOLD = 0.4
    OMR_BLACK_THRESHOLD = 127

    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"

    DEFAULT_HEADER_IMAGE_URL = "https://www.ucundinamarca.edu.co/images/ucundinamarca/escudo-color.png"
    DOCUMENT_TITLE = "HOJA DE RESPUESTAS"
    DOCUMENT_FOOTER = "ICFES"

    DEFAULT_QUESTIONS = 50

    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)