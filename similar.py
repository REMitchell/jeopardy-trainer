import pymysql
from pymysql.err import InternalError
import json

class SimilarQuestions:
    def __init__(self, user, jeopardyDB):
        self.user = user
        self.jeopardyDB = jeopardyDB
        self.question_ids = []

    def get_latest_wrong(self):
        answers = self.user.get_latest_wrong(self.jeopardyDB)
        return self.get_most_similar(answers)

    def get_most_similar(self, answers):
        self.question_ids = [answer.question_id for answer in answers]
        self.jeopardyDB.execute('SELECT app_ngrams.id, COUNT(app_ngrams.id) as count, app_ngrams.value, app_ngrams.instances '\
            'FROM app_ngrams JOIN app_question_ngrams ON app_ngrams.id = app_question_ngrams.ngram_id WHERE app_ngrams.properNoun = 1'\
            ' AND app_question_ngrams.question_id IN %s GROUP BY app_ngrams.id ORDER BY count DESC', (tuple(self.question_ids),))
        
        return self.get_best_question_for_nouns(self.jeopardyDB.cur.fetchall())
        
    def get_best_question_for_nouns(self, proper_nouns):
        if not len(proper_nouns):
            return self.random()
        
        #most_popular = self.most_popular_noun(proper_nouns)
        #if most_popular:
        #    return self.random_by_ngram(most_popular)
        
        common_and_long = self.common_and_long(proper_nouns)
        return self.random_by_ngram(common_and_long)

    def most_popular_noun(self, proper_nouns):
        if proper_nouns[0]['count'] > 1 and proper_nouns[0]['instances'] > 10:
            return proper_nouns[0]
    
    def common_and_long(self, proper_nouns):
        longest = sorted(proper_nouns, key=lambda k: len(k['value']), reverse=True)
        commonest = sorted(proper_nouns, key=lambda k: k['instances'], reverse=True)
        for i in range(0, len(proper_nouns)):
            if self.find(commonest[:i+1], longest[i]['id']):
                return longest[i]
    
    # Stupid utility function because Python
    def find(self, noun_list, noun_id):
        for noun in noun_list:
            if noun['id'] == noun_id:
                return noun

    def random_by_ngram(self, ngram):
        print("NGRAM IS: "+json.dumps(ngram))
        self.jeopardyDB.execute('SELECT * FROM app_question_ngrams WHERE ngram_id = %s AND question_id NOT IN %s ORDER BY RAND() LIMIT 1', (ngram['id'], tuple(self.question_ids),))
        question_ngram = self.jeopardyDB.cur.fetchall()[0]
        self.jeopardyDB.execute('SELECT questions.*, categories.name as category FROM questions JOIN categories ON questions.categoryId = categories.id WHERE questions.id = %s', (question_ngram['question_id']))
        return json.dumps(self.jeopardyDB.cur.fetchall()[0])
    
    def random(self):
        self.jeopardyDB.execute('SELECT questions.*, categories.name as category FROM questions JOIN categories ON questions.categoryId = categories.id ORDER BY RAND() LIMIT 1')
        return json.dumps(self.jeopardyDB.cur.fetchall()[0])
    

