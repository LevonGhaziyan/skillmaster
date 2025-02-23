from django.contrib import admin

# Register your models here.
from .models import ExamSimpleUser, TestModel, TestQuestionsListModel, TestQuestionsModel, TestQuestionTypesModel, TestQuestionAnswersModel, TestToUser

class TestQuestionsModelAdmin(admin.ModelAdmin):
    list_display = ("question", "question_type", "question_info")

admin.site.register(ExamSimpleUser)
admin.site.register(TestModel)
admin.site.register(TestQuestionsModel, TestQuestionsModelAdmin)
admin.site.register(TestQuestionsListModel)
admin.site.register(TestQuestionTypesModel)
admin.site.register(TestQuestionAnswersModel)
admin.site.register(TestToUser)