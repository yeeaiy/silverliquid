import os
from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 안전한 랜덤 시크릿 키 생성

visit_records = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')

        ADMIN_ID = 'admin'
        ADMIN_PW = '1234'

        if id == ADMIN_ID and pw == ADMIN_PW:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='아이디 또는 비밀번호가 올바르지 않습니다.')
    
    return render_template('login.html')

@app.route('/record', methods=['POST'])
def record():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    visit_records.insert(0, {'ip': ip, 'time': now})
    if len(visit_records) > 500:
        visit_records.pop()
    return jsonify({'ip': ip, 'time': now})

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html', records=visit_records)

@app.route('/clear', methods=['POST'])
def clear():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    visit_records.clear()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
