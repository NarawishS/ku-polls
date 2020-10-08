"""Models contain class of apps."""
from django.db import models
from django.utils import timezone


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

    def total_votes(self):
        sum = 0
        for i in range(self.choice_set.count()):
            sum += self.choice_set.get(pk=1 + i).votes
        return sum

    def reset_votes(self):
        for i in range(self.choice_set.count()):
            choice = self.choice_set.get(pk=1 + i)
            choice.votes = 0
            choice.save()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
