import base64
import os

class AresCrypto:
    def __init__(self, master_key="ARES_ALPHA_PROTO_2026"):
        self.master_key = master_key

    def seal_envelope(self, plain_text: str, dynamic_salt: str = "") -> str:
        """تشفير وتغليف النصوص"""
        key = self.master_key + dynamic_salt
        cipher_chars = []
        for i, char in enumerate(plain_text):
            key_c = key[i % len(key)]
            cipher_chars.append(chr(ord(char) ^ ord(key_c)))
        cipher_text = "".join(cipher_chars)
        return base64.b64encode(cipher_text.encode('utf-8')).decode('utf-8')

    def open_envelope(self, cipher_text: str, dynamic_salt: str = "") -> str:
        """فك تغليف وقراءة النصوص المشفرة"""
        try:
            key = self.master_key + dynamic_salt
            raw_cipher = base64.b64decode(cipher_text.encode('utf-8')).decode('utf-8')
            plain_chars = []
            for i, char in enumerate(raw_cipher):
                key_c = key[i % len(key)]
                plain_chars.append(chr(ord(char) ^ ord(key_c)))
            return "".join(plain_chars)
        except Exception:
            return None

    # --- الميزة الجديدة بالبلدي: تحويل الصور والملفات لنصوص مشفرة ---
    def encode_file_to_envelope(self, file_path: str) -> str:
        """تحويل الملف بالكامل إلى نص مشفر جاهز للإرسال"""
        if not os.path.exists(file_path):
            return None
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        # تحويل البايتات لنص عادي ثم تشفيره بنفس الطريقة
        raw_base64 = base64.b64encode(file_bytes).decode('utf-8')
        return self.seal_envelope(raw_base64)

    def decode_envelope_to_file(self, cipher_text: str, output_path: str):
        """تحويل النص المشفر المستلم إلى ملف أصلي وحفظه"""
        try:
            raw_base64 = self.open_envelope(cipher_text)
            if raw_base64:
                file_bytes = base64.b64decode(raw_base64.encode('utf-8'))
                with open(output_path, "wb") as f:
                    f.read(file_bytes)
                return True
        except Exception:
            pass
        return False

