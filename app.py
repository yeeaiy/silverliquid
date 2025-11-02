from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime, timezone, timedelta

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

@app.route('/admin')
def admin():
    return render_template('admin.html', records=visit_records)

@app.route('/clear', methods=['POST'])
def clear():
    visit_records.clear()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
