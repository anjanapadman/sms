from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Login(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student =models.BooleanField(default=False)
class teacherreg(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='teacher')
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contact_no = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Student(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='student')
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    grade=models.IntegerField()
    email= models.EmailField(max_length=254)
    contact_no =models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Attendance(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='attendance')
    attendance=models.CharField(max_length=100)
    date=models.DateField()
    time = models.TimeField()
class TimeTable(models.Model):
    subject = models.CharField(max_length=100)
    time=models.TimeField()
    date=models.DateField()
    Class=models.IntegerField()
class Notification(models.Model):
    subject = models.CharField(max_length=100)
    description= models.CharField(max_length=300)
    date=models.DateField()
class Feedback(models.Model):
    name =models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    date = models.DateField()
    reply=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name