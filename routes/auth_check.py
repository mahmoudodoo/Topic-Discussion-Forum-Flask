from flask import request,redirect,url_for
from get_db_connection import *


def is_authenticated():
    if request.cookies.get('username'):
        return True
    else:
        return False
    
def current_user():
    if is_authenticated():
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE userName = ?',(request.cookies.get('username'),)).fetchone() 
        return user
    else:
        pass
    