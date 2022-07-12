from django.db import models
from django.urls import reverse

# Create your models here.
class Role(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    role = models.CharField(max_length=32)

    def __str__(self):
        return self.role

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.id})

    def natural_key(self):
        return self.my_natural_key


class LeaveTypes(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    leave_type = models.CharField(max_length=32)

class OfficeLocation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    location = models.CharField(max_length=32, blank=True)
    timezone = models.CharField(max_length=32, blank=True)
    geofences = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.location

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.id})

    def natural_key(self):
        return self.my_natural_key


class Shift(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    shift = models.CharField(max_length=32)
    in_shift = models.DateTimeField()
    out_shift = models.DateTimeField()

    def __str__(self):
        return self.shift

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.id})

    def natural_key(self):
        return self.my_natural_key

def user_directory_path(instance,filename):
    return 'dataset/attendance/1/{0}/'.format(filename)

class User(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    firstname = models.CharField(max_length=32, blank=True)
    lastname = models.CharField(max_length=32, blank=True)
    surname = models.CharField(max_length=32, blank=True)
    job = models.CharField(max_length=32, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    office = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, null=True)
    facedata = models.ImageField(null=True, blank=True, upload_to='dataset/attendance/1/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstname+" "+self.lastname

    def get_absolute_url(self):
        return reverse('update', kwargs={'pk': self.id})

    def natural_key(self):
        return self.my_natural_key

class Attendance(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    worker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    in_dateTime = models.DateTimeField(auto_now_add=True)
    out_dateTime = models.DateTimeField(null=True)
    in_location = models.CharField(max_length=255,blank=True)
    out_location = models.CharField(max_length=255,blank=True)

    #Test
    attendanceDate = models.DateField(null=True)
    work_hours = models.CharField(blank=True, max_length=32, null=True)
    lateTime = models.CharField(blank=True, max_length=32, null=True)
    overTime = models.CharField(blank=True, max_length=32, null=True)


class Leave(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    leave_start = models.DateField()
    leave_end = models.DateField()
    leave_type = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE)

class OnLeave(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, on_delete=models.CASCADE)



