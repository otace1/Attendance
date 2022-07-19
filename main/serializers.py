from django.db import models
from rest_framework import serializers
from main.models import OfficeLocation

class OfficeLocationSerializer(serializers.Serializer):
    class Meta:
        model = OfficeLocation
        fields = '__all__'
