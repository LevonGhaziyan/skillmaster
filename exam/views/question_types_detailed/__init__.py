from .short_answer import ShortAnswer
from .multiple_choice import MultipleChoice
import json

from django.http import Http404

class QuestionTypeDetailedDeterminer:
    def __init__(self, question_property, question_type):
        self.question_property = question_property
        self.question_type = question_type

    def __call__(self):
        self._define()
        print(self.result)

        return json.dumps(self.result)

    def _define(self):
        match self.question_type:
            case "short_answer":
                short_answer = ShortAnswer(self.question_property)
                self.result = short_answer()

            case "multiple_choice":
                multiple_choice = MultipleChoice(self.question_property)
                self.result = multiple_choice()

            case _:
                raise Http404("Question type is wrong!!")