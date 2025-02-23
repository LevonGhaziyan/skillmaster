from .tests import TestBase
from .permissions import LoginRequired
from django.http import HttpRequest, HttpResponseRedirect, Http404
from ..models import TestQuestionTypesModel, TestModel, ExamSimpleUser, TestQuestionsModel, TestQuestionsListModel
from .question_types_detailed import QuestionTypeDetailedDeterminer

import json

class AddTestBase(TestBase):
    pass
        
class CreateNewTest(AddTestBase):
    _template = "exam/add_test/create_test.html"

    @property
    def _success_redirect(self):
        return f"/exam/test/create_test/{self.test.id}/select_question_type"

    @property
    def context(self):
        return {}
    
    @LoginRequired()()
    def get(self, request: HttpRequest):
        self.request = request
 
        return self.render_page()
    
    def post(self, request: HttpRequest):
        self.request = request

        self._get_from_POST()

        self._get_user()

        self._create_test()

        return self.success_redirect()
    
    def _get_from_POST(self):
        self.test_name = self.request.POST.get("test_name", "")
        self.deadline = self.request.POST.get("test_deadline", "")
        self.duration = self.request.POST.get("test_duration", "")

    def _get_user(self):
        try:
            self.user = ExamSimpleUser.objects.get(user=self.request.user)
        except:
            raise Http404("User wasn't found!!")

    def _create_test(self):
        try:
            self.test = TestModel(owner=self.user, test_name=self.test_name, duration=self.duration, deadline=self.deadline)
            self.test.save()
        except:
            raise Http404("Something went wrong!!")


class SelectQuestionType(AddTestBase):
    _template = "exam/add_test/select_type.html"

    @property
    def _success_redirect(self):
        return f"/exam/test/create_test/{self.test.id}/create_question?question_type={self.question_type}"

    @property
    def context(self):
        return {
            "test": self.test,
            "question_types": self.question_types,
            }
    
    @LoginRequired()()
    def get(self, request: HttpRequest, test_number):
        self.request = request
        self.test_number = test_number

        self._get_question_types()

        self._get_test()

        return self.render_page()
    
    @LoginRequired()()
    def post(self, request: HttpRequest, test_number):
        self.request = request
        self.test_number = test_number

        self._get_from_POST()

        self._get_test()

        return self.success_redirect()

    def _get_question_types(self):
        self.question_types = TestQuestionTypesModel.objects.all()

    def _get_test(self):
        try:
            self.test = TestModel.objects.get(pk=self.test_number)
        except:
            raise Http404("Test doesn't exist!!")
    
    def _get_from_POST(self):
        self.question_type = self.request.POST.get("question_type", "")

class CreateQuestion(AddTestBase):
    _template = "exam/add_test/create_question.html"

    @property
    def _success_redirect(self):
        return f"/exam/test/create_test/{self.test_number}/select_question_type"

    @property
    def context(self):
        return {
            "template": f"exam/test_details/{self.question_type}.html",
            "test_number": self.test_number,
            "question_type": self.question_type,
            }
    
    def get(self, request: HttpRequest, test_number):
        self.request = request
        self.test_number = test_number

        self._get_from_GET()

        return self.render_page()

    def post(self, request: HttpRequest, test_number):
        self.request = request
        self.test_number = test_number

        self._get_from_GET()

        self._get_from_POST()

        self._get_test()

        self._create_questions_model()

        self._connect_to_test()

        return self.success_redirect()

    def _get_from_GET(self):
        try:
            self.question_type = self.request.GET["question_type"]
        except:
            raise Http404("Something went wrong!!")
    
    def _get_from_POST(self):
        self.question = self.request.POST.get("question", "")
        self.question_property = self.request.POST.get("question_property", "")

    def _get_test(self):
        try:
            self.test = TestModel.objects.get(pk=self.test_number)
        except:
            raise Http404("Something wen wrong!!")
    
    @property
    def question_type_model(self):
        try:
            return TestQuestionTypesModel.objects.get(question_type_name=self.question_type)
        except:
            raise Http404("Something went wrong!!")
    
    def _create_questions_model(self):
        question_type_detailed_determiner = QuestionTypeDetailedDeterminer(self.question_property, self.question_type)
        self.question_info = question_type_detailed_determiner()

        try:
            self.question = TestQuestionsModel(question=self.question, question_type=self.question_type_model, question_info=self.question_info)
            self.question.save()
        except:
            raise Http404("Something went wrong!!")
    
    def _connect_to_test(self):
        self.test_questions = TestQuestionsListModel(test_model=self.test, question_model=self.question)
        self.test_questions.save()

class ReviewTest(AddTestBase):
    _template = "exam/add_test/review_test.html"

    @property
    def _success_redirect(self):
        return f"/exam/test/create_test/{self.test_number}/select_question_type"

    @property
    def context(self):
        return {
            "test_number": self.test_number,
            "questions": self.questions,
            }

    @LoginRequired()()
    def get(self, request: HttpRequest, test_number):
        self.request = request
        self.test_number = test_number

        self._get_test()

        self._get_questions()

        return self.render_page()

    def _get_test(self):
        try:
            self.test = TestModel.objects.get(pk=self.test_number)
        except:
            raise Http404("Something wen wrong!!")

    def _get_questions(self):
        self.questions = TestQuestionsListModel.objects.filter(test_model=self.test)
        print("asdAD", self.questions)