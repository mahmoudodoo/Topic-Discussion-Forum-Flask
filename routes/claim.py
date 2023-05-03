from app import app
from flask import render_template,jsonify, request, abort,make_response,redirect,url_for
from get_db_connection import *


@app.route("/claim/<int:topicID>", methods = ['GET','POST'])
def claim(topicID):
    conn = get_db_connection()
    claims = conn.execute(f"SELECT * FROM claim WHERE topic == '{topicID}'").fetchall()
    topic = conn.execute(f"SELECT * FROM topic WHERE topicID == '{topicID}'").fetchone()
    data = []
    for claim in claims:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{claim['postingUser']}'").fetchone()
        data.append(
            {"claimID":claim['claimID'],
             "postingUser":postingUser["userName"],
             "creationTime":claim['creationTime'],
             "updateTime":claim['updateTime'],
             "text":claim['text']
             }
        )
    conn.close()
    return render_template('claim.html',claims = data,topic=topic)