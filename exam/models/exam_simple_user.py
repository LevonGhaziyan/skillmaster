from django.db import models
from django.contrib.auth.models import User


class ExamSimpleUser(models.Model):
    LEVELS = [
        (0, 'Default'),
        (1, 'SimpleTest')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    take_test_permission_level = models.IntegerField(default=0, choices=LEVELS)
    some = models.IntegerField(default=45)

    def __str__(self):
        return self.user.username