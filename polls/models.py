"""Models contain class of apps."""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Poll Question with detail of published date and end date.

    :arg
        question_text(str): question of poll
        pub_date(DateTimeField): published date of this question
        end_date(DateTimeField): end date of this question
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='date published')
    end_date = models.DateTimeField(verbose_name='closed date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Check if this question has been published for less than a day or not.

        :return
            true: if this question has been published for less than a day
        """
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check if this question has published or not.

        :return
            true: if pub_date has pass
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """Check if this question is open for vote or not.

        :return
            true: if this question is_published and hasn't pass end_date
        """
        return self.pub_date <= timezone.now() <= self.end_date

    can_vote.admin_order_field = 'end_date'
    can_vote.boolean = True
    can_vote.short_description = 'Open?'


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

    def __str__(self):
        return self.choice_text
