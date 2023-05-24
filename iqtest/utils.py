import random

from iqtest.models import Test


class Question:
    tests = []
    correct = 0

    @staticmethod
    def set_tests(q):
        Question.correct = 0
        Question.tests = q.copy()

    @staticmethod
    def get_tests():
        return Question.tests

    @staticmethod
    def get():
        test = Question.tests.pop()
        lst = [test['correct'], test['answer1'], test['answer2'], test['answer3'], test['answer4'], test['answer5']]
        random.shuffle(lst)
        title = test['question']
        variant = {'a': lst[0], 'b': lst[1], 'c': lst[2], 'd': lst[3], 'e': lst[4], 'f': lst[5]}
        return {"title": title, 'id': test['id'], "variant": variant}

    @staticmethod
    def check(id, answer):
        t = Test.objects.get(pk=id)
        r = t.correct == answer
        if r:
            Question.correct += 1
        return r

    @staticmethod
    def get_correct(id):
        t = Test.objects.get(pk=id)
        return t.correct

    @staticmethod
    def get_total():
        return len(Question.tests)

    @staticmethod
    def get_score():
        return Question.correct