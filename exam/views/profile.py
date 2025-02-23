from django.http import Http404, HttpRequest

from ..models import ExamSimpleUser, TestToUser, TestModel
from .view_base import ViewBase
from .permissions import LoginRequired


class UserProfile(ViewBase):
    _template = "exam/user_profile.html"
        
    @property
    def context(self):
        return {
            "tests": self.completed_tests,
            "own_tests": self.own_tests,
        }

    @LoginRequired()()
    def get(self, request: HttpRequest, username):
        self.request = request
        self.username = username

        self._validate_user()

        self._get_exam_simple_user()

        self._get_completed_tests()

        self._get_own_tests()

        return self.render_page()
    
    def _validate_user(self):
        if self.username != self.request.user.username:
            raise Http404("You don't have permission for this action!!")
    
    def _get_exam_simple_user(self):
        try:
            self.exam_simple_user = ExamSimpleUser.objects.get(user=self.request.user)
        except:
            raise Http404("User doesn't exist!!")
    
    def _get_test_to_user_list(self):
        self.test_to_user = TestToUser.objects.filter(user=self.exam_simple_user)

    def _get_completed_tests(self):
        self._get_test_to_user_list()

        self.completed_tests = [test.test for test in self.test_to_user if test.is_completed]
    
    def _get_own_tests(self):
        self.own_tests = TestModel.objects.filter(owner=self.exam_simple_user).order_by("-pub_date")