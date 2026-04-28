import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, config):
        self.config = config
    
    def load_image(self, image_path):
        return cv2.imread(image_path)
    
    def convert_to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    def threshold(self, image, threshold_value=127):
        _, thresh = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)
        return thresh
    
    def find_contours(self, image):
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def find_reference_marks(self, image):
        gray = self.convert_to_grayscale(image)
        thresh = self.threshold(gray, 200)
        
        contours = self.find_contours(thresh)
        squares = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 50 < area < 500:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h
                if 0.8 < aspect_ratio < 1.2:
                    squares.append((x, y, w, h))
        
        squares.sort(key=lambda s: (s[1], s[0]))
        return squares[:4] if len(squares) >= 4 else squares
    
    def correct_perspective(self, image, reference_marks):
        if len(reference_marks) < 4:
            return image
        
        corners = np.zeros((4, 2), dtype="float32")
        
        reference_marks = sorted(reference_marks, key=lambda s: (s[1], s[0]))
        
        top_left = min(reference_marks[:2], key=lambda s: s[0])
        top_right = max(reference_marks[:2], key=lambda s: s[0])
        bottom_left = min(reference_marks[-2:], key=lambda s: s[0])
        bottom_right = max(reference_marks[-2:], key=lambda s: s[0])
        
        corners[0] = [top_left[0] + top_left[2]/2, top_left[1] + top_left[3]/2]
        corners[1] = [top_right[0] + top_right[2]/2, top_right[1] + top_right[3]/2]
        corners[2] = [bottom_left[0] + bottom_left[2]/2, bottom_left[1] + bottom_left[3]/2]
        corners[3] = [bottom_right[0] + bottom_right[2]/2, bottom_right[1] + bottom_right[3]/2]
        
        width = 612
        height = 792
        
        dst = np.array([
            [0, 0],
            [width - 1, 0],
            [0, height - 1],
            [width - 1, height - 1]
        ], dtype="float32")
        
        matrix = cv2.getPerspectiveTransform(corners, dst)
        warped = cv2.warpPerspective(image, matrix, (int(width), int(height)))
        
        return warped
    
    def extract_bubble_region(self, image, x, y, radius):
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.circle(mask, (int(x), int(y)), int(radius), 255, -1)
        return cv2.bitwise_and(image, image, mask=mask)
    
    def calculate_fill_percentage(self, bubble_region):
        if len(bubble_region.shape) == 3:
            bubble_region = cv2.cvtColor(bubble_region, cv2.COLOR_BGR2GRAY)
        
        total_pixels = cv2.countNonZero(bubble_region)
        total_area = bubble_region.shape[0] * bubble_region.shape[1]
        
        if total_area == 0:
            return 0
        
        return total_pixels / total_area