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

class OfficeSerializer(ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = '__all__'

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class ShiftSerializer(ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

