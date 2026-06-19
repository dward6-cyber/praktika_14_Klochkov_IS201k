from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-guestbook'

ekat_tz = ZoneInfo("Asia/Yekaterinburg")

messages = [
    {
        "id": 1,
        "name": "Иван Иванов",
        "created_at": datetime.now(ekat_tz).strftime("%d.%m.%Y %H:%M"),
        "message": "Отличный сайт! Всё очень красиво оформлено."
    },
    {
        "id": 2,
        "name": "Петр Петров",
        "created_at": datetime.now(ekat_tz).strftime("%d.%m.%Y %H:%M"),
        "message": "Тестирую отправку сообщений в гостевой книге."
    }
]

@app.route('/')
def index():
    logged_in = session.get('logged_in', False)
    username = session.get('username', '')
    
    return render_template(
        'index.html', 
        logged_in=logged_in, 
        username=username, 
        messages=messages, 
        total_count=len(messages)
    )

@app.route('/add', methods=['POST'])
def add_message():
    name = request.form.get('name')
    message_text = request.form.get('message')
    
    if name and message_text:
        new_id = max([msg['id'] for msg in messages]) + 1 if messages else 1
        current_time = datetime.now(ekat_tz).strftime("%d.%m.%Y %H:%M")
        messages.append({
            "id": new_id,
            "name": name,
            "created_at": current_time,
            "message": message_text
        })
        
    return redirect(url_for('index'))

@app.route('/delete/<int:msg_id>')
def delete_message(msg_id):
    if session.get('logged_in'):
        global messages
        messages = [msg for msg in messages if msg['id'] != msg_id]
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Неверный логин или пароль!'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
