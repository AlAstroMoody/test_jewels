from django.urls import path

from jewels.app.views import UploadView, ResultView

urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('result/', ResultView.as_view())
]
