from django.db import models

from .exam_simple_user import ExamSimpleUser

class TestModel(models.Model):
    test_name = models.CharField(max_length=20)
    owner = models.ForeignKey(ExamSimpleUser, on_delete=models.CASCADE)
    duration = models.IntegerField()
    deadline = models.DateTimeField()
     
    last_update = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name