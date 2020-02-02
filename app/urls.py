from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from app.views import *


urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('result/', ResultView.as_view())
]
