from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='date published')
    end_date = models.DateTimeField(verbose_name='closed date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        return self.pub_date <= timezone.now()

    def can_vote(self):
        return self.pub_date <= timezone.now() <= self.end_date

    can_vote.admin_order_field = 'end_date'
    can_vote.boolean = True
    can_vote.short_description = 'Open?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
