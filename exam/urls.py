from django.urls import path

from . import views

app_name = "exam"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("signup/", views.SignUp.as_view(), name="sign_up"),
    path("signup/verify", views.SignUpVerification.as_view(), name="sign_up_verification"),
    path("login/", views.LogIn.as_view(), name="log_in"),
    path("logout/", views.LogOut.as_view(), name="log_out"),
    path("test/create_test/", views.CreateNewTest.as_view(), name="create_test"),
    path("test/create_test/<int:test_number>/select_question_type", views.SelectQuestionType.as_view(), name="select_question_type"),
    path("test/create_test/<int:test_number>/create_question", views.CreateQuestion.as_view(), name="create_question"),
    path("test/create_test/<int:test_number>/review", views.ReviewTest.as_view(), name="review_test"),
    path("test/<int:test_number>/", views.view_test_redirect),
    path("test/<int:test_number>/<int:question_number>/", views.Test.as_view()),
    path("test/save/<int:test_number>/<int:question_number>/", views.Test.as_view()),
    path("user/<str:username>/", views.UserProfile.as_view()),
]