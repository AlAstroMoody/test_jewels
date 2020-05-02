from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import UploadModel, DealModel
from .serializers import UploadSerializer, DealSerializer


class UploadView(generics.CreateAPIView):
    queryset = UploadModel.objects.all()
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            filename = serializer.data['deals']
            DealModel.objects.all().delete()
            try:
                DealModel.load_to_database(filename)
                return Response({'Status': 'OK'})
            # как правильно обработать возможные исключения?
            except Exception:
                return Response({'Status': f'Error, Desc: file processing error'})


class DealView(generics.ListAPIView):
    serializer_class = DealSerializer
    queryset = DealModel.objects.all()[:5]

    def get(self, *args):
        data = DealModel.sample()
        if DealModel.objects.all():
            return Response({'response': data})
        else:
            return Response({'Status': f'Error, Desc: Ошибонька'})
