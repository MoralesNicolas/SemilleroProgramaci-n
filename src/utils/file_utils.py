import os
import tempfile

class FileUtils:
    @staticmethod
    def ensure_dir(path):
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def get_temp_path(prefix="temp", suffix=".tmp"):
        return tempfile.mktemp(prefix=prefix, suffix=suffix)
    
    @staticmethod
    def clean_temp_files(temp_dir):
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)
