from flask import Flask, request, jsonify
from data_manager import JsonDataManager

import os

app = Flask(__name__)
db = JsonDataManager()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    success, msg, user_data = db.login_user(data['username'], data['password'])
    return jsonify({"success": success, "message": msg, "user": user_data})

@app.route('/register', methods=['POST'])
def register():
    d = request.json
    success, msg = db.register_user(
        d['username'], d['fullname'], d['email'], d['phone'],
        d['neptun'], d['faculty'], d['major'], d['degree'],
        d['pass1'], d['pass2']
    )
    return jsonify({"success": success, "message": msg})

@app.route('/forum_data', methods=['GET'])
def get_forum():
    return jsonify(db.get_forum_data())

@app.route('/add_topic', methods=['POST'])
def add_topic():
    d = request.json
    db.add_topic(d['subforum_id'], d['title'], d['author'])
    return jsonify({"status": "ok"})

@app.route('/add_post', methods=['POST'])
def add_post():
    d = request.json
    db.add_post(d['subforum_id'], d['topic_id'], d['author'], d['content'])
    return jsonify({"status": "ok"})

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(db.get_all_users())

@app.route('/send_pm', methods=['POST'])
def send_pm():
    d = request.json
    db.send_private_message(d['sender'], d['receiver'], d['content'])
    return jsonify({"status": "ok"})

@app.route('/get_pms', methods=['POST'])
def get_pms():
    d = request.json
    msgs = db.get_private_messages(d['user1'], d['user2'])
    return jsonify(msgs)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    d = request.json
    db.set_online(d['username'])
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Helyi teszteléshez
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)