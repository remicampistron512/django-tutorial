from random import choices

from rest_framework.serializers import ModelSerializer

from polls.models import Question, Choice


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']

class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(
        source='choice_set',
        many=True,
        read_only=True,
    )
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date','user','choices']
        read_only_fields = ['user']
