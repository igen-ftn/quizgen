from django.shortcuts import render
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from execute.execute import execute
from root import root
import os

# Create your views here.


def home(request):
    return render(request, 'quizgen/home.html')


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

# TODO: napraviti da u request-u se prosledi koji tmplate (quiz ili survey), verovatno neki naziv path itd
def gen(request):
    debug=False
    #TODO: smanjiti da bude samo jedan model i jedan generator koji ce dobijati parametre na osnovu kojih ce raditi mesto hardcodovanja
    model = execute(os.path.join(root, "generator"), 'quiz.tx', 'example.quiz', debug, debug)
    modelsurvey = execute(os.path.join(root, "generator"), 'quiz.tx', 'example1.survey', debug, debug)

    generate("test_template.html", "quiz.html", {"page": model})
    generate("survey_template.html", "survey.html", {"page": modelsurvey})
    # TODO: promeniti tako da ne dira base vec samo da modifikuje likove za ponudjene quiz i survey
    generate("home_template.html", "index.html", {"page": model})

    return render(request, 'quizgen/home.html', {'data':'Success!', 'model':model, 'modelsurvey':modelsurvey})
