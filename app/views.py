from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from jewels.app.models import UploadModel, DealsModel, ResultModel
from jewels.app.serializers import UploadSerializer, ResultSerializer


class UploadView(generics.ListCreateAPIView):
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, )
    queryset = UploadModel.objects.all()

    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            csv_name = str(serializer.data.__getitem__('choice'))
            DealsModel.objects.all().delete()
            try:
                DealsModel.import_to_base(csv_name)
            except:
                return Response('Неверный формат файла',
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


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
