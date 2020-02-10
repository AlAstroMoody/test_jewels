from rest_framework import serializers

from app.models import UploadModel, ResultModel


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadModel
        fields = ['deals']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultModel
        fields = ('username', 'spent_money', 'gems')
