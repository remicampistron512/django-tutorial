import datetime

from django.conf import settings
from django.contrib import admin
from django.db import models, transaction  # type: ignore
from django.utils import timezone  # type: ignore

MAX_LENGTH = 20


def text_excerpt(text, max_length):
    # Tronque les textes trop longs pour l'affichage.
    return text[:max_length] + ('...' if len(text) > max_length
                                else '')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    # Conserve la question si son auteur est supprimé.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="questions",
    )

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id = None
        self.choice_set = None

    @classmethod
    def get_most_popular(cls):
        # Compare les questions selon le total des votes de leurs choix.
        all_questions = cls.objects.all()
        best_answer = (0,0)
        for question in all_questions:
            choices = question.choice_set.all()
            total_votes = 0
            for choice in choices:
               total_votes += choice.votes

            if best_answer[1] < total_votes:
                best_answer = question, total_votes

        return best_answer

    @classmethod
    def get_least_popular(cls):
        # Recherche le plus petit total de votes.
        all_questions = cls.objects.all()
        worst_question = None
        min_votes = None

        for question in all_questions:
            total_votes = sum(choice.votes for choice in question.choice_set.all())

            if min_votes is None or total_votes < min_votes:
                worst_question = question
                min_votes = total_votes

        return worst_question, min_votes







    def __str__(self):
        # Affiche la date et un extrait du texte de la question.
        return "{} {}".format(self.pub_date,
                              text_excerpt(self.question_text,
                                           MAX_LENGTH))


    def get_choices(self):
        # Renvoie le texte, les votes et le pourcentage de chaque choix.
        total = 0
        choices = self.choice_set.all()
        for c in choices:
            total += c.votes
        return [(c.choice_text, c.votes, (c.votes / total * 100) if total > 0 else 0)
                for c in choices]

    def get_max_choice(self):
        total = 0

        # Récupère les choix liés à cette question.
        choices = self.choice_set.all()
        max_choice = choices[0]
        for c in choices:
            total += c.votes
        if c.votes > max_choice.votes:
            max_choice = c
        return (max_choice.choice_text, max_choice.votes / total)

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self):
        # Vérifie si la publication date des dernières 24 heures.
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def age(self):
        # Calcule le temps écoulé depuis la publication.
        return timezone.now() - self.pub_date


class Choice(models.Model):
    # Supprime les choix lorsque leur question est supprimée.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return text_excerpt(self.choice_text, MAX_LENGTH)
