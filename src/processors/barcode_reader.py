import cv2
from pyzbar import pyzbar

class BarcodeReader:
    def __init__(self, config):
        self.config = config
    
    def read_barcode(self, image):
        barcodes = pyzbar.decode(image)
        
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            
            if barcode_type in ['CODE128', 'EAN13', 'CODE39']:
                return barcode_data
        
        return None
    
    def read_barcode_from_region(self, image, x, y, w, h):
        roi = image[y:y+h, x:x+w]
        return self.read_barcode(roi)