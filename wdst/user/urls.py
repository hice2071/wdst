from django.urls import path
from user import views

urlpatterns = [
    path('', views.UsersList.as_view(), name='UsersList'),
    path(r'<int:pk>/', views.UsersDetail.as_view(), name='UsersDetail'),
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('demo/', views.demo),
]
