from django.shortcuts import render
from django.http import JsonResponse
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


def generate(template_name, output_name, render_vars):
    env = Environment(trim_blocks=True, lstrip_blocks=True, loader=PackageLoader("app", "generator/templates"))
    template = env.get_template(template_name)
    rendered = template.render(render_vars)
    print(rendered)
    #i pisemo u fajl
    file_name = os.path.join(root, "templates/output", output_name)
    print(file_name)
    with open(file_name, "w+") as f:
        f.write(rendered)


def gen(request):
    debug=False
    # TODO: smanjiti da bude samo jedan model i jedan generator koji ce dobijati parametre na osnovu kojih ce raditi mesto hardcodovanja
    model = execute(os.path.join(root, "generator"), 'quiz.tx', 'example.quiz', debug, debug)
    modelsurvey1 = execute(os.path.join(root, "generator"), 'quiz.tx', 'example1.survey', debug, debug)
    modelsurvey = execute(os.path.join(root, "generator"), 'quiz.tx', 'example2.survey', debug, debug)
    generate("test_template.html", "survey.html", {"page": model})
    generate("survey_template.html", "survey.html", {"page": modelsurvey})
    generate("survey_template.html", "survey1.html", {"page": modelsurvey1})
    # TODO: promeniti tako da ne dira base vec samo da modifikuje likove za ponudjene quiz i survey
    generate("home_template.html", "index.html", {"page": model})

    return render(request, 'quizgen/home.html', {'data':'Success!', 'model':model, 'modelsurvey':modelsurvey})


def quizzes(request):
    #new_quiz = GrammarExample(title="Quiz1", type="Q", file_path="")
    #new_quiz.save()
    quizzes = GrammarExample.objects.filter(type="Q").all()

    return render(request, 'quiz/quiz.html', {'quizzes': quizzes})


def surveys(request):
    surveys = GrammarExample.objects.filter(type="S").all()

    return render(request, 'survey/survey.html', {'surveys': surveys})


def new_quiz(request):
    title = request.REQUEST['title']
    content = request.REQUEST['content']

    try:
        model = execute_on_request(os.path.join(root, "generator"), 'quiz.tx', content)
    except:
        return JsonResponse({'status': False}, safe=False)

    file_path = create_and_get_file_path(title, content, "q")
    new_quiz = GrammarExample(title=title, type="Q", file_path=file_path)
    new_quiz.save()

    return JsonResponse({'status': True}, safe=False)


def new_survey(request):
    print('')


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
