from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from app.models import UploadModel, ResultModel, DealModel
from app.serializers import UploadSerializer, ResultSerializer


class UploadView(generics.CreateAPIView):
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, )
    queryset = UploadModel.objects.all()

    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            csv_name = str(serializer.data.__getitem__('deals'))
            DealModel.objects.all().delete()
            try:
                DealModel.import_to_base(csv_name)
            except:
                return Response('Неверный формат файла',
                                status=status.HTTP_400_BAD_REQUEST)
            return Response('Успешная проверка', status=status.HTTP_201_CREATED)


class ResultView(generics.ListAPIView):
    serializer_class = ResultSerializer
    queryset = ResultModel.objects.all()[:5]

    def get(self, *args):
        queryset = self.get_queryset()
        serializer = ResultSerializer(queryset, many=True)
        ResultModel.objects.all().delete()
        ResultModel.make_all()
        ResultModel.give_gems()
        if ResultModel.objects.all():
            return Response(serializer.data)
        else:
            return Response('Не удаётся обработать последний загруженный файл',
                            status=status.HTTP_400_BAD_REQUEST)
