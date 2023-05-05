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
    conn.execute(f"UPDATE topic SET views = views + 1 WHERE topicID = {topic['topicID']}")
    conn.commit()
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
        for replay in replies:
            postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{replay['reply_posting_user']}'").fetchone()
            repliesData.append({
                "reply_id":replay["reply_id"],
                "postingUser":postingUser["userName"],
                "text":replay['reply_text'],
                "creationTime":replay['reply_creation_time'],
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
    if request.method=='POST':
        cur = conn.cursor()
        claimtext = request.form.get('claimtext')
        topicID = request.form.get('topicID')
        user = current_user()
        cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (topicID ,user['userID'],claimtext)
            )
        conn.commit()
        return redirect(url_for('claim',topicID=topicID))
    
    conn.close()
    return render_template('claim.html',claims = data,topic=topic, is_authenticated=is_authenticated(),current_user=current_user())