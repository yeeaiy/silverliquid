import os
import threading
import requests
import time
from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 안전한 시크릿 키

visit_records = []

def keep_alive():
    while True:
        time.sleep(300)  # 5분마다 ping
        try:
            url = os.environ.get('SELF_URL', 'https://silverliquid.onrender.com')
            requests.get(url)
            print("Keep-alive ping sent")
        except Exception as e:
            print(f"Keep-alive failed: {e}")

threading.Thread(target=keep_alive, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')

        ADMIN_ID = 'adm1n'
        ADMIN_PW = 'thisispw'

        if id == ADMIN_ID and pw == ADMIN_PW:
            session['logged_in'] = True
            return redirect(url_for('admin_page'))
        else:
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'
    
    return render_template('login.html', error=error)


@app.route('/record', methods=['POST'])
def record():
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.remote_addr

    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')

    visit_records.insert(0, {'ip': ip, 'time': now})
    if len(visit_records) > 500:
        visit_records.pop()

    return jsonify({'ip': ip, 'time': now})


@app.route('/admin')
def admin_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html', records=visit_records)


@app.route('/clear', methods=['POST'])
def clear():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    visit_records.clear()
    return redirect(url_for('admin_page'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
