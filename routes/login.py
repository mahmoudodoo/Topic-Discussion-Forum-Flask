from app import app
from flask import Flask, render_template, request, make_response, flash, redirect, url_for
from get_db_connection import *

@app.route('/login', methods = ['GET','POST'])
def login():
    conn = get_db_connection()
    username = request.cookies.get('username')
    if username:
        return make_response(redirect('/'))
    
    
    
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = conn.execute('SELECT * FROM user WHERE userName = ?',(username,)).fetchone()  
        if username==user['userName'] and password==user['passwordHash']:
            flash("Successful login", "success")
            resp = make_response(redirect('/'))
            resp.set_cookie('username', username)
            return resp
        else:
            flash("Wrong username or password", "danger")
    return redirect(url_for('home'))


@app.route('/logout', methods = ['GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('username')
    return resp

