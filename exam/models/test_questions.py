from django.db import models
from . import TestQuestionTypesModel
from .json_default import json_default

class TestQuestionsModel(models.Model):
    question = models.CharField(max_length=100)
    question_type = models.ForeignKey(TestQuestionTypesModel, on_delete=models.CASCADE)
    question_info = models.JSONField("QuestionInfo", default=json_default)

    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question