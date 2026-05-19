import socket

# المعايير الهندسية لشبكة ARES
VERSION = "1.0.0"
DEFAULT_MASTER_KEY = "ARES_ALPHA_PROTO_2026"

# منافذ البث والاستماع الافتراضية
START_BROADCAST_PORT = 9999
START_RELAY_PORT = 8888

# معرف العقدة الفريد المبني على اسم الجهاز الحالي في تيرماكس
NODE_IDENTITY = f"ARES-NODE-{socket.gethostname()}"

# مسار مجلد الطرود المستلمة (الصور والملفات المخفية)
RECEIVED_DIR = "ares_received"

