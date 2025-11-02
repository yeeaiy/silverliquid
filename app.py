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

    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr

    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')

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
