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
    conn.close()
    return render_template('reply_list.html',claims = data,topic=topic)









@app.route("/reply_claim_list", methods = ['GET','POST'])
def reply_claim_list():
    conn = get_db_connection()
    reply = request.args.get('replyText')
    claimID = request.args.get("claimID")
    print(f"reply = {reply}")
    print(f"claimID = {claimID}")
    cur = conn.cursor()
    user = current_user()
    dt_now = datetime.datetime.now()
    
    cur.execute("INSERT INTO replyText (postingUser, creationTime, text) VALUES (?, ?, ?)",(user['userID'], dt_now,reply))
    replyid = cur.lastrowid
    
    replyToClaimRelType=1
    cur.execute("INSERT INTO replyToClaim (reply, claim, replyToClaimRelType) VALUES (?, ?, ?)",(replyid, claimID,replyToClaimRelType))
    conn.commit()
    
    data = {}
    repliesList = []
    claim = conn.execute(f"SELECT * FROM claim WHERE claimID == '{claimID}'").fetchone()
    replies = conn.execute(f"""SELECT replyText.replyTextID AS reply_id, replyText.postingUser AS reply_posting_user, replyText.creationTime AS reply_creation_time, replyText.text AS reply_text
                FROM claim
                JOIN replyToClaim ON claim.claimID = replyToClaim.claim
                JOIN replyText ON replyToClaim.reply = replyText.replyTextID
                WHERE claim.claimID = {claim['claimID']} ORDER BY reply_creation_time DESC""").fetchall()
    
    for replay in replies:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{replay['reply_posting_user']}'").fetchone()
        replies_to_replies = conn.execute(f"""SELECT * FROM replyText INNER JOIN replyToReply ON replyText.replyTextID = replyToReply.reply WHERE replyToReply.parent = {replay['reply_id']}""").fetchall()
        repliesList.append(
            
             {
                "reply_id":replay["reply_id"],
                "postingUser":postingUser["userName"],
                "text":replay['reply_text'],
                "creationTime":replay['reply_creation_time'],
                "replies_to_replies":replies_to_replies
        }   
            
        )

    data["postingUser"] = claim["postingUser"]
    data["claim_header"] = claim["text"]
    data["creationTime"] = claim["creationTime"]
    data["repliesData"] = repliesList
    conn.close()
    return render_template('relpy_claim_list.html', claim =data,claimID=claim["claimID"])


@app.route("/reply_to_reply", methods = ['GET','POST'])
def reply_to_reply():
    conn = get_db_connection()
    replytoreply = request.args.get('replytoreplytext')
    parentReplyId = request.args.get("parentReplyId")
    claimID = request.args.get("claimID")
    cur = conn.cursor()
    user = current_user()
    dt_now = datetime.datetime.now()
    
    cur.execute("INSERT INTO replyText (postingUser, creationTime, text) VALUES (?, ?, ?)",(user['userID'], dt_now,replytoreply))
    replyid = cur.lastrowid
    
    replyToReplyRelType=1
    cur.execute("INSERT INTO replyToReply (reply, parent, replyToReplyRelType) VALUES (?, ?, ?)",(replyid, parentReplyId,replyToReplyRelType))
    conn.commit()
    
    data = {}
    repliesList = []
    claim = conn.execute(f"SELECT * FROM claim WHERE claimID == '{claimID}'").fetchone()
    replies = conn.execute(f"""SELECT replyText.replyTextID AS reply_id, replyText.postingUser AS reply_posting_user, replyText.creationTime AS reply_creation_time, replyText.text AS reply_text
                FROM claim
                JOIN replyToClaim ON claim.claimID = replyToClaim.claim
                JOIN replyText ON replyToClaim.reply = replyText.replyTextID
                WHERE claim.claimID = {claim['claimID']} ORDER BY reply_creation_time DESC""").fetchall()
    
    
    
    for replay in replies:
        postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{replay['reply_posting_user']}'").fetchone()
        replies_to_replies = conn.execute(f"""SELECT * FROM replyText INNER JOIN replyToReply ON replyText.replyTextID = replyToReply.reply WHERE replyToReply.parent = {replay['reply_id']}""").fetchall()
        replies_to_replies_list = []
        for rep in replies_to_replies:
            postingUser2 = conn.execute(f"SELECT * FROM user WHERE userID == '{rep['postingUser']}'").fetchone()
            replies_to_replies_list.append(
                {
                    "postingUser":postingUser2["userName"],
                    "text":rep['text'],
                    "creationTime":rep['creationTime']
                    
                }
            )
        repliesList.append(
            
             {
                "reply_id":replay["reply_id"],
                "postingUser":postingUser["userName"],
                "text":replay['reply_text'],
                "creationTime":replay['reply_creation_time'],
                "replies_to_replies":replies_to_replies_list
        }   
            
        )

    data["postingUser"] = claim["postingUser"]
    data["claim_header"] = claim["text"]
    data["creationTime"] = claim["creationTime"]
    data["repliesData"] = repliesList
    conn.close()
    return render_template('reply_to_reply_list.html',claim=data,claimID=claim["claimID"])