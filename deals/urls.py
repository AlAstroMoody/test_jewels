from django.urls import path

from . import views

app_name = 'deals'
urlpatterns = [
    path('upload', views.UploadView.as_view()),
    path('result', views.DealView.as_view()),
]
