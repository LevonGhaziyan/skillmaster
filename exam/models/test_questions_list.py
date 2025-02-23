from django.db import models
from . import TestModel
from . import TestQuestionsModel


class TestQuestionsListModel(models.Model):
    test_model = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    question_model = models.OneToOneField(TestQuestionsModel, on_delete=models.CASCADE)

    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_model} - {self.question_model}"