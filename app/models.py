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
