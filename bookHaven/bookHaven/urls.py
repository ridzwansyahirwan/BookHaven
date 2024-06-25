from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),  #http://127.0.0.1:8000/admin
    path('', RedirectView.as_view(url='/books/', permanent=True)), #redirect root ip to #http://127.0.0.1:8000/books
    path('books/', include('myapp.urls')), #access booklist and bookdetaisl on myapp
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]
