import socket
import threading
import json
import config
from hopper import AresHopper

class AresRelay:
    def __init__(self, db, crypto, relay_port=config.START_RELAY_PORT):
        self.db = db
        self.crypto = crypto
        self.relay_port = relay_port
        self.hopper = AresHopper(relay_port)
        self.is_running = False

    def start(self):
        self.is_running = True
        threading.Thread(target=self._server_core, daemon=True).start()

    def _server_core(self):
        while self.is_running:
            current_port = self.hopper.get_current_port()
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                server.bind(('0.0.0.0', current_port))
                server.listen(15)
                # السيرفر يعمل الآن على المنفذ المتغير
                while self.is_running:
                    # نتحقق من تغيير المنفذ كل دورة
                    if self.hopper.get_current_port() != current_port:
                        break 
                    
                    server.settimeout(1.0)
                    try:
                        client_sock, addr = server.accept()
                        threading.Thread(target=self._handle_packet, args=(client_sock, addr), daemon=True).start()
                    except socket.timeout:
                        continue
            except Exception:
                time.sleep(1)
            finally:
                server.close()

    def _handle_packet(self, client_sock, addr):
        try:
            raw_data = client_sock.recv(65535).decode('utf-8')
            if not raw_data: return
            
            packet = json.loads(raw_data)
            # (نفس منطق المعالجة السابق المدمج في core.py)
            # ... المعالجة ...
        finally:
            client_sock.close()

    def forward_packet(self, target_ip, packet_dict):
        try:
            # عند الإرسال، نستخدم نفس منفذ القفز الحالي للمستقبل
            port = self.hopper.get_current_port()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target_ip, port))
            sock.sendall(json.dumps(packet_dict).encode('utf-8'))
            sock.close()
            return True
        except Exception:
            return False

