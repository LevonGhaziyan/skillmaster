from django.http import HttpRequest, HttpResponseRedirect, Http404

from .view_base import ViewBase

from ..models import TestModel, TestQuestionsListModel, ExamSimpleUser, TestQuestionAnswersModel, TestToUser

from .permissions import LoginRequired, PermissionRequired

from .question_types import QuestionTypeDeterminer

import json

def view_test_redirect(request, test_number, *args, **kwargs):
    return HttpResponseRedirect(f"/exam/test/{test_number}/1")

class TestBase(ViewBase):
    pass

class Test(TestBase):
    _template = "exam/test.html"

    @property
    def _success_redirect(self):
        if self.question_number != len(self.questions_list):
            return f"/exam/test/{self.test_number}/{self.question_number + 1}/"
        
        return "/exam/"
    
    @property
    def context(self):
        context =  {
            "test": self.test_model,
            "question": self.question,
            "question_number": self.question_number,
            "template": f"exam/tests/{self.question.question_type}.html",
            }
        
        try:
            answer = TestQuestionAnswersModel.objects.get(user=self.user, question=self.question)
        except:
            pass
        else:
            context["answer"] = json.loads(answer.answer)

        return context

    @LoginRequired()()
    @PermissionRequired()()
    def get(self, request: HttpRequest, test_number, question_number):
        self.request = request
        self.test_number = test_number
        self.question_number = question_number

        self._get_test_model()

        self._get_questions_list()

        self._get_user()

        self._get_question()

        return self.render_page()

    @LoginRequired()()
    @PermissionRequired()()
    def post(self, request: HttpRequest, test_number, question_number):
        self.request = request
        self.test_number = test_number
        self.question_number = question_number

        self._get_test_model()

        self._get_questions_list()

        self._get_question()

        self._get_user()

        self._get_from_POST()

        self._save_answer()

        self._check_test_completeness()

        return self.success_redirect()

    
    def _get_test_model(self):
        try:
            self.test_model = TestModel.objects.get(pk=self.test_number)
        except:
            raise Http404("Test wasn't found!!")
    
    def _get_questions_list(self):
        try:
            self.questions_list = TestQuestionsListModel.objects.filter(test_model=self.test_model)
        except:
            raise Http404("There aren't any questions for this test!!")
    
    def _get_question(self):
        self.question = self.questions_list[self.question_number - 1].question_model

    def _get_user(self):
        try:
            self.user = ExamSimpleUser.objects.get(user=self.request.user)
        except:
            raise Http404("User wasn't found!!")

    def _get_from_POST(self):
        self.answers = self.request.POST.dict()

    def _check_answer_existence(self):
        try:
            self.existing_answer = TestQuestionAnswersModel.objects.get(user=self.user, question=self.question)
        except:
            return False
        else:
            return True
        
            
    def _save_answer(self):
        question_determiner = QuestionTypeDeterminer(self.answers, self.question.question_type.question_type_name)
        self.answer = question_determiner()

        try:
            if self._check_answer_existence():
                self.existing_answer.answer = self.answer
                self.existing_answer.save()
            else:
                self.answer_model = TestQuestionAnswersModel(user=self.user, question=self.question, answer=self.answer)
                self.answer_model.save()

        except:
            raise Http404("Something went wrong!!")

    def _check_test_completeness(self):
        for question in self.questions_list:
            try:
                TestQuestionAnswersModel.objects.get(question=question.question_model)
            except:
                self._save_completeness(False)
            else:
                self._save_completeness(True)
    
    def _save_completeness(self, is_completed):
        try:
            test_to_user = TestToUser.objects.get(test=self.test_model)
            test_to_user.is_completed = is_completed
            test_to_user.save()
        except:
            raise Http404("Something went wrong!!")