"""Views contain web response of this apps."""
import logging

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Vote

log = logging.getLogger("polls")
logging.basicConfig(level=logging.INFO)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def log_user_logged_in(sender, request, user, **kwargs):
    """Log when user login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Login user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_logged_out)
def log_user_logged_out(sender, request, user, **kwargs):
    """Log when user logout."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.info('Logout user: %s , IP: %s , Date: %s', user, ip, str(date))


@receiver(user_login_failed)
def log_user_login_failed(sender, request, credentials, **kwargs):
    """Log when user fail to login."""

    ip = get_client_ip(request)
    date = datetime.now()
    log.warning('Login user(failed): %s , IP: %s , Date: %s', credentials['username'], ip, str(date))


class IndexView(generic.ListView):
    """HttpResponse for Index.

    index page show a list of available question order by published date

    :arg
        template_name(str): urls_pattern
        context_object_name: name of context object
    """

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """HttpResponse for detail of question.

    queryset for the question class contain class that has published
    :arg
        model: class from models
        template_name: urls_pattern
    """

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """HttpsResponse for result.

    :arg
        model: class from models
        template_name: url_pattern
    """

    model = Question
    template_name = 'polls/results.html'


@login_required()
def vote(request, question_id):
    """
    Vote the choice of question id.

    vote the selected choice for the question id,
    if choice is not select you then will be redirect to detail to vote again

    :arg
        request: POST
        question_id: id of the question
    :return
        detail page if choice is invalid
        result if choice is valid
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        Vote.objects.update_or_create(user=user, question=question, defaults={'choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(question=question).filter(choice=choice).count()
            choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    date = datetime.now()
    log.info("User: %s, Poll's ID: %d, Date: %s.", user, question_id, str(date))
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
