from django.db import models
from .test import TestModel
from .exam_simple_user import ExamSimpleUser

class TestToUser(models.Model):
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    user = models.ForeignKey(ExamSimpleUser, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test} - {self.user.user.username}"