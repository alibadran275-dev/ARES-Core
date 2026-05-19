import time
import random

class AresHopper:
    def __init__(self, base_port=8888):
        self.base_port = base_port
        
    def get_current_port(self):
        """توليد منفذ عشوائي بناءً على الوقت الحالي (القفز الترددي)"""
        # القفز كل 300 ثانية (5 دقائق)
        time_slot = int(time.time() / 300)
        random.seed(time_slot)
        return self.base_port + random.randint(0, 50)

