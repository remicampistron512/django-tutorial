from django.db import transaction
from rest_framework.serializers import IntegerField, ModelSerializer, Serializer, ValidationError

from polls.models import Question, Choice


class VoteSerializer(Serializer):
    # Identifiant du choix auquel ajouter un vote.
    choice_id = IntegerField(min_value=1)


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']
        read_only_fields = ['votes']


class QuestionSerializer(ModelSerializer):
    # Lie le champ API « choices » aux choix associés à la question.
    choices = ChoiceSerializer(
        source='choice_set',
        many=True,
        required=False,
    )

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'user', 'choices']
        read_only_fields = ['user']

    def validate_choices(self, value):
        # Les choix sont acceptés uniquement lors de la création.
        if self.instance is not None:
            raise ValidationError('Choices can only be supplied when creating a question.')
        return value

    # En cas d'erreur, annule la création de la question et de ses choix.
    @transaction.atomic
    def create(self, validated_data):
        # Sépare les choix des données de la question.
        choices_data = validated_data.pop('choice_set', [])
        # ** transmet les champs validés comme arguments nommés.
        # **validated_data permet de "deballer" le dictionnaire
        question = Question.objects.create(**validated_data)
        # Crée chaque choix en le reliant à la nouvelle question.
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question
