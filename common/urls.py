from django.urls import path
from . import views

urlpatterns = [
    path('user/comments/', views.UserCommentsView.as_view()),
]
