"""Models contain class of apps."""
from django.db import models
from django.contrib.auth.models import User

from mysite.polls.models import Question


class Choice(models.Model):
    """Choice of Question contain text of this choice and total vote for this choice.

    :arg
        question: Question that contain this choice
        choice_test(str): detail of this choice
        votes(int): total vote for this choice
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text
