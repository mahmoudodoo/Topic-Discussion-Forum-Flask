from app import app
from flask import render_template, request,make_response,redirect
from get_db_connection import *
import datetime


@app.route("/register", methods=["POST","GET"])
def register():

    if request.method == 'POST':
        dt_now = datetime.datetime.now()
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,creationTime) VALUES (?, ?, ?, ?)",
                (f'{username}', f'{password}', True, dt_now)
                )
        conn.commit()
        conn.close()
        resp = make_response(redirect('/'))
        resp.set_cookie('username', username)
        return resp
    return render_template('register.html')