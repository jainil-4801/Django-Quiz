from django.conf.urls.static import static
from django.conf import settings 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quizz.urls')),
    path('api/auth/', include('accounts.urls')),
    path('nested_admin', include('nested_admin.urls')),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
