import os
import base64
from config import RECEIVED_DIR

class AresFileManager:
    def __init__(self):
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """إنشاء مجلد حفظ الملفات المستلمة صامتاً إذا لم يكن موجوداً"""
        if not os.path.exists(RECEIVED_DIR):
            os.makedirs(RECEIVED_DIR)

    def prepare_file_for_envelope(self, file_path: str) -> tuple:
        """تحويل الملف إلى بايتات مشفرة مبدئياً واستخراج اسمه وامتداده"""
        if not os.path.exists(file_path):
            return None, None
        
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        
        # تحويل الملف بالكامل إلى نص قابل للتمرير في الأجواء
        encoded_string = base64.b64encode(raw_bytes).decode('utf-8')
        return encoded_string, file_name

    def write_envelope_to_file(self, encoded_string: str, original_name: str) -> str:
        """إعادة بناء الملف أو الصورة المستلمة وحفظها في المجلد السري"""
        try:
            self._ensure_storage_exists()
            destination_path = os.path.join(RECEIVED_DIR, original_name)
            
            # فك حزمة البيانات وإعادة بنائها كملف أصلي
            file_bytes = base64.b64decode(encoded_string.encode('utf-8'))
            with open(destination_path, "wb") as f:
                f.write(file_bytes)
            
            return destination_path
        except Exception:
            return None

