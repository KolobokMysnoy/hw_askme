from django.core.paginator import Paginator
from django.shortcuts import render
from app.models import Question, Answer, Tag, Profile, LikeForQuestion, LikeForAnswer


def index(request):
    questions = paginate(Question.objects.new_questions(), request)
    context = {
        "questions": questions,
        "tags": all_tags()}
    return render(request, "index.html", context)


def ask(request):
    context = {"tags": all_tags()}
    return render(request, "ask.html", context)


def login(request):
    context = {"tags": all_tags()}
    return render(request, "login.html", context)


def signup(request):
    context = {"tags": all_tags()}
    return render(request, "signup.html", context)


def question(request, i: int):
    answers = paginate(Answer.objects.to_question(i), request, 5)
    context = {
        "question": Question.objects.single_question(i),
        "answers": answers,
        "tags": all_tags()
    }
    return render(request, "question.html", context)


def hot_list(request):
    questions = paginate(Question.objects.hot_questions(), request)
    context = {
        "questions": questions,
        "tags": all_tags()}
    return render(request, "hot_list.html", context)


def with_tag(request, tag: str):
    questions = paginate(Question.objects.with_tag(tag), request)
    context = {
        "tag": tag,
        "questions": questions,
        "tags": all_tags()}
    return render(request, "with_tag.html", context)


def all_tags():
    return Tag.objects.all()[:10]


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects_on_page = paginator.get_page(page)
    return objects_on_page

