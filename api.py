#!env/bin/python
import json
import os
from flask import Flask, request, make_response, send_from_directory
from flask.json import jsonify
from flask_cors import CORS

from unauthorized import Unauthorized
from entities.database import Database
from entities.user import User
from entities.user_answer import UserAnswer
from similar import SimilarQuestions

app = Flask(__name__)
CORS(app)

jeopardyDB = Database('jeopardy')
appDB = Database('jeopardy_app')

ui_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')

@app.errorhandler(Unauthorized)
def handle_unauthorized(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def check_session(request):
    if 'session' not in request.cookies:
        raise Unauthorized('You need to log in')
    user = User(session=request.cookies['session'])
    if user.check_session(appDB):
        return user
    raise Unauthorized('Invalid session')

@app.route('/jeopardy', methods=['GET'])
def home_proxy():
    return send_from_directory(ui_root, 'index.html')

@app.route('/jeopardy/<path:path>', methods=['GET'])
def ui_proxy(path):
    return send_from_directory(ui_root, path)

@app.route('/login', methods=['POST'])
def login():
    user = User(request.form['name'], request.form['password'])
    if(user.login(appDB)):
        resp = make_response(json.dumps({}))
        resp.set_cookie('session', value=user.session)
        return resp
    return jsonify(user.to_dict())

@app.route('/question', methods=['POST'])
def mark_question():
    user = check_session(request)
    user_answer = UserAnswer(user, request.json['question_id'], request.json['correct'])
    user_answer.save(appDB)
    return jsonify(user_answer.to_dict())

@app.route('/question', methods=['GET'])
def get_question():
    user = check_session(request)
    jeopardyDB.execute('SELECT questions.*, categories.name as category FROM questions JOIN categories ON questions.categoryId = categories.id ORDER BY RAND() LIMIT 1')
    return json.dumps(jeopardyDB.cur.fetchall()[0])

@app.route('/similar', methods=['GET'])
def get_similar():
    user = check_session(request)
    similar_questions = SimilarQuestions(user, jeopardyDB, appDB)
    return similar_questions.get_latest_wrong()

if __name__ == '__main__':
    app.run(debug=True)

