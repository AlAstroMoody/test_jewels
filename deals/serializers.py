from rest_framework import serializers

from .models import UploadModel, DealModel


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadModel
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealModel
        fields = ('username', 'spent_money', 'gems')
