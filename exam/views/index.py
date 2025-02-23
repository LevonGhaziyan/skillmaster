from django.http import HttpRequest, Http404
from django.shortcuts import get_object_or_404


from .permissions import LoginRequired
from ..models import TestModel, ExamSimpleUser, TestToUser
from .view_base import ViewBase


class Index(ViewBase):
    _template = "exam/index.html"

    @property
    def context(self):
        return {
            "tests": self.tests_list,
        }

    @LoginRequired()()
    def get(self, request: HttpRequest):
        self.request = request

        self._get_user()

        self._get_test_to_user_list()

        self._get_tests_list()

        return self.render_page()

    def _get_user(self):
        self.exam_simple_user = get_object_or_404(ExamSimpleUser, user=self.request.user.id)
    
    def _get_test_to_user_list(self):
        self.test_to_user = TestToUser.objects.filter(user=self.exam_simple_user)

    def _get_tests_list(self):
        # self.tests_list = TestModel.objects.filter(permission_level=self._user.take_test_permission_level).order_by("-pub_date")
        self.tests_list = [test.test for test in self.test_to_user if not test.is_completed]
    