import uuid
from django.db import models

# Create your models here.
class Role(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    role = models.CharField(max_length=32)

class LeaveTypes(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    leave_type = models.CharField(max_length=32)

class OfficeLocation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    locationname = models.CharField(max_length=32)

class Setting(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    office = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True)
    start_time = models.TimeField()
    lunch_in = models.TimeField(blank=True)
    lunch_out = models.TimeField(blank=True)
    out_time = models.TimeField()
    timezone = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True)

class User(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    firstname = models.CharField(max_length=32, blank=True)
    lastname = models.CharField(max_length=32, blank=True)
    surname = models.CharField(max_length=32, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    office = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True)
    facedata = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-id']

class Attendance(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()
    work_hours = models.TimeField()
    over_time = models.TimeField()
    late_time = models.TimeField()
    early_out = models.TimeField()
    in_location = models.CharField(max_length=255)
    out_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

class Leave(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    leave_start = models.DateField()
    leave_end = models.DateField()
    leave_type = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE)

class OnLeave(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE)



