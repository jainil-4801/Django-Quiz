from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Answer, Question, Quiz, QuizTaker, UsersAnswer
from .serializers import MyQuizListSerializer, QuizDetailSerializer, QuizListSerializer, QuizResultSerializer, UsersAnswerSerializer, QuizTakerSerializer, QuestionSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from datetime import datetime


class QuizListAPI(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quizz/quiz_list.html'
    serializer_class = MyQuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.exclude(quiztaker__user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        q1 = Quiz.objects.filter(time_start__gt=datetime.now())
        q2 = Quiz.objects.filter(time_end__lt=datetime.now())
        q3 = Quiz.objects.exclude(quiztaker__user=self.request.user).filter(time_start__lte=datetime.now(),time_end__gte=datetime.now())
        s1 = QuizListSerializer(q1, many=True)
        s2 = QuizListSerializer(q2, many=True)
        s3 = QuizListSerializer(q3, many=True)
        return Response({
            'ongoing': s3.data,
            'upcoming' : s1.data,
            'past' : s2.data
            })

class QuestionAPI(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quizz/questions.html'

    def get_object(self,*args,**kwargs):
        qid,quizid = self.kwargs["qid"],self.kwargs["quizid"]
        quiz = get_object_or_404(Quiz, id=quizid)
        obj = get_object_or_404(Question,quiz=quiz,order=qid)
        return obj
    
    def get(self,request,*args, **kwargs):
        qid,quizid = self.kwargs["qid"],self.kwargs["quizid"]
        quiz = get_object_or_404(Quiz, id=quizid)
        obj = get_object_or_404(Question,quiz=quiz,order=qid)
        serializer = QuestionSerializer(instance=obj)
        quiztaker = QuizTaker.objects.filter(user=self.request.user,quiz=quiz)
        data = serializer.data 
        mcqs = []
        ids = []
        img = data['image']
        for i in range(len(data['answer_set'])):
            mcqs.append((data['answer_set'][i]['label'],data['answer_set'][i]['id']))
        return Response({
            'mcqs' : mcqs,
            'id' : obj.id,
            'qno' : qid,
            'quiztaker' : quiztaker[0].id,
            'label' : data['label'],
            'img' : img,
            'options' : serializer.data['options'],
        })

    def post(self, request, *args, **kwargs):
        qid,quizid = self.kwargs["qid"],self.kwargs["quizid"]
        quiztaker_id = request.data['quiztaker']
        question_id = request.data['question']
        answer_id = request.data['answer']
        text_answer = request.data['text-ans']
        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)

        if quiztaker.completed:
            return Response({
                "message": "This quiz is already complete. you can't answer any more questions"},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        question = get_object_or_404(Question, id=question_id)
        obj = get_object_or_404(UsersAnswer,quiz_taker=quiztaker,question=question)
        if answer_id != '-1':
            answer = get_object_or_404(Answer, id=answer_id)
            obj.answer = answer
            obj.save()
        else:
            obj.text_ans = text_answer
            obj.save()
        total_Q = Question.objects.filter(quiz=quizid).count()
        if total_Q == qid:
            return redirect("Submit",id=quizid)
        return redirect("Question",qid=qid+1,quizid=quizid)


        



class QuizDetailAPI(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quizz/quiz_register.html'

    def get(self, *args, **kwargs):
        id = self.kwargs["id"]
        quiz = get_object_or_404(Quiz, id=id)
        obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
        if created:
            no = 1
            for question in Question.objects.filter(quiz=quiz):
                UsersAnswer.objects.create(
                    no=no, quiz_taker=obj, question=question)
                no += 1
        dt = quiz.time_end
        year, month, day, hour, minute, second = dt.year,dt.month,dt.day,dt.hour+5,dt.minute,dt.second 
        if minute+30>=60:
            minute -= 30 
            hour += 1
        return Response({'quiz': self.get_serializer(
            quiz, context={'request': self.request}).data,
            'message':"You have successfully registered for the Quiz, Go ahead by clicking the start button to attempt the Quiz.",
            'year':year,'month':month,'day':day,'hour':hour,'minute':minute,'second':second,
            })
    
    



class MyQuizListAPI(generics.ListAPIView):
    permissions_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = QuizTakerSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quizz/my_quiz_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = QuizTaker.objects.filter(user=self.request.user)
        return queryset
    
    def get(self,request,*args,**kwargs):
        queryset = QuizTaker.objects.filter(user=self.request.user)
        serializer = QuizTakerSerializer(queryset, many=True)
        qu = []
        for i in range(len(serializer.data)):
            qu.append(get_object_or_404(Quiz,id=list(serializer.data)[i]['quiz']).name)
            serializer.data[i]['name']=qu[i] 
        
        return Response({'serializer': serializer.data,'qu':qu})


class SubmitQuizAPI(generics.GenericAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'quizz/submit.html'
    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(id=self.kwargs['id'])
        quiztaker = get_object_or_404(QuizTaker, user=request.user, quiz=quiz)
        if quiztaker.completed:
            return Response({
                "message": "This quiz is already completed. You can't submit again"},
                status=status.HTTP_412_PRECONDITION_FAILED
            )
        quiztaker.completed = True
        correct_answers = 0
        u_answers = []
        for users_answer in UsersAnswer.objects.filter(quiz_taker=quiztaker):
            answer = Answer.objects.get(question=users_answer.question, is_correct=True)
            d = dict()
            que = Question.objects.filter(order=users_answer.no,quiz=quiz)
            d['question']  = que[0].label
            d['correct'] = False 
            if que[0].options:
                d['answer'] =  users_answer.answer
                d['act_answer'] = answer.label  
                if users_answer.answer == answer:
                    correct_answers += 1
                    d['correct'] = True 
            else:
                d['answer'] = users_answer.text_ans
                d['act_answer'] = answer.label  
                if users_answer.text_ans == answer.label:
                    correct_answers += 1
                    d['correct'] = True 
            u_answers.append(d)

        quiztaker.score = int(
            correct_answers /
            quiztaker.quiz.question_set.count() *
            100)
        quiztaker.save()
        # UsersAnswer.objects.all().delete()
        return Response({
            "message": "Congratulations!!! You have successfully completed your Quiz...",
            "Total_Marks": quiztaker.score,
            'answers' : u_answers
        }
        )
