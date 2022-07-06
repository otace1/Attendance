from rest_framework.serializers import ModelSerializer
from main.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class LeaveTypesSerializer(ModelSerializer):
    class Meta:
        model = LeaveTypes
        fields = '__all__'


