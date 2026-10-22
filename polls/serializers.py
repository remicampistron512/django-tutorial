from django.db import transaction
from rest_framework.serializers import IntegerField, ModelSerializer, Serializer, ValidationError

from polls.models import Question, Choice


class VoteSerializer(Serializer):
    choice_id = IntegerField(min_value=1)


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']
        read_only_fields = ['votes']

class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(
        source='choice_set',
        many=True,
        required=False,
    )
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date','user','choices']
        read_only_fields = ['user']

    def validate_choices(self, value):
        if self.instance is not None:
            raise ValidationError('Choices can only be supplied when creating a question.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        choices_data = validated_data.pop('choice_set', [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question
