from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from .execute.execute import execute, execute_on_request
from .root import root
from .models import *
import os

# Create your views here.


def home(request):
    return render(request, 'quizgen/home.html')


def new(request):
    return render(request, 'quizgen/grammarInput.html')


def generate(template_name, render_vars):
    env = Environment(trim_blocks=True, lstrip_blocks=True, loader=PackageLoader("app", "generator/templates"))
    template = env.get_template(template_name)
    rendered = template.render(render_vars)

    return rendered


def quizzes(request):
    quizzes = GrammarExample.objects.filter(type="Q").all()

    return render(request, 'quiz/quiz.html', {'quizzes': quizzes})


def quiz(request, quiz_id):
    quiz = GrammarExample.objects.filter(pk=quiz_id).first()

    if quiz is not None:
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/quizzes/" + quiz.title + ".quiz"), False, False)
        #html = generate("test_template.html", {"page": model})

        #return HttpResponse(html)

        return render(request, 'quiz/take-quiz.html', {'quiz': model})

    return redirect('/quiz')



def surveys(request):
    surveys = GrammarExample.objects.filter(type="S").all()

    return render(request, 'survey/survey.html', {'surveys': surveys})


def survey(request, survey_id):
    survey = GrammarExample.objects.filter(pk=survey_id).first()
    if survey is not None:
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/surveys/" + survey.title + ".survey"), False, False)

        return render(request, 'survey/take-survey.html', {'survey': model})

    return redirect('/survey')


def test_survey(request):
    survey = "asdsda"
    if survey is not None:
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "generator/example2.survey"), False, False)

        return render(request, 'survey/take-survey.html', {'survey': model})

    return redirect('/survey')



def new_quiz(request):
    title = request.POST['title']
    content = request.POST['content']

    try:
        model = execute_on_request(os.path.join(root, "generator"), 'quiz.tx', content)
    except Exception as e:
        return JsonResponse({'status': False, 'message': 'Nije ispostovana gramatika!'}, safe=False)

    file_path = create_and_get_file_path(title, content, "q")
    new_quiz = GrammarExample(title=title, type="Q", file_path=file_path)
    new_quiz.save()

    return JsonResponse({'status': True}, safe=False)


def new_survey(request):
    title = request.POST['title']
    content = request.POST['content']

    try:
        model = execute_on_request(os.path.join(root, "generator"), 'quiz.tx', content)
    except Exception as e:
        return JsonResponse({'status': False, 'message': 'Nije ispostovana gramatika!'}, safe=False)

    file_path = create_and_get_file_path(title, content, "s")
    new_survey = GrammarExample(title=title, type="S", file_path=file_path)
    new_survey.save()

    return JsonResponse({'status': True}, safe=False)


def create_and_get_file_path(file_name, file_content, type_of_test):
    file_path = None
    if type_of_test is "q":
        file_path = os.path.join(root, "app_files/quizzes", file_name + ".quiz")
        with open(file_path, "w") as f:
            f.write(file_content)
    elif type_of_test is "s":
        file_path = os.path.join(root, "app_files/surveys", file_name + ".survey")
        with open(file_path, "w") as f:
            f.write(file_content)

    return file_path


def get_exapmle_from_file(file_path):
    with open(file_path) as f:
        return f.readlines()
