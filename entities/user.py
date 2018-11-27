from pymysql.err import InternalError
import hashlib
import uuid

from entities.database import Database
from entities.user_answer import UserAnswer

class User:

    def __init__(self, name=None, password=None, id=None, session=None):
        self.name = name
        self.password = password
        self.id = id
        self.session = session

    def save(self, db):
        try:
            db.execute("SELECT * FROM users WHERE name=%s", (self.name))
            if db.cur.rowcount == 0:
                db.execute("INSERT INTO users (name) VALUES (%s)", (self.name))
                db.conn.commit()
                self.id = db.cur.lastrowid
            else:
                self.id = db.cur.fetchall()[0]["id"]

        except InternalError as e:
            print(e)
            db.conn.rollback()
        return self

    def check_session(self, db):
        db.execute('SELECT * FROM users WHERE session = %s', (self.session))
        if db.cur.rowcount == 0:
            return False
        else:
            user = db.cur.fetchall()[0]
            self.id = user['id']
            self.name = user['name']
            return True

    def login(self, db):
        db.execute('SELECT * FROM users WHERE name = %s AND password = %s', 
            (self.name, hashlib.sha256(bytearray(self.password, 'UTF-8')).hexdigest()))
        if db.cur.rowcount == 0:
            print(hashlib.sha256(bytearray(self.password, 'UTF-8')).hexdigest())
            return False
        else:
            self.id = db.cur.fetchall()[0]['id']
            # Create session variable
            self.session = uuid.uuid4().hex
            db.execute('UPDATE users SET session = %s WHERE id = %s', (self.session, self.id))
            db.conn.commit()
            return True
            
    def logout(self, db):
        db.execute('UPDATE users SET session = NULL WHERE name = %s', (self.name))
        db.conn.commit()

    def get_latest_wrong(self, db):
        db.execute('SELECT question_id FROM user_answers WHERE user_id = %s AND correct=0 ORDER BY updated DESC LIMIT 10', (self.id))
        incorrectIds = db.cur.fetchall()
        return [UserAnswer(self, incorrectId['question_id'], 0) for incorrectId in incorrectIds]
    
    def to_dict(self):
        return { 'id': self.id, 'name': self.name, 'session': self.session }