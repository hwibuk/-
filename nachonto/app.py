from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os

# 1. 모델 임포트
try:
    from models.robot_state import robot_manager
except ImportError:
    print("Error: models/robot_state.py 파일을 찾을 수 없습니다.")

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

CORS(app)

# 2. 메인 페이지 (index.html 띄우기)
@app.route('/')
def index():
    return render_template('index.html')

# 3. 로봇 상태 조회 API (JS의 dashboard.js에서 1초마다 호출)
@app.route('/api/robot/status', methods=['GET'])
def get_robot_status():
    """실시간 로봇 데이터를 반환합니다."""
    # 만약 robot_manager에 get_current_state() 함수가 있다면 아래처럼 사용하세요.
    # 없으면 그냥 robot_manager.state를 반환하도록 수정 가능합니다.
    return jsonify(robot_manager.get_current_state())

# 4. 로봇 제어 API (중복되었던 함수를 하나로 통합)
@app.route('/api/robot/control', methods=['POST'])
def control_robot():
    """조이스틱(move, stop) 및 기타 버튼 명령을 통합 처리합니다."""
    data = request.json
    action = data.get('action') # 'move', 'stop' 등
    direction = data.get('direction') # [추가] 'up', 'down', 'left', 'right' 방향 정보 수신

    if action == 'move':
        robot_manager.state["status"] = "moving"
        # [추가] 로봇 매니저의 상태에 방향 정보를 저장합니다.
        robot_manager.state["direction"] = direction
        return jsonify({"result": "success", "status": "moving", "direction": direction})

    elif action == 'stop':
        robot_manager.state["status"] = "idle"
        # [추가] 정지 시 방향 정보 초기화 (선택 사항)
        robot_manager.state["direction"] = None
        return jsonify({"result": "success", "status": "idle"})

    # 조이스틱 외에 다른 버튼(적재함 등) 명령 처리 로직
    # 만약 robot_manager에 update_command 함수가 있다면 여기서 호출
    if hasattr(robot_manager, 'update_command'):
        result = robot_manager.update_command(data)
        return jsonify(result)

    return jsonify({"result": "success", "action": action})

if __name__ == '__main__':
    # 현재 8000번 포트로 설정되어 있습니다.
    # 브라우저 접속 시 http://localhost:8000 으로 접속하세요.
    app.run(host='0.0.0.0', port=8000, debug=True)
