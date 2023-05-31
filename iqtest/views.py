import json

from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from iqtest.models import Test, Result, Ability
from iqtest.utils import Question


def is_login(user):
    return user.is_authenticated


# Create your views here.
def index(request: HttpRequest):
    u = User.objects.count()
    t = Test.objects.count()
    r = Result.objects.count()
    stat = {'user': u, 'test': t, 'result': r}
    return render(request, 'index.html', {'user': request.user, 'stat': stat})


@user_passes_test(is_login, '/login/')
def get_index(request: HttpRequest):
    return render(request, 'index.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
    return render(request, 'login.html')


@user_passes_test(is_login, '/login/')
def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('/')


def reg(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'reg.html')
        try:
            user = User.objects.create_user(username, password=password1)
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
        except:
            return render(request, 'reg.html')
    return render(request, 'reg.html')


def manual(request: HttpRequest):
    return render(request, 'manual.html')


def contact(request: HttpRequest):
    return render(request, 'contact.html')


def about(request: HttpRequest):
    return render(request, 'about.html')


@user_passes_test(is_login, '/login/')
def test(request: HttpRequest):
    return render(request, 'iq/game.html')


@user_passes_test(is_login, '/login/')
def end(request: HttpRequest):
    return render(request, 'iq/end.html')


@user_passes_test(is_login, '/login/')
def get_question(request: HttpRequest):
    p = json.loads(request.body)
    if p.get('start', False):
        test = Test.objects.all()
        tests = []
        for t in test: tests.append(model_to_dict(t))
        Question.set_tests(tests)
        return JsonResponse({'total': Question.get_total(), 'bonus': 1})
    if Question.get_total() == 0:
        score = Question.get_score()
        Result.objects.create(
            user_id=request.user.pk,
            result=68 + score * 2
        )
        ability = Ability.objects.get(id=score+1)
        return JsonResponse({'finish': True, 'username': request.user.username, 'iq': ability.iq, 'ability': ability.ability})
    data = Question.get()
    return JsonResponse(data)


@user_passes_test(is_login, '/login/')
def post_question(request: HttpRequest):
    p = json.loads(request.body)
    q_id: str = p['answer'][-6:-4]
    if q_id.startswith('/'):
        q_id = q_id[-1:]
    reqireds = ['id', 'answer']
    for r in reqireds:
        if r not in p:
            return JsonResponse({'ok': False, 'error': f'{r} required'})
    data = {'answer': 'incorrect'}
    if Question.check(q_id, p['answer']):
        data['answer'] = 'correct'
    data['correct'] = Question.get_correct(q_id)
    return JsonResponse(data)


@user_passes_test(is_login, '/login/')
def stat(request: HttpRequest):
    objs = list(Result.objects.filter(user_id=request.user.pk).all())
    return render(request, 'iq/stat.html', {'data': objs})


@user_passes_test(is_login, '/login/')
def rating(request: HttpRequest):
    objs = list(Result.objects.all())
    objs.sort(key=lambda x: x.result, reverse=True)
    new_objs = []
    for obj in objs:
        users = []
        for i in new_objs:
            users.append(i.user)
        if obj.user not in users:
            new_objs.append(obj)
    objs = new_objs
    lst = list(range(1, len(objs)+1))
    objs = list(zip(lst, objs))
    return render(request, 'iq/rating.html', {'data': objs})