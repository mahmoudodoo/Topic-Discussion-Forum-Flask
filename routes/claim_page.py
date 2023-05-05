from app import app
from flask import render_template,jsonify, request, abort,make_response,redirect,url_for
from get_db_connection import *
from .auth_check import *
import datetime

@app.route("/claim_page/<int:claimID>", methods = ['GET','POST'])
def claim_page(claimID):
    conn = get_db_connection()
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
    postingUser = conn.execute(f"SELECT * FROM user WHERE userID == '{claim['postingUser']}'").fetchone()
    data["postingUser"] = postingUser["userName"]
    data["claim_header"] = claim["text"]
    data["creationTime"] = claim["creationTime"]
    data["repliesData"] = repliesList
    
    return render_template('claim_page.html', claim =data,claimID=claim["claimID"],is_authenticated=is_authenticated(),current_user=current_user())