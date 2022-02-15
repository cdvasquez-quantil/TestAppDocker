from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_whith_future_questions(self):
        """ Was published recently return False for questions whose pub_date is in the future."""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="¿Pregunta para el futuro?", pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)


def create_question(question_text, days):
    """ Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published

    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):

    def test_no_questions(self):
        """ If no questions exist, an appropriate message is displayed. """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuentas disponibles.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="¿Pregunta para el futuro?", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No hay encuentas disponibles.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="¿Pregunta para el pasado?", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: ¿Pregunta para el pasado?>"]
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="¿Pregunta para el pasado?", days=-30)
        create_question(question_text="¿Pregunta para el futuro?", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: ¿Pregunta para el pasado?>"]
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="¿Pregunta para el pasado?", days=-30)
        create_question(question_text="¿Pregunta para el pasado?", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: ¿Pregunta para el pasado?>", "<Question: ¿Pregunta para el pasado?>"]
        )

class QuetionDetailViewTestCase(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="¿Pregunta para el futuro?", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the pass
        returns a 404 not found.
        """
        pass_question = create_question(question_text="¿Pregunta para el futuro?", days=-30)
        url = reverse("polls:detail", args=(pass_question.id,))
        response = self.client.get(url)
        self.assertContains(response, pass_question.question_text) 