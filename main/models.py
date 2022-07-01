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
    location = models.CharField(max_length=32, blank=True)
    timezone = models.CharField(max_length=32, blank=True)
    geofences = models.CharField(max_length=32, blank=True)

class Shift(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    shift = models.CharField(max_length=32)
    in_shift = models.TimeField()
    out_shift = models.TimeField()

class User(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    firstname = models.CharField(max_length=32, blank=True)
    lastname = models.CharField(max_length=32, blank=True)
    surname = models.CharField(max_length=32, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    office = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)
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



