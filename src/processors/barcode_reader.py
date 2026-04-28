import cv2
import numpy as np
from pyzbar import pyzbar

CODE39_PATTERNS = {
    '0': 'nnnwwnwnn', '1': 'wnnwnnnnw', '2': 'nnwwnnnnw', '3': 'wnwwnnnnn',
    '4': 'nnnwwnnnw', '5': 'wnnwwnnnn', '6': 'nnwwwnnnn', '7': 'nnnwnnwnw',
    '8': 'wnnwnnwnn', '9': 'nnwwnnwnn', 'A': 'wnnnnwnnw', 'B': 'nnwnnwnnw',
    'C': 'wnwnnwnnn', 'D': 'nnnnwwnnw', 'E': 'wnnnwwnnn', 'F': 'nnwnwwnnn',
    'G': 'nnnnnwwnw', 'H': 'wnnnnwwnn', 'I': 'nnwnnwwnn', 'J': 'nnnnwwwnn',
    'K': 'wnnnnnnww', 'L': 'nnwnnnnww', 'M': 'wnwnnnnwn', 'N': 'nnnnwnnww',
    'O': 'wnnnwnnwn', 'P': 'nnwnwnnwn', 'Q': 'nnnnnnwww', 'R': 'wnnnnnwwn',
    'S': 'nnwnnnwwn', 'T': 'nnnnwnwwn', 'U': 'wwnnnnnnw', 'V': 'nwwnnnnnw',
    'W': 'wwwnnnnnn', 'X': 'nwnnwnnnw', 'Y': 'nwnnwnwnn', 'Z': 'nwnnwwnnn',
    '-': 'nwnnnnwnw', '.': 'wwnnnnwnn', ' ': 'nwwwnnnnn', '$': 'nwnwnwnnn',
    '/': 'nwnwnnnwn', '+': 'nwnnnwnwn', '%': 'nnwnwnwnn',
}


class BarcodeReader:
    def __init__(self, config):
        self.config = config
    
    def read_barcode(self, image):
        if image is None or image.size == 0:
            return None
        
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            if gray.shape[0] < 10 or gray.shape[1] < 10:
                return None
            
            barcodes = pyzbar.decode(gray)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                if barcode_data:
                    return barcode_data
            
            eq = cv2.equalizeHist(gray)
            barcodes = pyzbar.decode(eq)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                if barcode_data:
                    return barcode_data
            
            binary = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            barcodes = pyzbar.decode(binary)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                if barcode_data:
                    return barcode_data
            
            binary_eq = cv2.adaptiveThreshold(
                eq, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            barcodes = pyzbar.decode(binary_eq)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                if barcode_data:
                    return barcode_data
            
            return None
        except Exception as e:
            print(f"Error leyendo barcode: {e}")
            return None
    
    def _decode_code39(self, gray):
        try:
            h, w = gray.shape
            
            binary = (gray < 100).astype(np.uint8)
            
            row = h // 2
            bars = []
            current = binary[row, 0]
            count = 0
            
            for x in range(w):
                if binary[row, x] == current:
                    count += 1
                else:
                    bars.append(count)
                    current = binary[row, x]
                    count = 1
            bars.append(count)
            
            if len(bars) < 27:
                return None
            
            avg_narrow = sum(b for b in bars if b < 20) / max(1, sum(1 for b in bars if b < 20))
            avg_wide = sum(b for b in bars if b >= 20) / max(1, sum(1 for b in bars >= 20))
            
            if avg_wide < avg_narrow * 1.5:
                avg_wide = avg_narrow * 2
            
            chars = []
            pos = 0
            
            while pos < len(bars) - 9:
                char_pattern = []
                for i in range(9):
                    width = bars[pos + i]
                    if width < avg_wide:
                        char_pattern.append('n')
                    else:
                        char_pattern.append('w')
                    pos += 1
                
                pattern_str = ''.join(char_pattern)
                
                for char, pattern in CODE39_PATTERNS.items():
                    if pattern == pattern_str:
                        chars.append(char)
                        break
            
            if chars:
                return ''.join(chars)
            
            return None
        except:
            return None
    
    def read_barcode_from_region(self, image, x, y, w, h):
        roi = image[y:y+h, x:x+w]
        return self.read_barcode(roi)