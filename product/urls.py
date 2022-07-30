from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.AllProductView.as_view(), name="all_product"),
    path('paycom/', views.TestView.as_view())
]
