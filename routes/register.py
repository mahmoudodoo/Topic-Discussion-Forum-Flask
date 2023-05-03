from app import app
from flask import render_template, request
from get_db_connection import *

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, user_password,email) VALUES (?, ?, ?)",
                (f'{username}', f'{password}', f'{email}')
                )
        conn.commit()
        conn.close()
    return render_template('register.html')