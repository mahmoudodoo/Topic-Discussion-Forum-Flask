from app import app
from flask import render_template,jsonify, request, abort,redirect,url_for
from get_db_connection import *
from .auth_check import *





@app.route("/", methods = ['GET','POST'])
def home():
    conn = get_db_connection()
    topics = conn.execute('SELECT * FROM topic').fetchall()
    data = []
    for topic in topics:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{topic['postingUser']}'").fetchone()
        data.append(
            {"id":topic['topicID'],
             "title":topic['topicName'],
             "postingUser":postingUser["userName"],
             "category":topic['category'],
             "creationTime":topic['creationTime'],
             "topicID":topic['topicID']
             }
        )
    if request.method=='POST':
        cur = conn.cursor()
        title = request.form.get('titleinput')
        category = request.form.get('category')
        user = current_user()
        cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            (title ,user['userID'],category)
            )
        conn.commit()
        return redirect(url_for('home'))
    conn.close()


    return render_template('home.html',topics=data,is_authenticated=is_authenticated(),current_user=current_user())


@app.route('/filter_by_category/', methods = ['GET'])
def filter_by_category():
    conn = get_db_connection()
    choice = request.args.get('choice')

    topics = conn.execute('SELECT * FROM topic WHERE category = ? ',(choice,)).fetchall()
    if choice =="All":
        topics = conn.execute('SELECT * FROM topic').fetchall()
    data = []
    for topic in topics:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{topic['postingUser']}'").fetchone()
        data.append(
            {"id":topic['topicID'],
             "title":topic['topicName'],
             "postingUser":postingUser["userName"],
             "category":topic['category'],
             "creationTime":topic['creationTime'],
             "topicID":topic['topicID']
             }
        )
        print(topic['category'])
    conn.close()

    return render_template('filtered_category.html',data=data)


@app.route('/filter_by_search/', methods = ['GET'])
def filter_by_search():
    conn = get_db_connection()
    value = request.args.get('value')
    print(value)
    topics = conn.execute(f"SELECT * FROM topic WHERE topicName LIKE '%{value}%'").fetchall()
    if value ==" ":
        topics = conn.execute('SELECT * FROM topic').fetchall()
    data = []
    for topic in topics:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{topic['postingUser']}'").fetchone()
        data.append(
            {"id":topic['topicID'],
             "title":topic['topicName'],
             "postingUser":postingUser["userName"],
             "category":topic['category'],
             "creationTime":topic['creationTime'],
             "topicID":topic['topicID']
             }
        )
    conn.close()

    return render_template('filtered_category.html',data=data)