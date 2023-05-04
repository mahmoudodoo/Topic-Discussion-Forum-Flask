from app import app
from flask import render_template,jsonify, request, abort,make_response,redirect,url_for
from get_db_connection import *
from .auth_check import *
import datetime

@app.route("/claim/<int:topicID>", methods = ['GET','POST'])
def claim(topicID):
    conn = get_db_connection()
    claims = conn.execute(f"SELECT * FROM claim WHERE topic == '{topicID}'").fetchall()
    topic = conn.execute(f"SELECT * FROM topic WHERE topicID == '{topicID}'").fetchone()
    data = []
    cur = conn.cursor()

    for claim in claims:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{claim['postingUser']}'").fetchone()
        
        replies = conn.execute(f"""SELECT replyText.replyTextID AS reply_id, replyText.postingUser AS reply_posting_user, replyText.creationTime AS reply_creation_time, replyText.text AS reply_text
                FROM claim
                JOIN replyToClaim ON claim.claimID = replyToClaim.claim
                JOIN replyText ON replyToClaim.reply = replyText.replyTextID
                WHERE claim.claimID = {claim['claimID']} ORDER BY reply_creation_time DESC""").fetchall()
        repliesData = []
        for re in replies:
            postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{re['reply_posting_user']}'").fetchone()
            repliesData.append({
                "reply_id":re["reply_id"],
                "postingUser":postingUser["userName"],
                "text":re['reply_text'],
                "creationTime":re['reply_creation_time'],
        })
        
        data.append(
            {"claimID":claim['claimID'],
             "postingUser":postingUser["userName"],
             "creationTime":claim['creationTime'],
             "updateTime":claim['updateTime'],
             "text":claim['text'],
             "repliesData":repliesData,
             "topicID":topicID
             }
        )

    conn.close()
    return render_template('claim.html',claims = data,topic=topic)