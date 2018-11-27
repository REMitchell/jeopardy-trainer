from pymysql.err import InternalError
from entities.database import Database

class UserAnswer:
    def __init__(self, user, question_id, correct, id=None):
        self.user = user
        self.question_id = question_id
        self.correct = correct
        self.id = id

    def save(self, db):
        db.cur.execute("INSERT INTO app_user_answers (user_id, question_id, correct) VALUES (%s, %s, %s)", (self.user.id, self.question_id, self.correct))
        db.conn.commit()
        self.id = db.cur.lastrowid
    
    def to_dict(self):
        return { 'id': self.id, 'question_id': self.question_id, 'correct': self.correct }