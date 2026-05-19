import socket
import threading
import time
import json
import config

class AresDiscovery:
    def __init__(self, db, broadcast_port=config.START_BROADCAST_PORT):
        self.db = db
        self.port = broadcast_port
        self.is_running = False

    def start(self):
        self.is_running = True
        # خيط للبث المستمر (صرخة الأداة لتخبر الآخرين بوجودها)
        threading.Thread(target=self._broadcast_pulse, daemon=True).start()
        # خيط للاستماع (استقبال نبضات الآخرين)
        threading.Thread(target=self._listen_for_nodes, daemon=True).start()

    def _broadcast_pulse(self):
        """بث نبضات متكررة لجذب العقد المحيطة"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.is_running:
            try:
                # رسالة البث تحتوي على هوية الجهاز
                pulse = {"node_id": config.NODE_IDENTITY, "status": "ACTIVE"}
                sock.sendto(json.dumps(pulse).encode(), ('255.255.255.255', self.port))
            except: pass
            time.sleep(2) # البث كل ثانيتين (سريع جداً)

    def _listen_for_nodes(self):
        """الاستماع الفوري لأي نبضة في الشبكة"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        while self.is_running:
            try:
                data, addr = sock.recvfrom(1024)
                node_info = json.loads(data.decode())
                if node_info['node_id'] != config.NODE_IDENTITY:
                    # تسجيل العقدة المكتشفة في قاعدة البيانات فوراً
                    self.db.update_node(node_info['node_id'], addr[0])
            except: pass

