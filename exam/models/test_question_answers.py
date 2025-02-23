from django.db import models

from . import ExamSimpleUser, TestQuestionsModel
from .json_default import json_default


class TestQuestionAnswersModel(models.Model):
    user = models.ForeignKey(ExamSimpleUser, on_delete=models.CASCADE)
    question = models.ForeignKey(TestQuestionsModel, on_delete=models.CASCADE)
    answer = models.JSONField("QuestionAnswer", default=json_default)

    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.question} - {self.answer}"