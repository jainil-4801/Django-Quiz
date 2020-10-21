from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from .forms import RegisterForm, LoginForm
from django.shortcuts import redirect

User = get_user_model()

class RegisterAPI(generics.GenericAPIView):
	serializer_class = RegisterSerializer
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'accounts/register.html'
	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		return redirect("login")

	def get(self,request):
		form = RegisterForm()
		return Response({
			'form':form
		})

class LoginAPI(generics.GenericAPIView):
	serializer_class = LoginSerializer
	queryset = User.objects.all()
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'accounts/login.html'
	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		login(request,user)
		return redirect('Quizzes')
	def get(self,request):
		form = LoginForm()
		return Response({
			'form':form
		})



class UserAPI(generics.RetrieveAPIView):
	permission_classes = [
		permissions.IsAuthenticated
	]
	serializer_class = UserSerializer

	def get_object(self):
		user = self.request.user
		return user

@api_view(('POST',))
def LogoutAPI(request):
	name = request.user.first_name 
	logout(request)

	return Response({
            "message":"Thank you for giving your precious time. See you soon next time!!",
            "name": name
            }
        ) 
