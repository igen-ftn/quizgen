from django.db import models


class GrammarExample(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70)
    TYPE_CHOICE = (
        ('Q', 'Quiz'),
        ('S', 'Survey')
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICE, default='Q')
    file_path = models.CharField(max_length=200)


class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)


class QuizStatistic(models.Model):
    quiz_id = models.IntegerField(primary_key=True)
    questions = models.ManyToManyField(QuizQuestion)
    taken_test = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)

