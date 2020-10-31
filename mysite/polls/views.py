"""Views contain web response of this apps."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from mysite.polls.models import Choice, Question


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
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
