import os

class Config:
    PAGE_WIDTH = 612
    PAGE_HEIGHT = 792
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 50
    MARGIN_TOP = 80
    MARGIN_BOTTOM = 60
    
    QUESTION_HEIGHT = 20
    BUBBLE_RADIUS = 6
    BUBBLE_SPACING = 30
    QUESTIONS_PER_PAGE = 50
    
    FONT_NAME = "Helvetica"
    FONT_SIZE_NORMAL = 8
    FONT_SIZE_SMALL = 7
    FONT_SIZE_TITLE = 10
    
    BARCODE_WIDTH = 150
    BARCODE_HEIGHT = 40
    BARCODE_X = 420
    BARCODE_Y = 740
    
    REFERENCE_MARK_SIZE = 10
    REFERENCE_MARK_COLOR = (0, 0, 0)
    
    OMR_THRESHOLD = 0.6
    OMR_BLACK_THRESHOLD = 127
    
    OUTPUT_DIR = "output"
    TEMP_DIR = "temp"
    
    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)