from django.urls import path, re_path
from .api import QuizListAPI, QuizDetailAPI, SubmitQuizAPI, MyQuizListAPI, QuestionAPI

 
urlpatterns = [
	path("my-quizzes/",MyQuizListAPI.as_view(),name="MyQuizzes"),
	path("quizzes/", QuizListAPI.as_view(),name="Quizzes"),
	path("quizzes/<int:quizid>/<int:qid>",QuestionAPI.as_view(),name="Question"),
    path("quizzes/<int:id>",QuizDetailAPI.as_view(),name="Quiz"),
    path("quizzes/<int:id>/submit",SubmitQuizAPI.as_view(),name="Submit"),
]