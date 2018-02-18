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
        html = generate("test_template.html", {"quiz": model, "quiz_id": quiz_id})

        return HttpResponse(html)

    return redirect('/quiz')


def surveys(request):
    surveys = GrammarExample.objects.filter(type="S").all()

    return render(request, 'survey/survey.html', {'surveys': surveys})


def survey(request, survey_id):
    survey = GrammarExample.objects.filter(pk=survey_id).first()

    if survey is not None:
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/surveys/" + survey.title + ".survey"), False, False)
        html = generate("survey_template.html", {"page": model})

        return HttpResponse(html)

    return redirect('/survey')


def new_quiz(request):
    title = request.POST['title']
    content = request.POST['content']

    try:
        model = execute_on_request(os.path.join(root, "generator"), 'quiz.tx', content)
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': False, 'message': 'Nije ispostovana gramatika!'}, safe=False)

    success, file_path = create_and_get_file_path(title, content, "q")

    if not success:
        return JsonResponse({'status': False, 'message': 'Ime kviza vec postoji!'}, safe=False)

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

    success, file_path = create_and_get_file_path(title, content, "s")

    if not success:
        return JsonResponse({'status': False, 'message': 'Ime ankete vec postoji!'}, safe=False)

    new_survey = GrammarExample(title=title, type="S", file_path=file_path)
    new_survey.save()

    return JsonResponse({'status': True}, safe=False)


def submit_quiz(request):
    quiz_id = request.POST['quiz_id']
    quiz = GrammarExample.objects.filter(pk=quiz_id).first()

    if quiz is not None:
        num_of_correct = 0
        num_of_incorrect = 0

        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/quizzes/" + quiz.title + ".quiz"), False, False)

        for question in model.type.questions:
            if question.multipleAnswers == 'one answer':
                correct_answer = get_correct_answer(question.answers)[0]
                if request.POST[question.question.text] == correct_answer:
                    num_of_correct += 1
                    print("Tacno")
                else:
                    num_of_incorrect += 1
                    print("Nije")
            elif question.multipleAnswers == 'ordered':
                order_correct = True
                correct_order = get_correct_order(question.answers)
                for i in range(len(correct_order)):
                    if request.POST[correct_order[i]] != str(i+1):
                        order_correct = False
                        break

                if order_correct:
                    print("TACNO - redosled")
                else:
                    print("Nije - redosled")
            elif question.multipleAnswers == 'matching':
                matched_correct = True
                matched_answers = get_matched_answers(question.answers)
                for i in range(len(matched_answers)):
                    if request.POST[matched_answers[i].value] != str(i+1):
                        matched_correct = False
                        break

                if matched_correct:
                    print('Tacno - spajanje')
                else:
                    print('NIje - spajanje')
            else:
                correct_answers = get_correct_answer(question.answers)
                if request.POST.getlist(question.question.text) == correct_answers:
                    num_of_correct += 1
                    print("TACNOOOO")
                else:
                    num_of_incorrect += 1
                    print("NONO")

    return redirect('/quiz/')


def get_correct_answer(answers):
    return [answer.answer.text for answer in answers if answer.isCorrect == '+']


def get_correct_order(answers):
    return answers[0].answer.sortedAnswers


def get_matched_answers(answers):
    return answers[0].answer.matchedAnswers


def create_and_get_file_path(file_name, file_content, type_of_test):
    file_path = None

    if type_of_test is "q":
        file_path = os.path.join(root, "app_files/quizzes", file_name + ".quiz")
    elif type_of_test is "s":
        file_path = os.path.join(root, "app_files/surveys", file_name + ".survey")

    if file_path is not None:
        if os.path.exists(file_path):
            return False, file_path
        else:
            with open(file_path, "w") as f:
                f.write(file_content)

    return True, file_path


def get_exapmle_from_file(file_path):
    with open(file_path) as f:
        return f.readlines()
