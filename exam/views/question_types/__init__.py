from .short_answer import ShortAnswer
from .multiple_choice import MultipleChoice
import json

from django.http import Http404

class QuestionTypeDeterminer:
    def __init__(self, answers, question_type):
        self.answers = answers
        self.question_type = question_type

    def __call__(self):
        self._define()

        return json.dumps(self.result)

    def _define(self):
        match self.question_type:
            case "short_answer":
                short_answer = ShortAnswer(self.answers)
                self.result = short_answer()

            case "multiple_choice":
                multiple_choice = MultipleChoice(self.answers)
                self.result = multiple_choice()

            case _:
                raise Http404("Question type is wrong!!")