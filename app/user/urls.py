from django.urls import path

from user import views

# app name for reverse mapping
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
