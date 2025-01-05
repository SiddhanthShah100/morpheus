from rest_framework import serializers
from .models import Form, Question, Option, Response, Answer

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'options']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'description', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text', 'file_upload', 'image_choice', 'slider_value', 'ranking_value', 'geolocation_value']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.answer_text:
            representation['answer_text'] = instance.answer_text
        elif instance.file_upload:
            representation['file_upload'] = instance.file_upload.url  
        elif instance.image_choice:
            representation['image_choice'] = instance.image_choice.url  
        elif instance.slider_value is not None:
            representation['slider_value'] = instance.slider_value
        elif instance.ranking_value is not None:
            representation['ranking_value'] = instance.ranking_value
        elif instance.geolocation_value:
            representation['geolocation_value'] = instance.geolocation_value

        return representation


class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Response
        fields = ['id', 'form', 'answers']
