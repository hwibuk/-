// joystick.js
document.getElementById('joy-up').addEventListener('click', () => addLog('정상', '수동 제어: 전진 (↑)'));
document.getElementById('joy-down').addEventListener('click', () => addLog('정상', '수동 제어: 후진 (↓)'));
document.getElementById('joy-left').addEventListener('click', () => addLog('정상', '수동 제어: 좌회전 (←)'));
document.getElementById('joy-right').addEventListener('click', () => addLog('정상', '수동 제어: 우회전 (→)'));
document.getElementById('joy-stop').addEventListener('click', () => addLog('주의', '수동 제어: 긴급 정지 (■)'));
