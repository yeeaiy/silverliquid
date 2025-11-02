from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# 방문 기록 저장 (메모리)
visit_records = []

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 로그인 페이지
@app.route('/login')
def login():
    return render_template('login.html')

# 방문 기록 등록 (AJAX POST)
@app.route('/record', methods=['POST'])
def record():
    ip = request.remote_addr
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    visit_records.insert(0, {'ip': ip, 'time': now})
    if len(visit_records) > 500:
        visit_records.pop()
    return jsonify({'ip': ip, 'time': now})

# 관리자 페이지
@app.route('/admin')
def admin():
    return render_template('admin.html', records=visit_records)

# 방문 기록 전체 삭제
@app.route('/clear', methods=['POST'])
def clear():
    visit_records.clear()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)