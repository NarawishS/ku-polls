from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question, Choice


def create_question(question_text, days):
    """Create a question to be use in test."""
    now = timezone.now()
    end = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=now, end_date=end)


class AuthenticateTests(TestCase):
    """Test authenticate"""

    def setUp(self):
        self.user = User.objects.create_user("Jane", "jane@gmail.com", "12345")
        self.user.first_name = 'Jane'
        self.user.last_name = "Doe"
        self.user.save()
        self.question = create_question("test1", 1)

    def test_user_login(self):
        """Test if the user already login."""
        self.assertTrue(self.client.login(username="Jane", password="12345"))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "Jane")

    def test_user_not_logged_in(self):
        """Test index if no user login."""
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, "Jane")

    def test_login_vote(self):
        """Check authenticate user vote"""
        self.client.login(username="Jane", password="12345")
        response = self.client.get(reverse('polls:vote', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)

    def test_not_login_vote(self):
        """Check if vote redirect to login page if not login"""
        response = self.client.get(reverse('polls:vote', args=(self.question.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/polls/1/vote/')
