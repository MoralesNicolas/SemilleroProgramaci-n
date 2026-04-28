import io
from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image

class BarcodeGenerator:
    def __init__(self, config):
        self.config = config
    
    def generate(self, id_number):
        writer = ImageWriter()
        writer.set_options({
            'module_width': 0.3,
            'module_height': 10,
            'quiet_zone': 6,
            'font_size': 10,
            'text_distance': 3,
            'background': 'white',
            'foreground': 'black',
            'write_text': True,
        })
        
        barcode = Code39(id_number, writer=writer, add_checksum=False)
        img_buffer = io.BytesIO()
        barcode.write(img_buffer)
        img_buffer.seek(0)
        
        img = Image.open(img_buffer)
        img = img.convert('RGB')
        return img
