import threading
import time
import random

class RobotState:
    def __init__(self):
        self.state = {
            "robot_id": "SEONGSU_03",
            "location": {"floor": "1F", "x": 100, "y": 200},
            "status": "idle", # idle, moving, charging, error
            "speed": 0.0,
            "battery_percent": 98.0,
            "battery_voltage": 49.0,
            "cpu_usage": 2.0,
            "memory_usage": 33.0,
        }
        self.lock = threading.Lock()
        self.running = True
        threading.Thread(target=self._simulate_robot, daemon=True).start()

    def _simulate_robot(self):
        while self.running:
            with self.lock:
                # 상태별 데이터 변화
                if self.state["status"] == "moving":
                    self.state["speed"] = round(random.uniform(0.5, 1.5), 2)
                    self.state["battery_percent"] -= 0.01
                    self.state["location"]["x"] += random.uniform(-1, 1)
                    self.state["location"]["y"] += random.uniform(-1, 1)
                else:
                    self.state["speed"] = 0.0

                # 하드웨어 리소스 노이즈
                self.state["cpu_usage"] = round(random.uniform(1.0, 10.0), 1)
                self.state["memory_usage"] = round(random.uniform(30.0, 35.0), 1)
            
            time.sleep(1)

    def get_current_state(self):
        with self.lock:
            return self.state.copy()

# 싱글톤 인스턴스
robot_manager = RobotState()
