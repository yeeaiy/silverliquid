from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime, timezone, timedelta
from threading import Thread
import time
import requests

app = Flask(__name__)
visit_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/record', methods=['POST'])
def record():
    # X-Forwarded-For 헤더에서 실제 클라이언트 IP 가져오기
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr

    # KST 시간
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')

    # 방문 기록 저장
    visit_records.insert(0, {'ip': ip, 'time': now})
    if len(visit_records) > 500:
        visit_records.pop()

    return jsonify({'ip': ip, 'time': now})

@app.route('/silv3')
def silv3():
    return render_template('silv3.html', records=visit_records)

@app.route('/clear', methods=['POST'])
def clear():
    visit_records.clear()
    return redirect(url_for('silv3'))

# 서버 자기 자신 ping 기능
def keep_alive(url, interval=300):
    """
    url: 서버의 외부 URL (Render에서 제공하는 URL)
    interval: ping 간격 (초, 기본 5분)
    """
    while True:
        try:
            requests.get(url)
            print(f"[Ping] {url} 성공")
        except Exception as e:
            print(f"[Ping] {url} 실패: {e}")
        time.sleep(interval)

if __name__ == '__main__':
    # Render에서 배포된 외부 URL로 변경하세요!
    server_url = "https://YOUR-RENDER-DOMAIN.onrender.com/"
    thread = Thread(target=keep_alive, args=(server_url,))
    thread.daemon = True
    thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
