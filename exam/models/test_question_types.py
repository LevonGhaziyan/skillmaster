from django.db import models
from .json_default import json_default

class TestQuestionTypesModel(models.Model):
    question_type_name = models.CharField(max_length=20)
    # question_type_structure = models.JSONField("QuestionTypeStructure", default=json_default)

    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_type_name