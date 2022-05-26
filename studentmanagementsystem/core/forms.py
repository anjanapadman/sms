import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from core.models import Login, teacherreg, Student, TimeTable, Notification, Feedback

def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')
class DateInput(forms.DateInput):
    input_type = 'date'
class LoginForm(UserCreationForm):
    username=forms.CharField()
    password1=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label='confirm password',widget=forms.PasswordInput)

    class Meta:
        model=Login
        fields=('username','password1','password2')

class TeacherregForm(forms.ModelForm):
     contact_no = forms.CharField(validators=[phone_number_validator])
     class Meta:
        model= teacherreg
        exclude = ('user',)
class StudentForm(forms.ModelForm):
    contact_no = forms.CharField(validators=[phone_number_validator])
    class Meta:
        model=Student
        exclude=('user',)
class TimeTableForm(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    class Meta:
            model=TimeTable
            fields='__all__'
class NotificationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model=Notification
        fields='__all__'
class FeedbackForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
            model=Feedback
            exclude=('reply',)




