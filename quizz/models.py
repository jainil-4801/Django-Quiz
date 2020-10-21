from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Quiz(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=70)
    duration = models.IntegerField()
    time_start = models.DateTimeField(auto_now_add=False)
    time_end = models.DateTimeField(auto_now_add=False)

    class Meta:
        ordering = ['time_start', ]
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    options = models.BooleanField(null=True, blank=True, default=True)
    label = models.CharField(max_length=1000)
    order = models.IntegerField(default=0)
    image = models.ImageField(
        null=True,
        blank=True,
        default='',
        upload_to="quiz/images")

    def __str__(self):
        return self.label

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class QuizTaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class UsersAnswer(models.Model):
    no = models.IntegerField(null=True, blank=True)
    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    text_ans = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.question.label
