from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import six
from django.views.decorators.csrf import csrf_exempt
from jinja2.environment import Environment
from jinja2.loaders import PackageLoader
from .execute.execute import execute, execute_on_request
from .root import root
from .models import *
import jinja2
import json
import os
import random

def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq

jinja2.filters.FILTERS['shuffle'] = filter_shuffle

# Create your views here.
def contains(value, list, question):
    print('vrednost' + value)
    print(list)
    if value in list[question]:
        return True
    else:
        return False

def check_order(value, list, index):
    if str(index) == list[value][0]:
        return True
    else:
        return False

def compare(value, index):
    if value == str(index):
        return True
    else:
        return False

def add_filters():
    loader = jinja2.PackageLoader('app', 'generator/templates')
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['contains'] = contains
    jinja2.filters.FILTERS['contains'] = contains
    jinja2.filters.FILTERS['check_order'] = check_order
    jinja2.filters.FILTERS['compare'] = compare

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

def quiz_results(request, quiz_id):
    add_filters()
    quiz = GrammarExample.objects.filter(pk=quiz_id).first()
    answers = request.session['old_post']
    if quiz is not None:
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/quizzes/" + quiz.title + ".quiz"), False, False)
        html = generate("test_results.html", {"quiz": model, "quiz_id": quiz_id, "user_answers":answers})

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
        html = generate("survey_template.html", {"survey": model, "survey_id": survey_id})

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
    # title = "Survey 3"
    # content = get_exapmle_from_file(os.path.join(root, "app_files/surveys/Survey 1.survey"))[0]

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



@csrf_exempt
def submit_quiz(request):
    quiz_id = request.POST['quiz_id']
    quiz = GrammarExample.objects.filter(pk=quiz_id).first()
    request.session['old_post'] = dict(six.iterlists(request.POST))
    print(request.session['old_post'])
    if quiz is not None:
        # statistic params
        num_of_correct = 0

        # ----------------------------
        quiz_statistic = QuizStatistic.objects.filter(pk=quiz_id).first()
        if quiz_statistic is None:
            quiz_statistic = QuizStatistic.objects.create(quiz_id=quiz_id)

        quiz_statistic.taken_test += 1
        quiz_questions = []

        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/quizzes/" + quiz.title + ".quiz"), False, False)

        for question in model.type.questions:
            quiz_question = QuizQuestion.objects.filter(quiz_id=quiz_id, text=question.question.text).first()
            if quiz_question is None:
                quiz_question = QuizQuestion.objects.create(quiz_id=quiz_id, text=question.question.text)

            if question.multipleAnswers == 'one answer':
                correct_answer = get_correct_answer(question.answers)[0]
                if request.POST[question.question.text] == correct_answer:
                    quiz_question.correct_answers += 1
                    num_of_correct += 1
                else:
                    quiz_question.incorrect_answers += 1
            elif question.multipleAnswers == 'ordered':
                order_correct = True
                correct_order = get_correct_order(question.answers)
                for i in range(len(correct_order)):
                    if request.POST[correct_order[i]] != str(i+1):
                        order_correct = False
                        break

                if order_correct:
                    quiz_question.correct_answers += 1
                    num_of_correct += 1
                else:
                    quiz_question.incorrect_answers += 1
            elif question.multipleAnswers == 'matching':
                matched_correct = True
                matched_answers = get_matched_answers(question.answers)
                for i in range(len(matched_answers)):
                    if request.POST[matched_answers[i].value] != str(i+1):
                        matched_correct = False
                        break

                if matched_correct:
                    quiz_question.correct_answers += 1
                    num_of_correct += 1
                else:
                    quiz_question.incorrect_answers += 1
            else:
                correct_answers = get_correct_answer(question.answers)
                if request.POST.getlist(question.question.text) == correct_answers:
                    quiz_question.correct_answers += 1
                    num_of_correct += 1
                else:
                    quiz_question.incorrect_answers += 1

            quiz_question.save()
            quiz_questions.append(quiz_question)

        quiz_statistic.questions.set(quiz_questions)
        quiz_statistic.correct_answers += num_of_correct
        quiz_statistic.save()

    return redirect('quiz_results', quiz_id)


def submit_survey(request):
    survey_id = request.POST['survey_id']
    survey = GrammarExample.objects.filter(pk=survey_id).first()

    if survey is not None:
        # ----------------------------
        model = execute(os.path.join(root, "generator/quiz.tx"),
                        os.path.join(root, "app_files/surveys/" + survey.title + ".survey"), False, False)

        survey_statistic = SurveyStatistic.objects.filter(pk=survey_id).first()
        if survey_statistic is None:
            survey_statistic = create_and_fill_object(model, survey_id)

        survey_statistic.taken_test += 1

        for question in model.type.questions:
            if question.questionType.label == 'multiple choice':
                if question.questionType.answerType == 'one answer':
                    key = request.POST[question.question.text]
                    survey_answer = Answer.objects.filter(survey_id=survey_id, key=key).first()
                    survey_answer.num_of_answers += 1
                    survey_answer.save()
                else:
                    answers = request.POST.getlist(question.question.text)
                    for answer in answers:
                        survey_answer = Answer.objects.filter(survey_id=survey_id, key=answer).first()
                        survey_answer.num_of_answers += 1
                        survey_answer.save()
            elif question.questionType.label == 'Likert':
                for statement in question.questionType.statements:
                    number = request.POST[statement.text]
                    answer = get_answer_by_number(question.questionType.answers, int(number))
                    survey_answer = Answer.objects.filter(survey_id=survey_id, key=statement.text, value=answer).first()
                    survey_answer.num_of_answers += 1
                    survey_answer.save()
            elif question.questionType.label == 'Semantic dif':
                for answer in question.questionType.answers:
                    key = answer.leftSideAnswer + " " + str(answer.leftValue) + " " + answer.rightSideAnswer + " " + str(answer.rightValue)
                    value = request.POST[answer.leftSideAnswer]
                    survey_answer = Answer.objects.filter(survey_id=survey_id, key=key, value=value).first()
                    if survey_answer is None:
                        survey_answer = Answer.objects.create(survey_id=survey_id, key=key, value=value)
                    survey_answer.num_of_answers += 1
                    survey_answer.save()
            elif question.questionType.label == 'Rank order':
                for answer in question.questionType.answers:
                    survey_answer = Answer.objects.filter(survey_id=survey_id, key=answer.text).first()
                    if survey_answer.value == 'empty':
                        survey_answer.value = '0'
                    survey_answer.value = str(int(survey_answer.value) + int(request.POST[answer.text]))
                    survey_answer.num_of_answers += 1
                    survey_answer.save()
            else:
                text = request.POST[question.question.text]
                survey_question_answer = Answer.objects.create(survey_id=survey_id, key=text)
                survey_question = SurveyQuestion.objects.filter(survey_id=survey_id, text=question.question.text).first()
                survey_question.answers.add(survey_question_answer)
                survey_question.save()

    return redirect('/survey/')


def get_answer_by_number(answers, number):
    for answer in answers:
        if answer.number == number:
            return answer.description
    return None


def create_and_fill_object(model, survey_id):
    survey_statistic = SurveyStatistic.objects.create(survey_id=survey_id)

    survey_questions = []

    for question in model.type.questions:
        survey_question = SurveyQuestion.objects.create(survey_id=survey_id, text=question.question.text)
        survey_question_answers = []

        if question.questionType.label == 'multiple choice':
            for answer in question.questionType.answers:
                survey_question_answer = Answer.objects.create(survey_id=survey_id, key=answer.text)
                survey_question_answers.append(survey_question_answer)
        elif question.questionType.label == 'Likert':
            for statement in question.questionType.statements:
                for answer in question.questionType.answers:
                    survey_question_answer = Answer.objects.create(survey_id=survey_id, key=statement.text, value=answer.description)
                    survey_question_answers.append(survey_question_answer)
        elif question.questionType.label == 'Rank order':
            for answer in question.questionType.answers:
                survey_question_answer = Answer.objects.create(survey_id=survey_id, key=answer.text)
                survey_question_answers.append(survey_question_answer)
        else:
            continue

        survey_question.answers.set(survey_question_answers)
        survey_question.save()
        survey_questions.append(survey_question)

    survey_statistic.questions.set(survey_questions)
    survey_statistic.save()

    return survey_statistic


def quiz_statistic(request, quiz_id):
    quiz_statistic = QuizStatistic.objects.filter(quiz_id=quiz_id).first()
    accuracy = int((quiz_statistic.correct_answers / (quiz_statistic.taken_test*len(quiz_statistic.questions.all())))*100)

    return render(request, 'statistic/quiz_statistic.html', {'quiz_statistic': quiz_statistic, 'accuracy': accuracy})


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
