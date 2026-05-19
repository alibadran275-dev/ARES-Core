import os
import sys
import time
import json
import sqlite3
from database import KernelDatabase
from crypto import AresCrypto
from discovery import AresDiscovery
from relay import AresRelay
from file_manager import AresFileManager
import config

def display_status():
    """الواجهة العلوية السيمبل والحديثة لـ ARES"""
    print(f"── ARES INTELLIGENCE CORE v{config.VERSION} ─────────────────────────────")
    print(f" [●] NODE ID    : {config.NODE_IDENTITY}")
    print(f" [●] NET STATUS : DECENTRALIZED MESH ACTIVE")
    print(f" [●] STORAGE    : KERNEL.DB & FILE_MANAGER LINKED")
    print("─────────────────────────────────────────────────────────────────")

def main():
    os.system('clear')
    display_status()
    
    # تهيئة المنظومة البرمجية الموزعة
    db = KernelDatabase()
    crypto = AresCrypto(master_key=config.DEFAULT_MASTER_KEY)
    file_mgr = AresFileManager()
    
    # ربط خدمات الشبكة بالمنافذ الديناميكية المقاومة للتعارض
    discovery = AresDiscovery(db, broadcast_port=config.START_BROADCAST_PORT)
    relay = AresRelay(db, crypto, relay_port=config.START_RELAY_PORT)

    # إقلاع الرادارات في الخلفية بصمت
    discovery.start()
    relay.start()
    
    print("[+] Subsystems operational. Awaiting command...\n")
    
    while True:
        print(" [1] View Neighborhood  [2] Send Text  [3] Send File/Image  [4] Logs  [5] Exit")
        choice = input(" ares://core > ").strip()

        if choice == "1":
            nodes = db.get_active_topology()
            print("\n── DISCOVERED NODES ──")
            if not nodes:
                print(" [-] Radio silence. No nearby ARES nodes cached.")
            for node in nodes:
                print(f" ▷ {node['node_id']} | IP: {node['last_known_ip']} | {node['last_seen']}")
            print("──────────────────────\n")
                
        elif choice == "2":
            # إرسال رسالة نصية عادية مشفرة
            next_hop = input(" ↳ Next Hop IP: ").strip()
            final_dest = input(" ↳ Final Destination ID: ").strip()
            msg = input(" ↳ Secret Message: ")
            
            packet_id = f"TXT-{int(time.time())}"
            payload_data = json.dumps({"type": "TEXT", "content": msg})
            sealed_payload = crypto.seal_envelope(payload_data)
            
            packet = {
                "packet_id": packet_id,
                "next_hop": next_hop,
                "destination": final_dest,
                "payload": sealed_payload
            }
            
            print(" [*] Encrypting and dispatching text packet...")
            relay.forward_packet(next_hop, packet)
            print(" [✓] Injected successfully.\n")

        elif choice == "3":
            # الميزة العملاقة الجديدة: إرسال وتشفير الصور والملفات
            next_hop = input(" ↳ Next Hop IP: ").strip()
            final_dest = input(" ↳ Final Destination ID: ").strip()
            file_path = input(" ↳ Target File/Image Path (e.g. photo.jpg): ").strip()
            
            print(" [*] Reading and isolating file bytes...")
            encoded_str, file_name = file_mgr.prepare_file_for_envelope(file_path)
            
            if not encoded_str:
                print(" [-] Error: Target file not found inside directory.\n")
                continue
                
            packet_id = f"FIL-{int(time.time())}"
            payload_data = json.dumps({"type": "FILE", "filename": file_name, "content": encoded_str})
            sealed_payload = crypto.seal_envelope(payload_data)
            
            packet = {
                "packet_id": packet_id,
                "next_hop": next_hop,
                "destination": final_dest,
                "payload": sealed_payload
            }
            
            print(f" [*] Sealing [{file_name}] inside onion cipher... Transmitting...")
            relay.forward_packet(next_hop, packet)
            print(" [✓] File packet successfully injected into network payload.\n")

        elif choice == "4":
            conn = db._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT packet_id, destination, status FROM secure_pipeline")
            rows = cursor.fetchall()
            print("\n── PIPELINE DATA INTERCEPT LOGS ──")
            for r in rows:
                print(f" • {r['packet_id']} ➔ {r['destination']} [{r['status']}]")
            if not rows:
                print(" [-] Pipeline queue clean.")
            print("──────────────────────────────────\n")
            conn.close()

        elif choice == "5":
            print("\n[!] Flushed. Halting ARES combat intelligence node.")
            discovery.is_running = False
            relay.is_running = False
            sys.exit(0)
            
        else:
            print(" [-] Command unrecognized.\n")

if __name__ == "__main__":
    # هذا السطر الذكي يقوم بمعالجة الطرود عند استقبالها تلقائياً إذا كانت تحتوي على ملفات
    # عن طريق ربط موديول الاستقبال بمدير الملفات مباشرة
    def advanced_packet_processor(packet_id, decrypted_raw):
        try:
            data = json.loads(decrypted_raw)
            if data.get("type") == "TEXT":
                print(f"\n[!!!] TARGET TEXT PACKET ARRIVED [ID: {packet_id}] -> {data['content']}\n")
            elif data.get("type") == "FILE":
                fm = AresFileManager()
                saved_at = fm.write_envelope_to_file(data['content'], data['filename'])
                print(f"\n[!!!] TARGET FILE PACKET ASSEMBLED SECURELY [ID: {packet_id}]")
                print(f"[SAVED AT]: {saved_at}\n")
        except Exception:
            pass

    # حقن وظيفة المعالجة المتقدمة داخل نظام الريلاي للتعامل التلقائي مع البيانات الضخمة
    import relay
    def _patched_handle_packet(self, client_sock, addr):
        try:
            raw_data = client_sock.recv(65535).decode('utf-8') # تكبير حجم البافر لاستقبال الصور الكبيرة
            if not raw_data: return
            packet = json.loads(raw_data)
            packet_id = packet.get("packet_id")
            next_hop = packet.get("next_hop")
            final_dest = packet.get("destination")
            payload = packet.get("payload")

            conn = self.db._get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO secure_pipeline (packet_id, destination, payload, routing_path, status) VALUES (?, ?, ?, ?, 'TRANSIT')", (packet_id, final_dest, payload, next_hop))
            conn.commit()

            if final_dest == config.NODE_IDENTITY or final_dest == "ME":
                decrypted_raw = self.crypto.open_envelope(payload)
                advanced_packet_processor(packet_id, decrypted_raw)
                cursor.execute("UPDATE secure_pipeline SET status='DELIVERED' WHERE packet_id=?", (packet_id,))
                conn.commit()
            else:
                self.forward_packet(next_hop, packet)
            conn.close()
        except Exception: pass
        finally: client_sock.close()

    AresRelay._handle_packet = _patched_handle_packet
    main()

