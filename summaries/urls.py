# summaries/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('summary/<int:pk>/', views.summary_detail_view, name='summary_detail'),
]