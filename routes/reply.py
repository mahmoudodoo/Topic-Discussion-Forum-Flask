from app import app
from flask import render_template,jsonify, request, abort,redirect,url_for
from get_db_connection import *
from .auth_check import *
import datetime





@app.route("/reply", methods = ['GET','POST'])
def reply():
    conn = get_db_connection()
    
    topicID = request.args.get('topicID')
    reply = request.args.get('replyText')
    claimID = request.args.get("claimID")
    
    print(f"topicID = {topicID}")
    print(f"reply = {reply}")
    print(f"claimID = {claimID}")
    
    topic = conn.execute(f"SELECT * FROM topic WHERE topicID == '{topicID}'").fetchone()
    data = []
    cur = conn.cursor()
    
    user = current_user()
    dt_now = datetime.datetime.now()

    cur.execute("INSERT INTO replyText (postingUser, creationTime, text) VALUES (?, ?, ?)",(user['userID'], dt_now,reply))
    replyid = cur.lastrowid
    
    replyToClaimRelType=1
    cur.execute("INSERT INTO replyToClaim (reply, claim, replyToClaimRelType) VALUES (?, ?, ?)",(replyid, claimID,replyToClaimRelType))
    conn.commit()
    
    claims = conn.execute(f"SELECT * FROM claim WHERE topic == '{topicID}'").fetchall()        
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

    return render_template('reply_list.html',claims = data,topic=topic)