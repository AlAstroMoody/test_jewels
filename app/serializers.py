from rest_framework import serializers

from jewels.app.models import UploadModel, ResultModel


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadModel
        fields = ['choice']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultModel
        fields = ['username', 'spent_money', 'gems']
