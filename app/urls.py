from django.urls import path

from app.views import *


urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('result/', ResultView.as_view())
]
