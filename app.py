from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# 방문 기록 저장 (메모리)
visit_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/record', methods=['POST'])
def record():
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = ip.split(',')[0].strip()  # 여러 프록시 거친 경우 첫 번째 IP 사용

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
